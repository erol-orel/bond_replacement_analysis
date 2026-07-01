"""
Portfolio optimisation for the best bond-replacement allocation.

Implements several objectives, all long-only with box constraints and group budgets so
the solutions stay realistic (institutional / OPP2-style caps on illiquid sleeves):

  - max_sharpe        : classic mean-variance tangency
  - min_variance      : global minimum-variance
  - min_cvar          : minimise 95% Conditional VaR (fat-tail aware; addresses the
                        draft's "mean-variance fails for non-Gaussian assets" caveat)
  - risk_parity       : equal risk contribution
  - max_return_capvol : maximise return s.t. vol <= benchmark vol

Two methodological corrections from the draft are applied to the RISK INPUTS:
  1. Dimson-adjusted betas/vols for smoothed/illiquid assets (private_credit, ils) via
     regression on contemporaneous + lagged market returns — recovers true risk.
  2. Liquidity haircuts: hard caps on monthly/locked sleeves (ils, private_credit).

The optimiser sizes the FULL 13-asset book; the AP5 equity/real-estate/cash core can be
held fixed (recommended) so only the 42% bond sleeve is reallocated across bonds + the 7
replacements — matching the mandate.
"""
from __future__ import annotations
import numpy as np
import pandas as pd
from scipy.optimize import minimize

TRADING = 252


# ---------------------------------------------------------------- risk-input helpers
def dimson_vol(asset: pd.Series, market: pd.Series, lags: int = 2) -> float:
    """Un-smoothed annualised vol via Dimson: regress asset on market lags 0..L, sum the
    betas to get the 'true' market beta, then rescale observed vol by (true/observed) beta
    ratio. Recovers understated risk for appraisal-smoothed series."""
    df = pd.concat([asset, market], axis=1).dropna()
    y = df.iloc[:, 0].values
    X = np.column_stack([df.iloc[:, 1].shift(k).fillna(0).values for k in range(lags + 1)])
    X = np.column_stack([np.ones(len(y)), X])
    beta, *_ = np.linalg.lstsq(X, y, rcond=None)
    true_beta = beta[1:].sum()
    contemp = beta[1]
    obs_vol = df.iloc[:, 0].std() * np.sqrt(TRADING)
    if abs(contemp) < 1e-6:
        return obs_vol
    return obs_vol * max(1.0, abs(true_beta) / abs(contemp))


def cov_matrix(rets: pd.DataFrame, market: str = "world_equity",
               smoothed=("private_credit", "ils"), lags: int = 2) -> pd.DataFrame:
    """Annualised covariance with Dimson variance correction for smoothed assets."""
    cov = rets.cov() * TRADING
    corr = rets.corr()
    std = np.sqrt(np.diag(cov.values))
    std = pd.Series(std, index=cov.index)
    for a in smoothed:
        if a in rets.columns:
            std[a] = dimson_vol(rets[a], rets[market], lags)
    # rebuild covariance from corrected stds and original correlation
    D = np.diag(std.values)
    cov_corr = D @ corr.values @ D
    return pd.DataFrame(cov_corr, index=cov.index, columns=cov.columns)


# ------------------------------------------------------------------------ objectives
def _ann_ret(w, mu):            return float(w @ mu)
def _ann_vol(w, cov):           return float(np.sqrt(w @ cov @ w))
def _neg_sharpe(w, mu, cov, rf): return -(_ann_ret(w, mu) - rf) / (_ann_vol(w, cov) + 1e-12)


def _cvar(w, rets, alpha=0.95):
    port = rets.values @ w
    var = np.percentile(port, (1 - alpha) * 100)
    tail = port[port <= var]
    return -(tail.mean() if len(tail) else var)     # positive number = expected loss


def _risk_parity_obj(w, cov):
    w = np.maximum(w, 1e-8)
    rc = w * (cov @ w)
    rc = rc / rc.sum()
    return float(np.sum((rc - 1.0 / len(w)) ** 2))


# --------------------------------------------------------------------------- solver
def optimise(rets: pd.DataFrame, objective="max_sharpe", *, rf=0.0,
             bounds=None, fixed=None, group_caps=None, target_vol=None,
             cov=None) -> dict:
    """Optimise weights over rets.columns.

    fixed      : {asset: weight} held constant (e.g. AP5 equity/RE/cash core).
    bounds     : {asset: (lo, hi)}; default (0, 1) for free assets.
    group_caps : list of (assets, max_total) — e.g. illiquid sleeve cap.
    target_vol : annualised vol cap (for max_return_capvol) or None.
    """
    cols = list(rets.columns)
    mu = rets.mean().values * TRADING
    if cov is None:
        cov = cov_matrix(rets)
    C = cov.loc[cols, cols].values
    n = len(cols)
    fixed = fixed or {}
    free = [c for c in cols if c not in fixed]
    fixed_sum = sum(fixed.values())

    idx = {c: i for i, c in enumerate(cols)}
    b = []
    for c in cols:
        if c in fixed:
            b.append((fixed[c], fixed[c]))
        elif bounds and c in bounds:
            b.append(bounds[c])
        else:
            b.append((0.0, 1.0))
    b = tuple(b)

    cons = [{"type": "eq", "fun": lambda w: w.sum() - 1.0}]
    if group_caps:
        for assets, cap in group_caps:
            ii = [idx[a] for a in assets if a in idx]
            cons.append({"type": "ineq",
                         "fun": (lambda w, ii=ii, cap=cap: cap - w[list(ii)].sum())})
    if target_vol is not None:
        cons.append({"type": "ineq",
                     "fun": lambda w: target_vol - _ann_vol(w, C)})

    if objective == "max_sharpe":
        fun = lambda w: _neg_sharpe(w, mu, C, rf)
    elif objective == "min_variance":
        fun = lambda w: _ann_vol(w, C)
    elif objective == "min_cvar":
        fun = lambda w: _cvar(w, rets)
    elif objective == "risk_parity":
        fun = lambda w: _risk_parity_obj(w, C)
    elif objective == "max_return_capvol":
        fun = lambda w: -_ann_ret(w, mu)
    else:
        raise ValueError(objective)

    # multi-start for robustness
    best = None
    rng = np.random.default_rng(7)
    starts = [np.array([1.0 / n] * n)]
    for _ in range(12):
        r = rng.random(n); r = r / r.sum()
        starts.append(r)
    for w0 in starts:
        try:
            res = minimize(fun, w0, method="SLSQP", bounds=b, constraints=cons,
                           options=dict(maxiter=500, ftol=1e-9))
            if res.success and (best is None or res.fun < best.fun):
                best = res
        except Exception:
            continue
    if best is None:
        raise RuntimeError(f"optimisation failed for {objective}")
    w = np.clip(best.x, 0, 1)
    w = w / w.sum()
    return dict(weights=dict(zip(cols, w)),
                ann_ret=_ann_ret(w, mu), ann_vol=_ann_vol(w, C),
                sharpe=(_ann_ret(w, mu) - rf) / (_ann_vol(w, C) + 1e-12),
                cvar95=_cvar(w, rets), objective=objective)
