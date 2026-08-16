"""
Central configuration: backtest window, AP5 strategic asset allocation, tolerance
bands, and the mapping of every sleeve / bond-replacement candidate to an investable
total-return proxy (SIX-listed CHF ETFs preferred; USD/EUR proxies converted to CHF).

All assumptions are documented in docs/source_materials/00_mandate_and_meeting_notes.md
and docs/methodology.md.
"""
from __future__ import annotations

# ----------------------------------------------------------------------------- window
START = "2019-07-01"        # 01/07/2019
END = "2026-06-30"          # 30/06/2026  (7 years)

BASE_CCY = "CHF"

# ----------------------------------------------------- AP5 strategic asset allocation
# VZ "Anlageprofil 5" (VVIA index implementation). Sums to 1.00.
AP5_TARGET = {
    "swiss_equity": 0.250,
    "world_equity": 0.250,
    "swiss_bonds":  0.168,
    "world_bonds":  0.252,
    "real_estate":  0.050,
    "cash":         0.030,
}
BOND_SLEEVE = ["swiss_bonds", "world_bonds"]          # 42% total
assert abs(sum(AP5_TARGET.values()) - 1.0) < 1e-9

# -------------------------------------------------------------- rebalancing settings
# Smart Rebalancing: relative tolerance band around each target weight.
# Base case ±20% relative (slide shows ±8% relative on equity as a minimum; widened to
# a defensible institutional default). Band width is stress-tested in the analysis.
REL_BAND = 0.20
MONITOR_FREQ = "ME"         # month-end monitoring (pandas offset alias)

# ------------------------------------------------------------------- data proxy map
# Each entry: ticker, native currency, and a short description. adjclose = total return.
# .SW = SIX Swiss Exchange (CHF, dividends reinvested for accumulating share classes).
PROXIES = {
    # --- AP5 benchmark sleeves ---------------------------------------------------
    "swiss_equity": dict(ticker="CHSPI.SW", ccy="CHF",
                         desc="iShares Core SPI (Swiss Performance Index TR)"),
    "world_equity": dict(ticker="XDWL.SW", ccy="CHF",
                         desc="Xtrackers MSCI World (CHF listing, UNHEDGED)"),
    "swiss_bonds":  dict(ticker="CSBGC0.SW", ccy="CHF",
                         desc="iShares Core CHF Swiss bond (SBI-type, CHF)"),
    "world_bonds":  dict(ticker="AGGS.SW", ccy="CHF",
                         desc="iShares Global Aggregate Bond CHF-HEDGED"),
    "real_estate":  dict(ticker="CHSRI.SW", ccy="CHF",
                         desc="iShares Swiss Property / SXI Real Estate Funds"),
    # cash handled synthetically (SNB/SARON path) -> see build_cash()

    # --- bond-replacement candidates (ranked by liquidity in the draft) ----------
    "gold":         dict(ticker="ZGLD.SW", ccy="CHF",
                         desc="ZKB Gold ETF (CHF) — physical gold"),
    "convertibles": dict(ticker="ICVT", ccy="USD",
                         desc="iShares Convertible Bond ETF (USD) -> CHF"),
    "clo":          dict(ticker="JAAA", ccy="USD",
                         desc="Janus Henderson AAA CLO ETF (USD) -> CHF; spliced w/ FLOT pre-2020-10"),
    "infrastructure": dict(ticker="IGF", ccy="USD",
                         desc="iShares Global Infrastructure ETF (USD) -> CHF"),
    "managed_futures": dict(ticker="DBMF", ccy="USD",
                         desc="iMGP DBi Managed Futures (USD) -> CHF"),
    "private_credit": dict(ticker="BIZD", ccy="USD",
                         desc="VanEck BDC Income (public direct-lending proxy, USD) -> CHF"),
    # ils handled synthetically (no daily-liquid Yahoo proxy) -> see build_ils()

    # --- splice / helper series --------------------------------------------------
    "_flot":        dict(ticker="FLOT", ccy="USD",
                         desc="iShares Floating Rate Bond ETF (CLO backfill proxy)"),
}

# FX (Yahoo quotes X=CHF as units of CHF per 1 unit foreign for 'CHF=X' == USDCHF)
FX = {
    "USD": "CHF=X",      # USDCHF  (CHF per USD)
    "EUR": "EURCHF=X",   # EURCHF  (CHF per EUR)
    "GBP": "GBPCHF=X",
}

# Which non-CHF proxies are held via a CHF-HEDGED share class (per VZ / the draft).
# world_equity is intentionally NOT here (PM: equities unhedged). gold via ZGLD.SW is
# CHF-priced physical gold (kept unhedged, the standard Swiss access route).
HEDGE_TO_CHF = ["convertibles", "clo", "infrastructure", "managed_futures", "private_credit"]

# USD short-rate path (approx. SOFR / upper Fed funds), % p.a., for CHF-hedge carry.
USD_PATH = [
    ("2019-07-01", 2.40), ("2019-08-01", 2.15), ("2019-10-31", 1.65),
    ("2020-03-16", 0.15), ("2022-03-17", 0.50), ("2022-05-05", 1.00),
    ("2022-06-16", 1.75), ("2022-07-28", 2.50), ("2022-09-22", 3.25),
    ("2022-11-03", 4.00), ("2022-12-15", 4.50), ("2023-02-02", 4.75),
    ("2023-03-23", 5.00), ("2023-05-04", 5.25), ("2024-09-19", 5.00),
    ("2024-11-08", 4.75), ("2024-12-19", 4.50), ("2025-09-18", 4.25),
    ("2026-06-30", 4.25),
]

# SNB policy-rate path (approx., for synthetic CHF cash & ILS risk-free leg), % p.a.
# step-dated (date -> annual rate). Source: SNB decisions, rounded.
SNB_PATH = [
    ("2019-07-01", -0.75),
    ("2022-06-16", -0.25),
    ("2022-09-22",  0.50),
    ("2022-12-15",  1.00),
    ("2023-03-23",  1.50),
    ("2023-06-22",  1.75),
    ("2024-03-21",  1.50),
    ("2024-06-20",  1.25),
    ("2024-09-26",  1.00),
    ("2024-12-12",  0.50),
    ("2025-03-20",  0.25),
    ("2025-06-19",  0.00),
    ("2026-06-30",  0.00),
]
