# Methodology — step by step (2008–2026 study)

This document explains **every step** of the analysis so a reader can follow and reproduce it
without reading the code. The goal: replicate the VZ **AP5** mandate from its real index
constituents, extend it back to 2008, and measure what happens when the bond sleeve is
replaced — in 10% steps — by investable alternatives, read across four SNB rate regimes.
CHF, monthly total return, net of fees.

> Supersedes the earlier 2019–2026 daily/Yahoo-proxy study (`download_data.py`,
> `run_analysis.py`, `walkforward.py`, `montecarlo.py`), which is retained for reference.

### All assumptions at a glance

| Assumption | Base case |
|---|---|
| Sample window | 2008-02 – 2026-06 (common to every book; EM debt begins 2008-02) |
| Frequency | Monthly, CHF total return, net of fees |
| Bond sleeve replaced | 42% (16.8% Swiss + 25.2% world), in 10% steps (0, 10, …, 100%) |
| Rebalancing | VZ-style Smart Rebalancing at the **category/sleeve level**; alternatives held as one equal-weighted "alts" sleeve (per-constituent bands = robustness) |
| Band | ±8% relative (VZ-consistent base; ±5/10/15/20% as robustness) |
| Transaction cost | 10 bps one-way of turnover (0–50 bps as robustness) |
| Fee load | 1.37%/yr constant (0.12% product + 1.25% management), exact multiplicative `(1+r)/(1+m)` |
| Cash proxy | SNB policy-rate path, prior month-end (monthly, no intra-month time-weighting) |
| HY/EM currency | CHF-hedged via a policy-rate-implied full-month carry approximation (unhedged as robustness) |
| Risk-free (Sharpe/Sortino) | CHF cash proxy, excess returns (zero-rf variant reported alongside) |

---

## Step 0 — Sources (`data/bloomberg/`, provided by the analyst)

| File / sheet | Content |
|---|---|
| `Memoire_de_master.xlsx` → *Indexes data - Bloomberg* | daily index levels: SBI AAA-BBB (+1-5), SPI, SLI, SPI Extra, MSCI World, MSCI World Small, MSCI EM, SXI Real Estate |
| … → *Bonds history* (cols 52–55) | monthly **SNB** and **Fed** policy rates, 2008–2026 |
| … → *Price history AP5 VZ* | the **real** VZ AP5 (VVIA) daily NAV, 2019–2026 (used for validation) |
| `CHF hedged data.xlsx` | Bloomberg Global Aggregate (+1-5) **CHF-hedged**, monthly |
| `Consolidation_allocations.xlsx` | the real VZ AP5 category allocation and its drift, 2017–2026 |

Provenance images (VZ *Kundendoku* slide 5 = the exact AP5 index composition; slide 6 = the
fund-selection process; the PM email confirming CHF-hedging; the SNB sub-period justification)
are archived under `docs/source_materials/`.

## Step 1 — The exact AP5 allocation (VZ Kundendoku slide 5)

AP5 = *Anlageprofil 5*, implemented as **VVIA** (VV mit Indexanlagen — index funds). The slide
gives the full index-level target. We use it verbatim (same-index provider splits collapsed to
their economic exposure; the slide's bar figures are rounded and re-normalised to the category
totals):

| Category (total) | Index | Weight |
|---|---|---|
| **Aktien Schweiz 25%** | SPI | 11% |
| | SLI | 12% |
| | SPI Extra | 2% |
| **Aktien Welt 25%** | MSCI World | 19% |
| | MSCI World Small Caps | 3% |
| | MSCI Emerging Markets | 3% |
| **Zinswerte Schweiz 16.8%** | SBI AAA-BBB | 10.8% |
| | SBI AAA-BBB 1-5 (short) | 6.0% |
| **Zinswerte Welt 25.2%** (CHF-hedged) | Global Aggregate | 16.8% |
| | Global Aggregate 1-5 (short) | 8.4% |
| **Immobilien CH 5%** | SXI Real Estate Funds | 5% |
| **Liquidität 3%** | CHF cash | 3% |

Totals: **equity 50%, bonds 42%, real estate 5%, cash 3%**. The **bond sleeve to be replaced =
42%** (16.8% Swiss + 25.2% world), and it deliberately keeps its **broad/short-duration split**
— the short (1-5) tranches matter for the rising-rate story (Step 8). This is a strict upgrade
over the earlier draft, which had collapsed Swiss equity to SPI-only, foreign equity to
MSCI-World-only, and the bond sleeve to two broad indices.

