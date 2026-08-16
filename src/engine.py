"""
Backtesting engine with VZ-style Smart Rebalancing (bandwidth/threshold rebalancing),
plus calendar and buy-and-hold rebalancing for comparison.

Core model
----------
A portfolio is a dict {sleeve: target_weight}. We hold units of each sleeve's total-
return index. Between monitoring dates weights drift with prices. On a monitoring date
we check whether any sleeve's weight has left its tolerance band; if so we rebalance the
WHOLE book back to target (the VZ chart shows weights snapping back to the target line).
Transaction costs are applied to the traded turnover.

The engine is frequency-agnostic; the thesis uses monthly CHF total-return data (annualise
with periods=12). Historical constituent data are monthly, so the reconstruction observes the
portfolio monthly and cannot reproduce VZ's intra-month continuous monitoring.
"""
from __future__ import annotations
import numpy as np
import pandas as pd


def _monitor_dates(index: pd.DatetimeIndex, freq: str) -> pd.DatetimeIndex:
    """Last trading day on/before each period end for the given pandas offset alias."""
    if freq in (None, "none", "BH"):
        return pd.DatetimeIndex([])
    marks = pd.Series(index, index=index).resample(freq).last()
    return pd.DatetimeIndex(marks.dropna().values)


def backtest(prices: pd.DataFrame,
             target: dict[str, float],
             *,
             mode: str = "smart",          # 'smart' | 'calendar' | 'buyhold'
             rel_band: float = 0.20,        # relative tolerance band (smart mode)
             monitor_freq: str = "ME",      # monitoring cadence
             tc_bps: float = 10.0,          # one-way transaction cost, bps of turnover
             target_schedule: list | None = None,  # [(Timestamp, target_dict), ...]
             start: str | None = None,
             end: str | None = None) -> dict:
    """Run a backtest. Returns dict with 'value', 'weights', 'trades', 'turnover'.

    If target_schedule is given (list of (date, target_dict)), the active target is the
    most recent scheduled target; a target change forces a rebalance (regime switching).
    All target_dicts must share the same universe as `target`.
    """
    cols = list(target.keys())
    px = prices[cols].copy()
    if start:
        px = px.loc[px.index >= pd.Timestamp(start)]
    if end:
        px = px.loc[px.index <= pd.Timestamp(end)]
    px = px.dropna()
    idx = px.index
    ret = px.pct_change().fillna(0.0)

    def _vec(tdict):
        v = np.array([tdict.get(c, 0.0) for c in cols], dtype=float)
        return v / v.sum()

    # build a per-day target matrix (handles regime switching)
    sched = None
    if target_schedule:
        sched = sorted(((pd.Timestamp(d), _vec(t)) for d, t in target_schedule),
                       key=lambda x: x[0])

    def target_on(day, w_prev):
        if not sched:
            return w_prev
        cur = sched[0][1]
        for d, v in sched:
            if d <= day:
                cur = v
            else:
                break
        return cur

    w_tgt = _vec(target)
    lo, hi = w_tgt * (1 - rel_band), w_tgt * (1 + rel_band)

    if mode == "calendar":
        mdates = set(_monitor_dates(idx, monitor_freq))
    elif mode == "smart":
        mdates = set(_monitor_dates(idx, monitor_freq))
    else:  # buyhold
        mdates = set()

    value = 1.0
    cur_tgt = sched[0][1].copy() if sched else w_tgt.copy()
    w = cur_tgt.copy()                      # start at (initial) target
    vals, whist, trades = [], [], []
    turnover_total = 0.0

    for t, day in enumerate(idx):
        if t > 0:
            r = ret.iloc[t].values
            w = w * (1.0 + r)
            value *= (w.sum())              # portfolio grows by weighted return
            w = w / w.sum()                 # renormalise drifted weights

        # regime switch: if the active target changed, force a rebalance to it
        new_tgt = target_on(day, cur_tgt)
        regime_change = not np.allclose(new_tgt, cur_tgt)
        if regime_change:
            cur_tgt = new_tgt
            lo, hi = cur_tgt * (1 - rel_band), cur_tgt * (1 + rel_band)

        do_rebal = regime_change
        if day in mdates:
            if mode == "calendar":
                do_rebal = True
            elif mode == "smart":
                if np.any(w < lo - 1e-12) or np.any(w > hi + 1e-12):
                    do_rebal = True

        if do_rebal:
            turnover = np.abs(cur_tgt - w).sum() / 2.0   # one-way turnover fraction
            cost = turnover * (tc_bps / 1e4)
            value *= (1 - cost)
            turnover_total += turnover
            trades.append((day, turnover))
            w = cur_tgt.copy()

        vals.append(value)
        whist.append(w.copy())

    out_value = pd.Series(vals, index=idx, name="value") * 100.0
    out_w = pd.DataFrame(whist, index=idx, columns=cols)
    out_tr = pd.DataFrame(trades, columns=["date", "turnover"]).set_index("date") \
        if trades else pd.DataFrame(columns=["turnover"])
    return dict(value=out_value, weights=out_w, trades=out_tr,
                turnover=turnover_total, n_rebal=len(trades),
                target=dict(zip(cols, w_tgt)), mode=mode,
                rel_band=rel_band, monitor_freq=monitor_freq)


