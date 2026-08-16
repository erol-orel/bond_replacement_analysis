# Bond Replacement Analysis — VZ AP5 across rate regimes (2008–2026)

Empirical support for the HEC Lausanne MSc Finance thesis
*"Alternatives aux obligations dans la construction de portefeuille en environnement de
taux bas."* We replicate the VZ **Anlageprofil 5 (AP5)** mandate from the **real Bloomberg
constituent indices** with **VZ Smart Rebalancing**, extend it back to **January 2008**,
and replace the 40.75% bond sleeve with investable alternatives **over the whole period** —
read **regime by regime** (SNB). CHF, monthly total return, **net of fees** (0.12% product +
1.25% management).

> **Reframed brief (Aug 2026, with the thesis director).** Replace bonds over the *whole*
> sample and analyse by regime — bonds are a problem both when rates are *low* and when they
> *rise* — which removes the need for a contested low-rate threshold. Earlier 2019–2026
> daily/Yahoo study is retained under `run_analysis.py` / `walkforward.py` / `montecarlo.py`.

## TL;DR findings
- **Validated reconstruction**: rebuilt AP5 tracks the *real* VZ VVIA NAV at **0.94
  correlation / 2.7% tracking error** (2019–2026) — the machinery is trustworthy (fig. 02).
- **The bond problem is not only low rates.** Bonds delivered their premium **only when
  rates fell** (R1 2008–14: +4%/yr). In the negative-rate era (R2) the sleeve earned ≈0;
  when rates *rose* (R3 2022–24) **world bonds lost 2%/yr** on duration (fig. 05).
- **Replacement pays off conditionally**: it wins in the negative-rate (R2) and easing (R4)
  regimes, is neutral during hikes (R3), and *costs* return only when bonds rally (R1).
- **No free lunch over the full cycle**: full replacement lifts CAGR 3.74% → 4.47% but
  raises drawdown −19% → −27% with **Sharpe flat (0.51 → 0.49)**.
- **Recommendation: partial (≈33–66%) replacement** — captures the regime upside, keeps a
  bond core for flight-to-quality, avoids the drawdown penalty of going all-in.
- **Keep both bond sub-indices** (Swiss vs world corr 0.79, divergent in the hiking regime).
- Honest note: **commodities and managed futures lost money 2008–2026**; the equal-weight
  basket carries them, so nothing is cherry-picked.

➡️ Résumé exécutif (FR): **[`reports/resume_executif.md`](reports/resume_executif.md)**
· Full write-up: **[`reports/thesis_report.md`](reports/thesis_report.md)**
· Method: **[`docs/methodology.md`](docs/methodology.md)**
· **Word exports**: `reports/docx/` (FR summary + EN full report) · **FR high-DPI charts**:
`reports/figures_fr/` (`python src/figures_fr.py`; rebuild docx with `python reports/docx/build_docx.py`)
· Thesis structure help: **[`docs/thesis_guidance.md`](docs/thesis_guidance.md)**

## Repo layout
```
src/
  data_bloomberg.py     parse VZ/Bloomberg xlsx -> monthly CHF constituents + rates + VZ NAV
  data_alternatives.py  investable alt proxies (CHF) to 2008 (gold, commodities, HY, EM, ...)
  build_panel.py        merge constituents + alternatives + SNB cash -> monthly panel
  engine.py             VZ Smart Rebalancing (±20% bands) + metrics (frequency-agnostic)
  analysis_2008.py      MAIN: validation, regimes, descriptive stats, replacement steps, figures
  (legacy 2019-2026 study) download_data.py, run_analysis.py, walkforward.py, montecarlo.py
data/bloomberg/         real source workbooks (Bloomberg / SNB / VZ)
data/processed/         monthly CHF panels
analysis/               output tables (perf, regimes, descriptive stats, weights, validation)
reports/                thesis_report.md + figures/
docs/                   methodology.md, thesis_guidance.md, source_materials/
```

## Reproduce
```bash
pip install pandas numpy scipy matplotlib requests openpyxl
export REQUESTS_CA_BUNDLE=/root/.ccr/ca-bundle.crt SSL_CERT_FILE=$REQUESTS_CA_BUNDLE
python src/data_bloomberg.py      # constituents_chf_monthly, rates_monthly, vz_ap5_track
python src/data_alternatives.py   # alternatives_chf_monthly
python src/build_panel.py         # panel_levels_monthly, panel_returns_monthly
python src/analysis_2008.py       # analysis/*.csv, reports/figures/01-08_*.png
python src/appendix_optimization.py   # secondary/theoretical optimised sleeve (appendix)
```

## Portfolios (2008–2026 study)
| ID | Book | Bond sleeve replaced |
|---|---|---|
| P0 | AP5 benchmark | 0% (the mandate, Smart-Rebalanced) |
| P1 | Replace 33% | 33% of the 40.75% sleeve → diversified basket |
| P2 | Replace 66% | 66% |
| P3 | Replace 100% | 100% |

Naïve basket = equal weight of the six alternatives with full 2008 history (gold,
commodities, infrastructure, managed futures, high yield, EM debt). A **curated** basket
(HY 35 / EM debt 30 / gold 20 / infrastructure 15, dropping the two money-losers) dominates
it — Sharpe 0.55 vs 0.49 at full replacement, above AP5's 0.51 (fig. 08). A secondary
in-sample optimisation appendix (`appendix_optimization.py`) shows even the optimiser keeps
bonds.

## Important caveats
Investable ETF/fund **proxies** (not the exact VZ funds); **monthly** frequency understates
intra-month drawdowns; foreign equity is a USD price index converted to CHF TR (cancels in
comparisons, validated at 0.94 corr); convertibles start 2009; commodity/CTA proxies carry
real tracking error; single historical path. Optimisation kept as a secondary/appendix
exercise per the director. See `docs/methodology.md`. Not investment advice.

## Source materials
Under `docs/source_materials/erta_2026-08/`: the VZ *Kundendoku* Smart-Rebalancing slide,
the PM's email (rebalancing = bandwidths; only bonds hedged to CHF), and the SNB
sub-period justification. Raw data workbooks under `data/bloomberg/`.
