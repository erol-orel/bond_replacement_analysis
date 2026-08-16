"""
Single source of truth for the 2008-2026 study. Every main script imports its assumptions
from here, so the numbers cannot diverge across modules/docs again (the earlier 40.75% vs
42% inconsistency came from duplicated constants).
"""
from __future__ import annotations

# ---- AP5 strategic target: exact VZ Kundendoku slide-5 index composition (VVIA, profil 5) ----
# Same-index provider splits collapsed to economic exposure; slide bar figures are rounded.
AP5 = {
    # Aktien Schweiz 25%
    "swiss_equity": 0.11, "sli": 0.12, "spi_extra": 0.02,          # SPI / SLI / SPI Extra
    # Aktien Welt 25%
    "world_equity": 0.19, "world_small": 0.03, "em_equity": 0.03,  # MSCI World / Small / EM
    # Zinswerte Schweiz 16.8%
    "swiss_bonds": 0.108, "swiss_bonds_1_5": 0.06,                 # SBI AAA-BBB / 1-5
    # Zinswerte Welt 25.2% (hedged CHF)
    "world_bonds": 0.168, "world_bonds_1_5": 0.084,               # Global Agg / 1-5
    # Immo CH 5% + Liquidität 3%
    "real_estate": 0.05, "cash": 0.03,
}
BOND_SLEEVE = {"swiss_bonds": 0.108, "swiss_bonds_1_5": 0.06,      # 42% total (16.8 + 25.2)
               "world_bonds": 0.168, "world_bonds_1_5": 0.084}
BOND_TOTAL = round(sum(BOND_SLEEVE.values()), 6)                    # 0.42
CORE = {k: v for k, v in AP5.items() if k not in BOND_SLEEVE}      # equity/RE/cash, fixed

# ---- replacement candidates -------------------------------------------------------------
# primary basket: the six alternatives with full 2008 history, EQUAL WEIGHT (pre-specified)
PRIMARY_BASKET = ["gold", "commodities", "infrastructure", "managed_futures",
                  "high_yield", "em_debt"]
PRIMARY_W = {k: 1.0 / len(PRIMARY_BASKET) for k in PRIMARY_BASKET}
# ex-post exploratory basket (chosen after seeing full-sample results — NOT the recommendation)
CURATED_W = {"high_yield": 0.35, "em_debt": 0.30, "gold": 0.20, "infrastructure": 0.15}
# convertibles: a candidate asset class, excluded from the primary basket (history from 2009)

# ---- backtest assumptions (base case) ---------------------------------------------------
PER = 12                       # monthly
FEE_PRODUCT = 0.0012           # underlying product TER (agreed with director)
FEE_MGMT = 0.0125              # VZ wrapper / management fee (agreed with director)
FEE_ANNUAL = FEE_PRODUCT + FEE_MGMT     # 1.37% /yr applied to every book
TC_BPS = 10.0                  # one-way transaction cost, bps of turnover (base)
# Band width is a RECONSTRUCTION ASSUMPTION, not a stated VZ rule. The VZ slide-5 example
# (50% target, 46-54% hard bounds) implies ~±8% relative hard bands; we take that VZ-consistent
# value as the BASE case and show the conclusion survives ±5/10/15/20% (robustness.py).
BAND_BASE = 0.08
BAND_GRID = [0.05, 0.08, 0.10, 0.15, 0.20]
TC_GRID = [0.0, 5.0, 10.0, 25.0, 50.0]

START, END = "2008-01-31", "2026-06-30"
STEPS = list(range(0, 101, 10))        # 0, 10, ..., 100 % of the bond sleeve replaced

# four SNB rate regimes (Justification_sous_periodes_BNS.docx)
REGIMES = {
    "R1_2008-14_low_positive": ("2008-01-31", "2014-12-31"),
    "R2_2015-22_negative": ("2015-01-31", "2022-05-31"),
    "R3_2022-24_hikes_plateau": ("2022-06-30", "2024-02-29"),
    "R4_2024-26_easing": ("2024-03-31", "2026-06-30"),
    "Full_2008-26": (START, END),
}

# stress windows (peak-to-trough style, month-end)
STRESS = {
    "COVID_2020": ("2020-01-31", "2020-04-30"),
    "Rate_shock_2022": ("2021-12-31", "2022-10-31"),
    "SVB_bank_2023": ("2023-02-28", "2023-05-31"),
}


def step_name(pct):
    return "AP5" if pct == 0 else f"repl_{pct}"
