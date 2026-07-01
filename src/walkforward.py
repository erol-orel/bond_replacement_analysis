"""
Out-of-sample walk-forward test.

Motivation: the O1 max-Sharpe book in the base analysis is fitted on the FULL 2019-2026
sample, so its ~0.90 Sharpe is optimistic (look-ahead / in-sample bias). A walk-forward
estimates weights using ONLY past data at each re-estimation date and applies them to the
following, unseen out-of-sample (OOS) block. Chaining the OOS blocks gives an honest,
implementable track record.

Design
------
- Universe: AP5 equity/real-estate/cash CORE fixed (58%); only the 42% bond sleeve is
  reallocated across bonds + the 7 replacements (same as the base optimisation).
- Expanding window: initial training = first `init_months`; re-estimate every `step_months`
  using ALL data up to that date; hold the estimated weights over the next block, applying
  Smart Rebalancing to them.
- Objectives compared OOS: max-Sharpe, min-variance, min-CVaR. Benchmarks: AP5 (P0) and the
  full-sample in-sample optimum (the "cheating" upper bound).

Reuses the existing engine via a target_schedule (each re-estimation = a new target regime).
"""
from __future__ import annotations
import os
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from engine import backtest, perf_metrics
from optimize import optimise, cov_matrix
import portfolios as P
from config import AP5_TARGET

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ANL = os.path.join(HERE, "analysis")
FIG = os.path.join(HERE, "reports", "figures")
os.makedirs(ANL, exist_ok=True); os.makedirs(FIG, exist_ok=True)

CORE = {"swiss_equity": 0.25, "world_equity": 0.25, "real_estate": 0.05, "cash": 0.03}
SLEEVE = ["swiss_bonds", "world_bonds", "gold", "convertibles", "clo",
          "infrastructure", "managed_futures", "ils", "private_credit"]
CAPS = {"gold": (0, 0.08), "convertibles": (0, 0.05), "clo": (0, 0.15),
        "infrastructure": (0, 0.10), "managed_futures": (0, 0.08), "ils": (0, 0.05),
        "private_credit": (0, 0.03), "swiss_bonds": (0, 0.42), "world_bonds": (0, 0.42)}
ILLIQUID_CAP = [(["ils", "private_credit"], 0.05)]

OBJECTIVES = {"WF_max_sharpe": "max_sharpe",
              "WF_min_variance": "min_variance",
              "WF_min_cvar": "min_cvar"}


def _estimate_dates(index, init_months=24, step_months=6):
    """Re-estimation dates: month-ends, starting init_months in, every step_months."""
    me = pd.Series(index, index=index).resample("ME").last().dropna()
    me = pd.DatetimeIndex(me.values)
    start = index.min() + pd.DateOffset(months=init_months)
    dates = [d for d in me if d >= start]
    return dates[::step_months] if step_months > 1 else dates


def walk_forward(px, rets, objective, init_months=24, step_months=6):
    """Return (oos_value, schedule, weight_history) for one objective."""
    cols = list(CORE) + SLEEVE
    R = rets[cols]
    est_dates = _estimate_dates(rets.index, init_months, step_months)
    schedule, whist = [], {}
    for d in est_dates:
        train = R.loc[R.index <= d]
        if len(train) < 250:
            continue
        cov = cov_matrix(train)
        try:
            r = optimise(train, objective, fixed=CORE, bounds=CAPS,
                         group_caps=ILLIQUID_CAP, cov=cov)
        except Exception:
            continue
        book = P._normbook({k: v for k, v in r["weights"].items() if v > 1e-4})
        schedule.append((d, book))
        whist[d] = r["weights"]
    # OOS window starts at first estimation date
    oos_start = schedule[0][0]
    px_oos = px.loc[px.index >= oos_start]
    bt = backtest(px_oos, target=schedule[0][1], target_schedule=schedule,
                  mode="smart", rel_band=0.20)
    return bt["value"], schedule, pd.DataFrame(whist).T


def full_sample_optimum(px, rets, objective, oos_start):
    """In-sample (look-ahead) optimum over the WHOLE period, evaluated on the OOS window
    only — the 'cheating' upper bound."""
    cols = list(CORE) + SLEEVE
    R = rets[cols]
    r = optimise(R, objective, fixed=CORE, bounds=CAPS, group_caps=ILLIQUID_CAP,
                 cov=cov_matrix(R))
    book = P._normbook({k: v for k, v in r["weights"].items() if v > 1e-4})
    px_oos = px.loc[px.index >= oos_start]
    return backtest(px_oos, book, mode="smart", rel_band=0.20)["value"], r["weights"]


