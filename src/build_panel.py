"""
Merge the Bloomberg constituents, the alternatives proxies and a CHF cash index into one
monthly total-return panel (levels, base 100) and its monthly simple-return matrix.

Cash is built from the SNB policy-rate path (monthly accrual = snb/12), so it correctly
goes NEGATIVE over the 2015-2022 negative-rate era — central to the thesis.

Output: data/processed/panel_levels_monthly.csv , panel_returns_monthly.csv
Run:  python src/build_panel.py   (after data_bloomberg.py and data_alternatives.py)
"""
from __future__ import annotations
import os
import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROC = os.path.join(HERE, "data", "processed")


def build_cash(rates: pd.DataFrame) -> pd.Series:
    m = rates["snb"] / 100.0 / 12.0
    lvl = (1.0 + m).cumprod()
    return (lvl / lvl.iloc[0] * 100).rename("cash")


def main():
    con = pd.read_csv(os.path.join(PROC, "constituents_chf_monthly.csv"),
                      index_col=0, parse_dates=True)
    alt = pd.read_csv(os.path.join(PROC, "alternatives_chf_monthly.csv"),
                      index_col=0, parse_dates=True)
    rates = pd.read_csv(os.path.join(PROC, "rates_monthly.csv"),
                        index_col=0, parse_dates=True)
    cash = build_cash(rates)

    # Global Aggregate 1-5 (hedged, short world bonds) starts only in 2010; splice the broad
    # Global Aggregate (hedged) returns backward as a proxy so 2008-2009 is covered.
    if con["world_bonds_1_5"].isna().any():
        wb15, broad = con["world_bonds_1_5"], con["world_bonds"]
        first = wb15.first_valid_index()
        ratio = wb15.loc[first] / broad.loc[first]
        pre = con.index < first
        con.loc[pre, "world_bonds_1_5"] = broad.loc[pre] * ratio

    # normalise every index to the same month-end grid before merging
    def to_me(obj):
        obj = obj.copy()
        obj.index = obj.index.to_period("M").to_timestamp("M")
        return obj[~obj.index.duplicated(keep="last")]
    con, alt, cash = to_me(con), to_me(alt), to_me(cash.to_frame())["cash"]

    panel = pd.concat([con, alt, cash], axis=1, sort=True).loc["2008-01-31":"2026-06-30"]
    panel.to_csv(os.path.join(PROC, "panel_levels_monthly.csv"))
    rets = panel.pct_change()
    rets.to_csv(os.path.join(PROC, "panel_returns_monthly.csv"))

    print("PANEL:", panel.shape, panel.index.min().date(), "->", panel.index.max().date())
    print("columns:", list(panel.columns))
    print("\nfirst valid index per column:")
    print(panel.apply(lambda c: c.first_valid_index().date()).to_string())
    print("\ncash: first", round(cash.iloc[0], 1), "last", round(cash.iloc[-1], 2),
          "| min level", round(cash.min(), 2), "(negative-rate drag)")


if __name__ == "__main__":
    main()
