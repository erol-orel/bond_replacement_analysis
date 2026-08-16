# Data dictionary

Monthly panel (`data/processed/panel_levels_monthly.csv`, base 100; returns in
`panel_returns_monthly.csv`), 2008-01 to 2026-06, CHF total return.

| Column | Meaning | Source index | Ccy treatment | History |
|---|---|---|---|---|
| `swiss_bonds` | SBI AAA-BBB (broad) | SBR14T | CHF native | 2008 |
| `swiss_bonds_1_5` | SBI AAA-BBB 1-5 (short) | ST15T | CHF native | 2008 |
| `swiss_equity` | SPI | SPI | CHF native | 2008 |
| `sli` | SLI (Swiss large) | SLI | CHF native | 2008 |
| `spi_extra` | SPI Extra (mid/small) | SPIEX | CHF native | 2008 |
| `world_equity` | MSCI World | MXWO | USD price → CHF TR proxy | 2008 |
| `world_small` | MSCI World Small | MXWOSC | USD price → CHF TR proxy | 2008 |
| `em_equity` | MSCI EM | MXEF | USD price → CHF TR proxy | 2008 |
| `real_estate` | SXI Real Estate Funds | SWIIT | CHF native | 2008 |
| `world_bonds` | Global Aggregate (hedged) | — | CHF-hedged (Bloomberg) | 2008 |
| `world_bonds_1_5` | Global Agg 1-5 (hedged) | — | CHF-hedged; **spliced** pre-2010 | 2010 (spliced 2008) |
| `gold` | SPDR Gold | GLD | USD → CHF unhedged | 2008 |
| `commodities` | Invesco DB Commodity | DBC | USD → CHF unhedged | 2008 |
| `infrastructure` | iShares Global Infra | IGF | USD → CHF unhedged | 2008 |
| `convertibles` | SPDR Blmbg Convertibles | CWB | USD → CHF unhedged | 2009 |
| `managed_futures` | Guggenheim Managed Futures | RYMFX | USD → CHF unhedged | 2008 |
| `high_yield` | iShares iBoxx HY | HYG | **CHF-hedged** (approx.) | 2008 |
| `high_yield_unhedged` | HYG, unhedged | HYG | USD → CHF unhedged | 2008 |
| `em_debt` | iShares JPM EM Bond | EMB | **CHF-hedged** (approx.) | 2008 |
| `em_debt_unhedged` | EMB, unhedged | EMB | USD → CHF unhedged | 2008 |
| `cash` | CHF policy-rate cash proxy | SNB path | CHF | 2008 |

Rates (`rates_monthly.csv`): `snb`, `fed` policy rates (%). VZ NAV
(`vz_ap5_track_monthly.csv`): real VVIA cumulative return, 2019–2026.
Canonical headline numbers: `analysis/results_manifest.json`.
