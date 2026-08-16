# Methodology — step by step (2008–2026 study)

This document explains **every step** of the analysis so a reader can follow and reproduce it
without reading the code. The goal: replicate the VZ **AP5** mandate from its real index
constituents, extend it back to 2008, and measure what happens when the bond sleeve is
replaced — in 10% steps — by investable alternatives, read across four SNB rate regimes.
CHF, monthly total return, net of fees.

> Supersedes the earlier 2019–2026 daily/Yahoo-proxy study (`download_data.py`,
> `run_analysis.py`, `walkforward.py`, `montecarlo.py`), which is retained for reference.

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
  grossed up by a constant net dividend yield (World/Small 2.1%, EM 2.6%). Because the
  equity/RE/cash **core is identical in every portfolio we compare**, this proxy **cancels
  exactly** in all AP5-vs-replacement contrasts; it only affects the validation, where it
  performs well (Step 9).

## Step 3 — The CHF cash index (`build_panel.py`)

Cash is built from the **SNB policy-rate path**: monthly accrual = `snb/12`, compounded. This
means cash **goes negative over 2015–2022** (the −0.75% era) — essential to the thesis, and
something a naïve "cash = 0%" assumption would miss.

The short world-bond index (Global Aggregate 1-5, hedged) begins only in 2010; its broad
counterpart's returns are **spliced backward** as a proxy for 2008–2009 (documented in code).

## Step 4 — Currency treatment (PM email)

The VZ PM confirmed: **only the global bond sleeve is hedged to CHF**; equities are unhedged.
We follow this exactly — world bonds and the two credit-like replacements (high yield, EM debt)
are CHF-hedged; equities, real assets and gold keep their FX exposure (Step 7).

## Step 5 — Fees

A constant **1.37%/yr** load — **0.12% product + 1.25% management** (agreed with the director)
— is applied as a monthly drag to **every** portfolio. Applying it equally to AP5 and to all
replacement books means it does not distort the comparison, while making the reconstruction
directly comparable to the **net** VZ NAV.

## Step 6 — Rebalancing (`engine.py`)

VZ **Smart Rebalancing**: predefined **±20% relative bands**, monitored monthly. The whole book
snaps back to target only when a sleeve leaves its band (confirmed by slide 5–6 and the PM
email). 10 bps one-way transaction cost on traded turnover. The engine is frequency-agnostic;
monthly metrics annualise with `periods = 12`.

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

The **naïve basket** equal-weights the six with full 2008 history; a **curated basket**
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

## Step 9 — Replacement design & validation

- **Steps:** move **0, 10, 20, …, 100%** of the 42% bond sleeve into the basket; the
  equity/RE/cash core stays fixed. Reported net of fees, per regime and full-period.
- **Validation:** reconstruct AP5 (Smart Rebalancing, net of fees) using VZ's real category
  drift mapped onto the granular sub-indices, and compare to the real VZ VVIA NAV over
  2019–2026: **corr 0.955, tracking error 2.35%/yr**, mean absolute monthly gap 0.5%. The
  residual tracking error is intrinsic to using public index series + a USD-price equity proxy
  rather than VZ's exact CHF-share-class funds, and it cancels in all comparisons.
- **Optimisation** is kept as a **secondary appendix** (`appendix_optimization.py`, in-sample,
  monthly) at the director's request.

## Step 10 — Reproduce

```bash
pip install pandas numpy scipy matplotlib requests openpyxl
export REQUESTS_CA_BUNDLE=/root/.ccr/ca-bundle.crt SSL_CERT_FILE=$REQUESTS_CA_BUNDLE
python src/data_bloomberg.py      # constituents_chf_monthly, rates_monthly, vz_ap5_track
python src/data_alternatives.py   # alternatives_chf_monthly
python src/build_panel.py         # panel_levels_monthly, panel_returns_monthly
python src/analysis_2008.py       # analysis/*.csv, reports/figures/01-08_*.png
python src/appendix_optimization.py  # appendix (secondary)
python src/figures_fr.py          # French 300-dpi charts
```

## Limitations

Investable ETF/fund proxies (not the exact VZ funds); **monthly** frequency understates
intra-month drawdowns; foreign equity is a USD price index converted to CHF TR (cancels in
comparisons, validated at 0.955 corr); convertibles start 2009 and the short world-bond index
is spliced pre-2010; commodity/CTA proxies carry real tracking error; a single historical path.
Academic reproduction, not investment advice.