The strategic weights are held **fixed** and applied back to 2008 (per the director: *"apply
the same allocation backward with Smart Rebalancing"*). The real product's weights drift
tactically; that drift is used only to tighten the validation (Step 9).

## Step 2 — Building the monthly series (`data_bloomberg.py`)

- Each index is read from its paired date/value columns and resampled to **month-end**.
- Swiss indices (SPI, SLI, SPI Extra, SBI, SXI) are native **CHF total return**.
- World bonds use the **CHF-hedged** Global Aggregate series (from `CHF hedged data.xlsx`).
- Foreign equity indices (MSCI World / Small / EM) are Bloomberg **price** indices in **USD**.
  They are converted to a CHF total-return proxy: `level × USD/CHF` (spot, Yahoo `CHF=X`)
  grossed up by a **fixed ex-ante** net dividend yield (World/Small 2.1%, EM 2.6% — the long-run
  MSCI net yields, **not tuned to the VZ validation**). The equity/RE/cash **core is common to
  every compared portfolio**, so this proxy's direct level bias is shared across strategies;
  however, under band rebalancing it affects breach timing/turnover/cost, so it does **not
  cancel mechanically** — the effect on the AP5-vs-replacement contrast is second-order.

## Step 3 — The CHF cash proxy (`build_panel.py`)

Cash is a **policy-rate cash proxy**: the SNB policy-rate path accrued monthly (`snb/12`),
assuming full and immediate pass-through to cash remuneration. To avoid intra-month look-ahead
(a policy change mid-month applied to the whole month), month *t* is accrued on the **prior
month-end rate** — the information available at the start of the month. It is therefore a
**monthly** proxy: the monthly policy-rate observation is used as a simplified remuneration rate
and **intra-month policy changes are not explicitly time-weighted** (this is not a daily SARON
backtest). Its *return* is negative
over 2015–2022 (the −0.75% era); the wealth index itself does not go negative. This CHF cash
series is also the **risk-free rate** for Sharpe/Sortino (computed on excess returns; a
zero-risk-free variant is reported alongside and barely differs). A SARON-based proxy would be a
natural refinement.

The short world-bond index (Global Aggregate 1-5, hedged) begins only in 2010; its broad
counterpart's returns are **spliced backward** as a proxy for 2008–2009. This makes the short
and broad world-bond series identical in those two GFC years — a strong assumption in a key
stress window, so `robustness.py` re-runs the study from 2010 (no splice) and confirms the
conclusion is unchanged.

## Step 4 — Currency treatment

The VZ PM confirmed VZ hedges **only its own global bond sleeve** to CHF; equities are
unhedged. We follow this for the AP5 core. Extending the hedge to the **credit-like
replacements** (HY, EM debt) is **our modelling assumption**, not a VZ statement. The hedge is
a **policy-rate-implied approximation**: `r_CHF-hedged ≈ r_USD-local + (r_CHF − r_USD)/12`
using the **prior** month-end SNB/Fed differential (same no-look-ahead lag as cash), applied as
a **simplified full-month carry approximation**, which ignores forward points, cross-currency
basis and roll cost — so it is *not* an actual hedged-product return. `robustness.py` re-runs with HY/EM **unhedged** to show
the hedge assumption's impact (it lowers the full-replacement Sharpe from ~0.46 to ~0.43 and removes the partial-Sharpe edge).

## Step 5 — Fees

The fee stack is explicit. The underlying proxy returns are used as the **market benchmark
returns**: where a proxy is a fund/ETF (the alternatives), its **fund-level costs are reflected
in the observed total-return series**; where a proxy is a Bloomberg **index** total-return series
(the AP5 equity/RE/bond core), the series is a gross-of-vehicle-cost market benchmark and does
**not** contain the specific vehicle-level costs of the actual VZ funds. On top of these proxy
returns, the **common VZ wrapper/management load of 1.37%/yr** (0.12% product + 1.25% management,
agreed with the director) is applied to **every** book as an **exact multiplicative** monthly
drag, `net = gross × 1/(1+m)` with `(1+m)^12 = 1.0137`. This 1.37% is a **constant fee assumption
held over the full historical reconstruction** — it does not attempt to reconstruct VZ's exact
historical fee schedule back to 2008. Transaction costs (Step 6) and the FX-hedge cost (Step 4)
are separate. Applying the wrapper equally to AP5 and replacements keeps the comparison clean and
matches the **net** VZ NAV used in validation.

## Step 6 — Rebalancing (`engine.py`)

The mandate uses **band-based monitoring** (not calendar rebalancing) — an observed fact from
the VZ *Kundendoku* and PM email. The **documented example** is the 50%-equity case with soft
bounds 48–52% and hard bounds 46–54%, i.e. **≈±8% relative** hard bands around target. VZ does
**not** publish the general formula for other target weights, so the band width used to
generalise the example is a **reconstruction assumption**, not "the VZ rule". We take the
**VZ-consistent ±8% relative** as the base case and show in `robustness.py` that the conclusion
is unchanged across **±5 / 10 / 15 / 20%**. (This is a **single-band** approximation — the
engine has one band and snaps to target on breach; it does not reproduce VZ's separate 48–52%
soft / 46–54% hard levels, which are not a published operational rule.)

**Monitoring level (primary specification).** The VZ documentation describes Smart Rebalancing at
the **allocation-category level** (the 50% example is a *category* allocation, not an individual
index). The primary specification therefore monitors the ±8% band on **category weights** — Swiss
equities, world equities, Swiss bonds, world bonds, real estate, cash, and the replacement
alternatives as **one "alts" sleeve** with fixed internal (equal) weights — via the engine's
`group_map` argument. The research question is about replacing the **42% bond sleeve**, not about
inventing a new six-asset micro-rebalancing scheme, so the alternatives are held as a single
sleeve rather than each carrying its own tight ±8% band. Monitoring every individual constituent
(per-constituent bands) is kept only as a **robustness comparison**
(`analysis/robustness_granular_vs_category.csv`): it rebalances far more often (≈61–96 vs ≈36–37
triggers over 2008–26) but leaves CAGR/Sharpe/MaxDD essentially unchanged, so the conclusion does
**not** depend on the band architecture.

**Whole-book restore (reconstruction assumption).** When a monitored category leaves its band the
engine restores the **whole book to the strategic target** (`w = target`). The VZ documentation
supports monitoring, predefined bands, and correcting allocations when thresholds are exceeded,
but it does **not** publish the internal trade-allocation algorithm. *We assume that a triggered
rebalance restores the monitored category allocation to its strategic target; the exact VZ
trade-allocation mechanism is not observable from the available documentation.* Costs are 10 bps
one-way transaction cost (0–50 bps sensitivity). The engine is frequency-agnostic; monthly metrics
annualise with `periods = 12`.

## Step 7 — The replacement candidates (`data_alternatives.py`)

Bar the director's requirement — *instruments you can actually buy, whose total return net of
all fees is computable, with a long history* — we use investable index/ETF proxies back to 2008:

| Instrument (proxy) | Role | CHF treatment |
|---|---|---|
| Gold (GLD) | crisis hedge | unhedged |
| Commodities (DBC) | inflation | unhedged |
| Infrastructure (IGF) | real income | unhedged |
| Convertibles (CWB, from 2009) | hybrid | unhedged |
| Managed futures (RYMFX) | crisis-alpha | unhedged |
| High yield (HYG) | credit carry | **CHF-hedged** |
| EM debt (EMB) | credit carry | **CHF-hedged** |

The **naïve basket** equal-weights the six with histories beginning in 2008 (EM debt from
2008-02, which fixes the common 2008-02 – 2026-06 sample window); a **curated basket**
(HY 35 / EM 30 / gold 20 / infra 15) drops the two money-losers and tilts to defensive carry.

### Candidates deliberately excluded (and why)

- **Insurance-linked securities (ILS / cat bonds)** — no investable vehicle has a clean,
  daily/monthly, public **total-return** history back to 2008; the asset is semi-liquid with
  event-driven gaps. Including a synthetic proxy would violate the director's *investable,
  net-of-fee, replicable* bar, so ILS is dropped.
- **Private equity / private credit** — unlisted, **appraisal-based (smoothed) NAV**, quarterly
  liquidity and multi-year lock-ups. A listed BDC/LPE proxy shows *equity* risk, not the
  smoothed private return, and cannot be rebalanced monthly. Excluded on liquidity and
  return-measurement grounds.
- **Swiss mortgage funds** (*fonds hypothécaires suisses*) — attractive in principle (CHF,
  defensive, income), but they are **institutional investment foundations** (Anlagestiftungen):
  unlisted, appraisal-based NAV, semi-annual/quarterly liquidity, **no public daily/monthly
  total-return series or investable benchmark**. We searched public data (Yahoo, SIX tickers)
  and found none usable. Dropped for the same reason as ILS/private markets — with the note
  that if VZ can supply an institutional mortgage-fund NAV series, it would be a natural,
  thesis-relevant CHF addition.

The common thread: every included instrument is **daily/monthly liquid, investable, and
mark-to-market**; every excluded one fails at least one of those tests.

## Step 8 — Regimes (`Justification_sous_periodes_BNS.docx`)

Four SNB regimes, so we can comment on bonds in *every* rate environment, not only low-rate
windows: **R1 2008–14** (low positive), **R2 2015–22** (negative, −0.75%), **R3 2022–24**
(hikes to +1.75% then plateau), **R4 2024–26** (easing back to 0). Both broad and short-duration
bond tranches are shown per regime, so the **duration effect** is explicit (short world bonds
lost far less than broad in the 2022–24 hikes).

## Step 9 — Replacement design, validation & robustness

- **Steps:** move **0, 10, 20, …, 100%** of the 42% bond sleeve into the primary
  (pre-specified equal-weight) basket; the equity/RE/cash core stays fixed. Net of fees.
- **Validation (stylised benchmark, not exact replica):** reconstruct AP5 using VZ's real
  *recorded target-allocation* path (**category level** only — Aktien Ausland/Schweiz,
  Zinswerte Ausland/Schweiz, Immobilien, Liquidität — mapped onto the granular sub-indices via
  the Kundendoku split) as a target schedule. This **assumes the within-category index
  proportions were constant** over the validation window, so the 0.955 is partly a validation of
  that mapping. Because VZ trade dates are unavailable, a change in the recorded target is
  interpreted as a rebalance event. Compared to the real VZ VVIA NAV, 2019–2026:
  **corr 0.955**, regression **β 0.97 / α −0.35%/yr / R² 0.91**, tracking error 2.35%/yr,
  cumulative gap +25.1% vs +21.1%. We treat it as a stylised benchmark, not an exact trading
  reconstruction.
- **Robustness (`robustness.py`):** (i) paired **block-bootstrap CIs** for ΔCAGR/ΔSharpe/ΔMaxDD
  vs AP5 — Sharpe differences straddle zero, drawdown reliably worsens (P up to 91%);
  (ii) **sensitivity matrix** over band, cost, hedge and splice — the qualitative conclusion
  survives the tested variations; (iii) **stress table** (2020/2022/2023, ex-post illustrative).
- **Optimisation** is a **secondary appendix** (`appendix_optimization.py`, in-sample; *not*
  independent evidence — same sample/proxies/construction).
- **Config & tests:** all assumptions live in `src/config_main.py` (single source of truth);
  `tests/test_engine.py` checks weights-sum-to-1, band-rebalance logic, exact fees, turnover
  cost, and that a shared equity-core shock cannot manufacture an edge. Canonical headline
  numbers are written to `analysis/results_manifest.json`, which the reports cite.

## Step 10 — Reproduce

```bash
pip install -r requirements.txt      # pinned versions

# --- DETERMINISTIC default: runs on the committed data/processed/ snapshot (no downloads) ---
python src/analysis_2008.py          # analysis/*.csv + results_manifest.json, figures 01-08
python src/robustness.py             # bootstrap CIs, sensitivity matrix, stress table (fig 09)
python src/appendix_optimization.py  # appendix (secondary)
python src/figures_fr.py             # French 300-dpi charts
python tests/test_engine.py          # unit tests (6 pass)

# --- OPTIONAL data refresh (pulls LIVE Yahoo data; may differ slightly from the snapshot) ---
# $REQUESTS_CA_BUNDLE is used if set (egress proxy); no machine-specific path is hard-coded
python src/data_bloomberg.py && python src/data_alternatives.py && python src/build_panel.py
```

> **Reproducibility.** The committed `data/processed/*.csv` **is** the canonical snapshot; the
> deterministic block above reproduces every number in `results_manifest.json` (which also
> records the code commit, Python/numpy/pandas versions and the risk-free basis) without any
> network access. Only the optional refresh block hits live Yahoo.
>
> **Confidentiality.** The Bloomberg/VZ source files under `data/bloomberg/` and
> `docs/source_materials/` are **confidential** — see `docs/source_register.md`. Keep the
> repository **private**; do not publish without checking redistribution rights.

## Limitations

Investable ETF/fund proxies (not the exact VZ funds); **monthly** frequency understates
intra-month drawdowns; foreign equity is a USD price index converted to CHF TR (common to all
books, second-order under band rebalancing, validated at 0.955 corr); the CHF hedge and cash
are policy-rate approximations; convertibles start 2009 and the short world-bond index is
spliced pre-2010 (shown not to change conclusions); commodity/CTA proxies carry real tracking
error; a single historical path (the bootstrap addresses sampling, not model, uncertainty);
regime inference from four buckets is descriptive, not causal. Academic reproduction, not
investment advice.
