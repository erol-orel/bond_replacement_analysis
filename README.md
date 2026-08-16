# Bond Replacement Analysis — VZ AP5 across rate regimes (2008–2026)

Empirical support for the HEC Lausanne MSc Finance thesis
*"Alternatives aux obligations dans la construction de portefeuille en environnement de
taux bas."* We replicate the VZ **Anlageprofil 5 (AP5 / VVIA)** mandate from its **exact
Bloomberg index constituents** (VZ Kundendoku slide 5) with **VZ Smart Rebalancing**, extend
it back to **January 2008**, and replace the **42% bond sleeve** with investable alternatives
**over the whole period** — read **regime by regime** (SNB). CHF, monthly total return, **net
of fees** (0.12% product + 1.25% management).

> **Reframed brief (Aug 2026, with the thesis director).** Replace bonds over the *whole*
> sample and analyse by regime — bonds are a problem both when rates are *low* and when they
> *rise* — which removes the need for a contested low-rate threshold. Earlier 2019–2026
> daily/Yahoo study is retained under `run_analysis.py` / `walkforward.py` / `montecarlo.py`.

## TL;DR findings
- **Validated reconstruction**: rebuilt AP5 (granular index composition) tracks the *real* VZ
  VVIA NAV at **0.955 correlation / 2.35% tracking error** (2019–2026) — trustworthy (fig. 02).
- **The bond problem is not only low rates, and duration is the channel.** Bonds paid off
  **only when rates fell** (R1 2008–14: +4%/yr). In the negative-rate era (R2) the sleeve
  earned ≈0; when rates *rose* (R3 2022–24) broad world bonds **lost 2%/yr** — while the
  short-duration (1-5) tranche lost only −0.8% (fig. 05).
- **Replacement pays off conditionally**: it wins in the negative-rate (R2) and easing (R4)
  regimes, is neutral during hikes (R3), and *costs* return only when bonds rally (R1).
- **No free lunch over the full cycle**: full replacement lifts CAGR 3.43% → 4.30% but raises
  drawdown −21% → −28% with **Sharpe flat** (peaks only mildly, ~0.49 around 20–40%).
- **Recommendation: partial (≈20–40%) replacement** — sits at the Sharpe peak, captures the
  regime upside, keeps a bond core for flight-to-quality.
- **Curate the basket**: dropping the two money-losers (commodities, managed futures) and
  tilting to credit + gold lifts full-replacement Sharpe 0.47 → **0.53**, above AP5's 0.47.
- **Excluded with reasons**: ILS, private equity/credit, and Swiss mortgage funds — all fail
  the *investable / liquid / net-of-fee* bar (no public mark-to-market series). See methodology.

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
Bond sleeve (42%) replaced in **10% steps**: `AP5` (0%), `repl_10`, `repl_20`, …, `repl_100`.
Equity/RE/cash core held fixed at the granular AP5 composition.

Naïve basket = equal weight of the six alternatives with full 2008 history (gold, commodities,
infrastructure, managed futures, high yield, EM debt). A **curated** basket (HY 35 / EM 30 /
gold 20 / infra 15, dropping the two money-losers) dominates it — full-replacement Sharpe
**0.53 vs 0.47**, above AP5's 0.47 (fig. 08). A secondary in-sample optimisation appendix
(`appendix_optimization.py`) shows even the optimiser keeps bonds (min-variance → 100%
short-duration world bonds).

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