def main():
    px = pd.read_csv(os.path.join(HERE, "data/processed/prices_chf.csv"),
                     index_col=0, parse_dates=True)
    rets = pd.read_csv(os.path.join(HERE, "data/processed/returns_daily.csv"),
                       index_col=0, parse_dates=True)

    values, schedules, whists = {}, {}, {}
    for label, obj in OBJECTIVES.items():
        v, sched, wh = walk_forward(px, rets, obj)
        values[label] = v; schedules[label] = sched; whists[label] = wh
    oos_start = schedules["WF_max_sharpe"][0][0]

    # benchmarks on the SAME OOS window
    px_oos = px.loc[px.index >= oos_start]
    values["P0_AP5_benchmark_OOS"] = backtest(px_oos, AP5_TARGET, mode="smart",
                                              rel_band=0.20)["value"]
    # in-sample (look-ahead) upper bounds
    is_weights = {}
    for label, obj in OBJECTIVES.items():
        v_is, w_is = full_sample_optimum(px, rets, obj, oos_start)
        values[f"IS_{obj}_lookahead"] = v_is
        is_weights[obj] = w_is

    # ---- metrics over the OOS window ----
    rows = {}
    for k, v in values.items():
        m = perf_metrics(v)
        rows[k] = dict(CAGR=m["CAGR"], Vol=m["Vol"], Sharpe=m["Sharpe"],
                       Sortino=m["Sortino"], MaxDD=m["MaxDD"], CVaR95=m["CVaR95"])
    mt = pd.DataFrame(rows).T
    mt.to_csv(os.path.join(ANL, "walkforward_metrics.csv"))
    pd.DataFrame(values).to_csv(os.path.join(ANL, "walkforward_values.csv"))

    # in-sample vs OOS Sharpe gap (the overfitting headline)
    gap = {}
    for label, obj in OBJECTIVES.items():
        gap[obj] = dict(
            OOS_Sharpe=perf_metrics(values[label])["Sharpe"],
            InSample_lookahead_Sharpe=perf_metrics(values[f"IS_{obj}_lookahead"])["Sharpe"],
        )
    gapdf = pd.DataFrame(gap).T
    gapdf["overfit_gap"] = gapdf["InSample_lookahead_Sharpe"] - gapdf["OOS_Sharpe"]
    gapdf.to_csv(os.path.join(ANL, "walkforward_overfit_gap.csv"))

    # ---- figures ----
    fig, ax = plt.subplots(figsize=(9, 5))
    show = ["P0_AP5_benchmark_OOS", "WF_max_sharpe", "WF_min_variance", "WF_min_cvar",
            "IS_max_sharpe_lookahead"]
    for i, k in enumerate([s for s in show if s in values]):
        v = values[k]
        ax.plot(v / v.iloc[0] * 100, label=k, lw=2.0 if "benchmark" in k else 1.4,
                ls="--" if k.startswith("IS_") else "-")
    ax.set_title(f"Out-of-sample walk-forward (OOS start {oos_start.date()}) — rebased 100")
    ax.set_ylabel("Index"); ax.legend(fontsize=7)
    fig.savefig(os.path.join(FIG, "08_walkforward.png")); plt.close(fig)

    # overfit gap bar
    fig, ax = plt.subplots(figsize=(7, 4.2))
    x = np.arange(len(gapdf))
    ax.bar(x - 0.2, gapdf["InSample_lookahead_Sharpe"], 0.4, label="In-sample (look-ahead)")
    ax.bar(x + 0.2, gapdf["OOS_Sharpe"], 0.4, label="Out-of-sample (walk-forward)")
    ax.set_xticks(x); ax.set_xticklabels(gapdf.index, fontsize=8)
    ax.set_ylabel("Sharpe"); ax.set_title("In-sample vs out-of-sample Sharpe (overfitting gap)")
    ax.legend(fontsize=8)
    fig.savefig(os.path.join(FIG, "09_overfit_gap.png")); plt.close(fig)

    pd.set_option("display.width", 200)
    print(f"OOS window: {oos_start.date()} -> {px.index.max().date()} "
          f"({len(px_oos)} days)\n")
    print("=== WALK-FORWARD OOS METRICS ===")
    print((mt * [100, 100, 1, 1, 100, 100]).round(2).to_string())
    print("\n=== OVERFITTING GAP (Sharpe) ===")
    print(gapdf.round(2).to_string())


if __name__ == "__main__":
    main()