# --------------------------------------------------------------------------- metrics
def perf_metrics(value: pd.Series, rf_annual: float = 0.0,
                 periods: int = 252, rf_series: pd.Series | None = None) -> dict:
    """Standard performance/risk metrics from a value series.

    Sharpe/Sortino are computed on EXCESS returns over the risk-free rate. Pass `rf_series`
    (per-period risk-free returns, e.g. the CHF cash proxy) for a time-varying MAR; otherwise
    the scalar `rf_annual` is used. Sharpe = mean(excess)/std(portfolio); Sortino uses the
    proper downside deviation relative to the MAR: sqrt(mean(min(excess,0)^2))."""
    v = value.dropna()
    r = v.pct_change().dropna()
    n = len(r)
    if n == 0:
        return {}
    cagr = (v.iloc[-1] / v.iloc[0]) ** (periods / n) - 1
    vol = r.std() * np.sqrt(periods)
    if rf_series is not None:
        rf_d = rf_series.reindex(r.index).fillna(0.0)
    else:
        rf_d = pd.Series((1 + rf_annual) ** (1 / periods) - 1, index=r.index)
    excess = r - rf_d
    downside = np.sqrt((np.minimum(excess, 0.0) ** 2).mean()) * np.sqrt(periods)  # MAR=rf
    # Sharpe on excess returns: mean(excess)/std(excess) — correct denominator for a
    # time-varying risk-free (with a constant rf, std(excess)==std(r)).
    ex_std = excess.std()
    sharpe = excess.mean() / ex_std * np.sqrt(periods) if ex_std > 0 else np.nan
    sortino = excess.mean() * periods / downside if downside > 0 else np.nan
    dd = v / v.cummax() - 1
    maxdd = dd.min()
    calmar = cagr / abs(maxdd) if maxdd < 0 else np.nan
    var95 = np.percentile(r, 5)
    cvar95 = r[r <= var95].mean()
    var99 = np.percentile(r, 1)
    cvar99 = r[r <= var99].mean()
    # longest drawdown duration (in trading days)
    underwater = (dd < 0).astype(int)
    dur, mx = 0, 0
    for u in underwater:
        dur = dur + 1 if u else 0
        mx = max(mx, dur)
    return dict(
        CAGR=cagr, Vol=vol, Sharpe=sharpe, Sortino=sortino,
        MaxDD=maxdd, Calmar=calmar, VaR95=var95, CVaR95=cvar95,
        VaR99=var99, CVaR99=cvar99, MaxDD_periods=mx,
        TotalReturn=v.iloc[-1] / v.iloc[0] - 1, DownsideVol=downside,
    )


def metrics_table(value_dict: dict[str, pd.Series], rf_annual: float = 0.0) -> pd.DataFrame:
    rows = {k: perf_metrics(v, rf_annual) for k, v in value_dict.items()}
    return pd.DataFrame(rows).T
