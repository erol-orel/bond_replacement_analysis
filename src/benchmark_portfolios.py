"""
Benchmark portfolios — the three comparisons a jury would ask for.

The main study replaces bonds with ALTERNATIVES. This script adds the natural benchmarks
that tell us whether the alternatives bring anything specific:

  B1  bonds -> EQUITIES (the existing AP5 equity mix, scaled). If this matches the
      alternatives, their extra return is just disguised equity risk.
  B2  bonds -> CASH (SNB path). The defensive "do nothing" floor.
  B3  replace only the WORLD bonds (25.2%), keep the Swiss bonds — the asymmetric
      replacement the regime analysis suggests (world bonds lost -2.9%/yr in the
      2022-24 hikes while Swiss bonds stayed positive).

Same assumptions as everything else: net of the 1.37% fee, category-level Smart
Rebalancing (±8%), common 2008-02..2026-06 window, Sharpe = excess over CHF cash.

Outputs: analysis/benchmark_portfolios.csv, analysis/benchmark_portfolios_sweep.csv
Run:  python src/benchmark_portfolios.py   (after build_panel.py)
"""
from __future__ import annotations
import os
import pandas as pd

from config_main import AP5, PRIMARY_W, START
from analysis_2008 import replacement_book
from single_alternatives import _metrics

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROC = os.path.join(HERE, "data", "processed")
ANL = os.path.join(HERE, "analysis")

# B1: the AP5 equity mix, renormalised to 100% (50% of the book -> basket weights)
_EQ = {k: AP5[k] for k in ["swiss_equity", "sli", "spi_extra",
                           "world_equity", "world_small", "em_equity"]}
_eq_tot = sum(_EQ.values())
EQ_BASKET = {k: v / _eq_tot for k, v in _EQ.items()}
# B2: cash only
CASH_BASKET = {"cash": 1.0}
# B3: only the world-bond tranches are replaced (Swiss bonds kept)
WORLD_SLEEVE = {"world_bonds": 0.168, "world_bonds_1_5": 0.084}   # 25.2%


def world_only_book(frac: float, basket: dict = PRIMARY_W) -> dict:
    """AP5 with `frac` of the WORLD bonds moved into `basket`; Swiss bonds untouched."""
    book = dict(AP5)
    for k, w in WORLD_SLEEVE.items():
        book[k] = w * (1 - frac)
    tot = sum(WORLD_SLEEVE.values())
    for k, w in basket.items():
        book[k] = book.get(k, 0.0) + tot * frac * w
    return {k: v for k, v in book.items() if v > 1e-9}


BENCH = {
    "Obligations -> actions (mix AP5)": lambda f: replacement_book(f, EQ_BASKET),
    "Obligations -> cash": lambda f: replacement_book(f, CASH_BASKET),
    "Oblig. MONDIALES seules -> mix egal (suisses gardees)": world_only_book,
}


def main():
    px = pd.read_csv(os.path.join(PROC, "panel_levels_monthly.csv"),
                     index_col=0, parse_dates=True)
    px = px.loc[px.index >= pd.Timestamp(START)]
    cash_ret = px["cash"].pct_change()

    # full table at 100% replacement (plus AP5 and the equal mix for reference)
    rows = {"AP5 (reference)": _metrics(px, AP5, cash_ret),
            "Mix egal des 6 alternatives (100%)": _metrics(px, replacement_book(1.0), cash_ret)}
    for name, maker in BENCH.items():
        rows[f"{name} (100%)"] = _metrics(px, maker(1.0), cash_ret)
    full = pd.DataFrame(rows).T

    # sweep: Sharpe and MaxDD by dose
    sweep_rows = {}
    for name, maker in BENCH.items():
        row = {}
        for f in (0.25, 0.50, 0.75, 1.0):
            m = _metrics(px, maker(f), cash_ret)
            row[f"Sharpe_{int(f*100)}"] = m["Sharpe"]
            row[f"MaxDD_{int(f*100)}"] = m["MaxDD"]
        sweep_rows[name] = row
    sweep = pd.DataFrame(sweep_rows).T

    full.to_csv(os.path.join(ANL, "benchmark_portfolios.csv"))
    sweep.to_csv(os.path.join(ANL, "benchmark_portfolios_sweep.csv"))

    pd.set_option("display.width", 200, "display.max_columns", 20)
    show = full.copy()
    show[["CAGR", "Vol", "MaxDD", "CVaR95"]] *= 100
    print("=== BENCHMARKS (net de frais, fenetre commune, Sharpe vs cash CHF) ===")
    print(show.round(2).to_string())
    print("\n=== SWEEP Sharpe par dose ===")
    print(sweep[[c for c in sweep.columns if c.startswith("Sharpe")]].round(3).to_string())


if __name__ == "__main__":
    main()
