"""
Single-alternative replacement — "one alternative at a time".

The main study replaces bonds with an equal-weight BASKET of six alternatives. This script
answers the prior, simpler question a reader asks first: *what does each alternative do on its
OWN?* For every one of the six alternatives it replaces the bonds (0->100%) with that single
alternative, and reports CAGR / volatility / Sharpe (excess over CHF cash) / MaxDD / CVaR95.

It then places the two mixes (equal-weight, curated) on the same table, so the reader can see
why a mix is used rather than any single winner. All net of the 1.37% fee, category-level
Smart Rebalancing, common 2008-02..2026-06 window — identical assumptions to the main study.

Outputs: analysis/single_alt_full_replacement.csv, analysis/single_alt_sweep.csv
Run:  python src/single_alternatives.py   (after build_panel.py)
"""
from __future__ import annotations
import os
import pandas as pd

from engine import backtest, perf_metrics
from config_main import (PRIMARY_BASKET, PRIMARY_W, CURATED_W, BAND_BASE, TC_BPS,
                         CATEGORY, PER, START)
from analysis_2008 import replacement_book, net_of_fee

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROC = os.path.join(HERE, "data", "processed")
ANL = os.path.join(HERE, "analysis")

# human-readable names (proxy tickers kept for transparency)
LABEL = {
    "gold": "Gold (GLD)",
    "commodities": "Commodities (DBC)",
    "infrastructure": "Infrastructure (IGF)",
    "managed_futures": "Managed futures (RYMFX)",
    "high_yield": "High yield (HYG, hedged)",
    "em_debt": "EM debt (EMB, hedged)",
}


def _metrics(px, book, cash_ret):
    bt = backtest(px, book, mode="smart", rel_band=BAND_BASE, monitor_freq="ME",
                  tc_bps=TC_BPS, group_map=CATEGORY)
    m = perf_metrics(net_of_fee(bt["value"]), periods=PER, rf_series=cash_ret)
    return {k: m[k] for k in ("CAGR", "Vol", "Sharpe", "MaxDD", "CVaR95")}


def full_replacement_table(px, cash_ret):
    """Each single alternative replacing 100% of bonds, plus the two mixes and AP5."""
    from config_main import AP5
    rows = {}
    rows["AP5 (0% replaced)"] = _metrics(px, AP5, cash_ret)
    for a in PRIMARY_BASKET:
        rows[LABEL[a]] = _metrics(px, replacement_book(1.0, {a: 1.0}), cash_ret)
    rows["Equal-weight mix (6)"] = _metrics(px, replacement_book(1.0, PRIMARY_W), cash_ret)
    rows["Curated mix"] = _metrics(px, replacement_book(1.0, CURATED_W), cash_ret)
    tbl = pd.DataFrame(rows).T
    return tbl


def sweep_table(px, cash_ret, fracs=(0.25, 0.50, 0.75, 1.0)):
    """Each single alternative across replacement fractions (Sharpe and MaxDD)."""
    rows = {}
    for a in PRIMARY_BASKET:
        row = {}
        for f in fracs:
            m = _metrics(px, replacement_book(f, {a: 1.0}), cash_ret)
            row[f"Sharpe_{int(f*100)}"] = m["Sharpe"]
            row[f"MaxDD_{int(f*100)}"] = m["MaxDD"]
        rows[LABEL[a]] = row
    return pd.DataFrame(rows).T


def main():
    px = pd.read_csv(os.path.join(PROC, "panel_levels_monthly.csv"),
                     index_col=0, parse_dates=True)
    px = px.loc[px.index >= pd.Timestamp(START)]
    cash_ret = px["cash"].pct_change()

    full = full_replacement_table(px, cash_ret)
    sweep = sweep_table(px, cash_ret)
    full.to_csv(os.path.join(ANL, "single_alt_full_replacement.csv"))
    sweep.to_csv(os.path.join(ANL, "single_alt_sweep.csv"))

    pd.set_option("display.width", 200, "display.max_columns", 20)
    show = full.copy()
    show[["CAGR", "Vol", "MaxDD", "CVaR95"]] *= 100
    print("=== 100% OF BONDS REPLACED BY A SINGLE ALTERNATIVE (net of fees) ===")
    print("    (CAGR/Vol/MaxDD/CVaR95 in %, Sharpe vs CHF cash; sorted by Sharpe)")
    print(show.round(2).sort_values("Sharpe", ascending=False).to_string())
    print("\n=== SINGLE-ALTERNATIVE SWEEP — Sharpe by replacement fraction ===")
    sh = sweep[[c for c in sweep.columns if c.startswith("Sharpe")]]
    print(sh.round(3).to_string())


if __name__ == "__main__":
    main()
