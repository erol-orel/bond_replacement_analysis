# Methodology (2008–2026 reframed study)

Reproducible pipeline replicating the VZ **AP5** mandate from **Bloomberg constituent
indices**, applying **VZ Smart Rebalancing**, and replacing the bond sleeve with investable
alternatives **over the whole period**, read **regime by regime**. CHF, monthly total
return, net of fees.

> Supersedes the earlier 2019–2026 daily/Yahoo-proxy study. That code
> (`download_data.py`, `run_analysis.py`, `walkforward.py`, `montecarlo.py`) is retained but
> the headline analysis is now `analysis_2008.py`.

---

## 1. Sources (`data/bloomberg/`, provided by the analyst)

| File / sheet | Content |
|---|---|
| `Memoire_de_master.xlsx` → *Indexes data - Bloomberg* | daily index levels: SBI AAA-BBB, SPI, MSCI World, MSCI EM, SXI Real Estate Funds |
| … → *Bonds history* (cols 52–55) | monthly **SNB** and **Fed** policy rates, 2008–2026 |
| … → *Price history AP5 VZ* | the **real** VZ AP5 (VVIA) daily NAV, 2019–2026 (validation) |
| `CHF hedged data.xlsx` | Bloomberg Global Aggregate **CHF-hedged** (world bonds), monthly |
| `Consolidation_allocations.xlsx` | the real VZ AP5 target allocation and its drift, 2017–2026 |

Provenance for the source materials (VZ *Kundendoku* Smart-Rebalancing slide, the PM email
confirming CHF-hedging, the SNB sub-period justification) is archived under
`docs/source_materials/erta_2026-08/`.

## 2. Building the panel

`src/data_bloomberg.py`
- Reads the paired date/value columns per index; resamples to **month-end**.
- Swiss bonds (SBI AAA-BBB), Swiss equity (SPI), real estate (SXI) are native CHF total
  return. World bonds = the **CHF-hedged** Global Aggregate.
- **Foreign equity** (MSCI World / EM) is a Bloomberg *price* index in USD → converted to a
  CHF total-return proxy: `level × USD/CHF` (spot, from Yahoo `CHF=X`) grossed up by a
  constant net dividend yield (`DIV_WORLD = 2.1%`, `DIV_EM = 2.6%`). The equity core is
  identical across all compared portfolios, so this proxy **cancels** in every
  AP5-vs-replacement contrast; it is validated against the real VZ NAV (§5).

`src/data_alternatives.py` — investable proxy total-return series to 2008, CHF:
- **Unhedged** (× spot USD/CHF): gold `GLD`, commodities `DBC`, infrastructure `IGF`,
  convertibles `CWB`, managed futures `RYMFX`.
- **CHF-hedged** (USD local TR + `(r_CHF − r_USD)/12` monthly carry, from the SNB/Fed
  paths): high yield `HYG`, EM debt `EMB` — mirroring VZ's *only bonds are hedged* rule.
- Cat bonds are omitted (no investable vehicle has a clean 2008 history).

`src/build_panel.py` — merges constituents + alternatives + a **CHF cash** index built from
the SNB path (monthly accrual `snb/12`, so it goes **negative** 2015–2022) onto one
month-end grid → `data/processed/panel_levels_monthly.csv`, `panel_returns_monthly.csv`.

## 3. Rebalancing engine

`src/engine.py` — VZ Smart Rebalancing: predefined **±20% relative bands**, monthly
monitoring; the whole book snaps to target only when a sleeve leaves its band. Also supports
calendar and buy-and-hold for comparison, and regime-switching via a target schedule.
Frequency-agnostic; monthly metrics use `periods = 12`. 10 bps one-way transaction cost.

## 4. Fees

A constant **1.37%/yr** load — **0.12% product + 1.25% management** (agreed with the
internship director) — applied as a monthly drag to every portfolio (`net_of_fee`). Applies
equally to AP5 and to all replacement books, so it does not distort the comparison; it does
make the reconstruction directly comparable to the *net* VZ NAV.

## 5. Validation

`analysis_2008.py::validate_vs_vz` reconstructs AP5 (Smart Rebalancing, net of fees) and
compares to the real VZ VVIA NAV over 2019–2026: **corr 0.94, tracking error 2.7%/yr**,
mean absolute monthly gap 0.6% (fig. 02).

## 6. Regimes (`Justification_sous_periodes_BNS.docx`)

Four SNB regimes: **R1 2008–14** (low positive), **R2 2015–22** (negative, −0.75%),
**R3 2022–24** (hikes to +1.75% then plateau), **R4 2024–26** (easing back to 0). Every
book and the bond sleeve itself are measured in each regime — this replaces the contested
"low-rate threshold" with an all-regime reading.

## 7. Replacement design

Move **0 / 33 / 66 / 100%** of the 40.75% bond sleeve into the equal-weight basket of the
six full-history alternatives; equity/RE/cash core fixed. Descriptive statistics and the
Swiss-vs-world-bond redundancy test decide whether the sleeve can be simplified (it cannot:
corr 0.79, divergent in R3). Optimisation is kept as a **secondary/appendix** exercise per
the director.

## 8. Reproduce

```bash
pip install pandas numpy scipy matplotlib requests openpyxl
export REQUESTS_CA_BUNDLE=/root/.ccr/ca-bundle.crt SSL_CERT_FILE=$REQUESTS_CA_BUNDLE
python src/data_bloomberg.py      # -> constituents_chf_monthly, rates_monthly, vz_ap5_track
python src/data_alternatives.py   # -> alternatives_chf_monthly
python src/build_panel.py         # -> panel_levels_monthly, panel_returns_monthly
python src/analysis_2008.py       # -> analysis/*.csv, reports/figures/01-07_*.png
```
