"""
APPENDIX (secondary / theoretical).

The thesis director judged portfolio optimisation "too theoretical" to headline, so this is
kept deliberately out of the main analysis. It answers only one question: if one *did*
optimise the 42% sleeve over the full 2008-2026 sample (equity/RE/cash core fixed),
across bonds + the six full-history alternatives, what would the "optimal" sleeve look like
and how would it compare to the simple AP5 / curated books?

These weights are IN-SAMPLE (they see the whole history) and therefore optimistic; they are
a descriptive upper bound, not an implementable recommendation.

Run:  python src/appendix_optimization.py   (after build_panel.py)
"""
from __future__ import annotations
import os
import numpy as np
import pandas as pd

import optimize
optimize.TRADING = 12                      # monthly annualisation for this appendix
from optimize import optimise               # noqa: E402
from engine import backtest, perf_metrics   # noqa: E402
from config_main import BAND_BASE, TC_BPS   # noqa: E402

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROC = os.path.join(HERE, "data", "processed")
ANL = os.path.join(HERE, "analysis")
PER = 12

# granular AP5 equity/RE/cash core, held fixed (58%)
CORE = {"swiss_equity": 0.11, "sli": 0.12, "spi_extra": 0.02,
        "world_equity": 0.19, "world_small": 0.03, "em_equity": 0.03,
        "real_estate": 0.05, "cash": 0.03}
# the 42% sleeve: four bond tranches + six alternatives
SLEEVE = ["swiss_bonds", "swiss_bonds_1_5", "world_bonds", "world_bonds_1_5",
          "gold", "commodities", "infrastructure", "managed_futures", "high_yield", "em_debt"]
# realistic caps so no single alternative dominates the defensive sleeve
CAPS = {"swiss_bonds": (0, 0.42), "swiss_bonds_1_5": (0, 0.42), "world_bonds": (0, 0.42),
        "world_bonds_1_5": (0, 0.42), "gold": (0, 0.12), "commodities": (0, 0.08),
        "infrastructure": (0, 0.10), "managed_futures": (0, 0.10),
        "high_yield": (0, 0.20), "em_debt": (0, 0.15)}


def net_of_fee(value, fee=0.0137):
    r = value.pct_change().fillna(0.0)
    m = (1 + fee) ** (1 / PER) - 1
    n = ((1 + r) / (1 + m)).cumprod()          # exact multiplicative fee (matches main study)
    return n / n.iloc[0] * 100


def main():
    px = pd.read_csv(os.path.join(PROC, "panel_levels_monthly.csv"),
                     index_col=0, parse_dates=True)
    cols = list(CORE) + SLEEVE
    R = px[cols].pct_change().dropna()
    cov = R.cov() * PER

    books = {}
    for obj in ["min_variance", "max_sharpe", "min_cvar"]:
        r = optimise(R, obj, fixed=CORE, bounds=CAPS, cov=cov)
        w = {k: round(v, 4) for k, v in r["weights"].items() if v > 1e-3}
        books[f"OPT_{obj}"] = w

    cash_ret = px["cash"].pct_change()
    rows, weights = {}, {}
    for name, w in books.items():
        bt = backtest(px, w, mode="smart", rel_band=BAND_BASE, monitor_freq="ME", tc_bps=TC_BPS)
        m = perf_metrics(net_of_fee(bt["value"]), periods=PER, rf_series=cash_ret)
        rows[name] = {k: m[k] for k in ["CAGR", "Vol", "Sharpe", "MaxDD", "CVaR95"]}
        weights[name] = w
    tbl = pd.DataFrame(rows).T
    wt = pd.DataFrame(weights).T.fillna(0)
    tbl.to_csv(os.path.join(ANL, "appendix_optimisation_perf.csv"))
    wt.to_csv(os.path.join(ANL, "appendix_optimisation_weights.csv"))

    pd.set_option("display.width", 220, "display.max_columns", 20)
    print("=== APPENDIX: optimised sleeve (IN-SAMPLE, secondary) — net of fees ===")
    print((tbl * [100, 100, 1, 100, 100]).round(2).to_string())
    print("\nSleeve weights (equity/RE/cash core fixed at 58%):")
    print((wt[[c for c in SLEEVE if c in wt.columns]] * 100).round(1).to_string())
    print("\nNote: in-sample, optimistic; a descriptive upper bound, not a recommendation.")


if __name__ == "__main__":
    main()
