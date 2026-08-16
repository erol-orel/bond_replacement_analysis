# Replacing bonds in a Swiss portfolio — a structured thesis

### VZ AP5 mandate · CHF, monthly total return, net of fees · February 2008 – June 2026

*Structured version of the empirical thesis. It is built to be read top to bottom: what we ask,
the raw material, the exact portfolios we test, then the results one step at a time — first
replacing bonds with **one** alternative, then with a **mix**, then with an **optimised**
allocation. Every number comes from the reproducible pipeline (`analysis/results_manifest.json`,
`analysis/*.csv`).*

---

## 1. Goal and approach

**Goal (one sentence).** Find out whether the **42% in bonds** of the Swiss VZ **AP5** mandate can
be replaced by other investable assets, and **at what cost in risk** — over the full 2008–2026
sample and across interest-rate regimes.

We answer in three clear steps, from simplest to most advanced:

- **Step A — one alternative at a time.** Replace the bonds with a **single** alternative (gold
  only, high yield only, …) and see what each one does on its own.
- **Step B — a mix.** Replace the bonds with a **basket** of alternatives, and justify *which*
  alternatives and *what weights* from Step A.
- **Step C — an optimised allocation.** Let an optimiser choose the "best" weights in-sample, as a
  descriptive upper bound.

Everything is compared to the **AP5 benchmark** (bonds untouched) on the same four things:
**return, volatility, worst loss (drawdown), and extreme loss (CVaR)**, plus the **Sharpe** ratio
(return per unit of risk, measured as excess over CHF cash).

The three questions behind these steps: **(Q1)** does replacing bonds change return? **(Q2)** does
it change downside risk? **(Q3)** does the answer depend on the rate regime?

## 2. The building blocks (2008-02 → 2026-06, CHF, per asset)

Before combining anything, here is each asset on its own — the raw material. Sharpe is excess over
CHF cash.

| Asset (proxy) | CAGR | Vol | Sharpe | MaxDD |
|---|---|---|---|---|
| Swiss equity (SPI) | 6.6% | 12.6% | 0.57 | −38% |
| World equity (MSCI World) | 8.6% | 18.7% | 0.53 | −42% |
| Real estate (SXI) | 6.1% | 7.7% | 0.80 | −19% |
| **Swiss bonds (broad)** | **1.8%** | 3.6% | 0.50 | −16% |
| **Swiss bonds (1–5y)** | **1.1%** | 1.7% | 0.66 | −7% |
| **World bonds (hedged, broad)** | **1.1%** | 3.5% | 0.30 | −18% |
| **World bonds (hedged, 1–5y)** | **0.6%** | 1.8% | 0.31 | −9% |
| Gold (CHF) | 6.1% | 16.4% | 0.44 | −38% |
| High yield (HYG, hedged) | 3.9% | 10.3% | 0.41 | −29% |
| EM debt (EMB, hedged) | 3.3% | 11.5% | 0.33 | −28% |
| Infrastructure (IGF) | 4.0% | 14.8% | 0.34 | −45% |
| Managed futures (RYMFX) | **−0.8%** | 13.8% | 0.01 | −47% |
| Commodities (DBC) | **−1.6%** | 18.9% | 0.00 | −76% |
| Cash (SNB path) | 0.1% | 0.0% | — | −5% |

**What this already tells us.** The bonds did little over 2008–2026 (0.6%–1.8%/yr) — the problem
the thesis is about. Among the candidate replacements, **gold** has the best stand-alone return
(6.1%) but is volatile; **commodities and managed futures actually lost money** over this sample;
**high yield and EM debt** sit in between. No single alternative is an obvious drop-in for bonds.

## 3. The portfolios we test (the map)

This is the full list of what is replaced, by what, and by how much. Bonds are replaced **in 10%
steps** (0%, 10%, …, 100%); "0%" is always the AP5 benchmark.

| ID | What is replaced | Replaced by | How much |
|---|---|---|---|
| **B0** | nothing (benchmark) | — (AP5 as-is) | 0% |
| **A·gold** | bonds | gold only | 0→100% |
| **A·hy** | bonds | high yield only | 0→100% |
| **A·em** | bonds | EM debt only | 0→100% |
| **A·infra** | bonds | infrastructure only | 0→100% |
| **A·cta** | bonds | managed futures only | 0→100% |
| **A·comm** | bonds | commodities only | 0→100% |
| **B·equal** | bonds | equal-weight mix of the 6 above | 0→100% |
| **B·curated** | bonds | curated mix: HY 35 / EM 30 / gold 20 / infra 15 | 0→100% |
| **C·max-Sharpe** | bonds + sleeve | optimiser picks the weights (in-sample) | optimiser |
| **C·min-risk** | bonds + sleeve | optimiser picks the weights (in-sample) | optimiser |

The equity/real-estate/cash core (58%) is always held fixed; only the 42% in bonds is touched.

## 4. Step A — replace bonds with ONE alternative at a time

Replace **100% of the bonds** with a single alternative (`analysis/single_alt_full_replacement.csv`).
Sorted best to worst by Sharpe:

| 100% of bonds → | CAGR | Vol | Sharpe | MaxDD | CVaR95 |
|---|---|---|---|---|---|
| **Gold only** | **5.9%** | 10.4% | **0.60** | **−21%** | −6.8% |
| *Curated mix (for reference)* | 4.9% | 10.0% | 0.52 | −28% | −7.0% |
| **AP5 benchmark (0% replaced)** | 3.6% | 7.7% | **0.48** | −20% | −5.2% |
| High yield only | 4.6% | 10.3% | 0.48 | −31% | −7.3% |
| EM debt only | 4.4% | 10.3% | 0.47 | −26% | −7.3% |
| *Equal-weight mix (for reference)* | 4.3% | 10.1% | 0.46 | −28% | −7.1% |
| Infrastructure only | 4.6% | 12.8% | 0.41 | −39% | −9.4% |
| Managed futures only | 2.9% | 10.2% | 0.32 | −26% | −6.3% |
| Commodities only | 2.4% | 13.1% | 0.24 | −39% | −9.7% |

**Reading this table (the key result of Step A):**
- **Only gold, on its own, clearly beats the benchmark on risk-adjusted return** (Sharpe 0.60 vs
  0.48), and it does so *without* a deeper worst-loss (−21% vs −20%). Every other single
  alternative is **equal to or worse than** simply keeping the bonds.
- **High yield and EM debt** roughly match the benchmark's Sharpe but with **much deeper drawdowns**
  (−31% / −26% vs −20%): more return, more risk, no free lunch.
- **Commodities and managed futures** are the worst: they *lost money* over the sample and drag any
  portfolio down.
- Honesty note on gold: the 0.60 Sharpe is a **single, concentrated bet** — 42% of the portfolio in
  one asset over a sample (2008–2026) in which gold did unusually well, and gold pays **no income**
  (unlike bonds' carry). It is a strong historical result, not a safe recommendation to hold 42%
  gold.

## 5. Step B — replace bonds with a MIX (and why this mix)

A single asset is fragile (all eggs in one basket, especially gold). So we diversify across
several alternatives. Step A tells us **exactly how to build the mix**:

1. **Equal-weight mix of all six** (the naïve choice). Result: Sharpe **0.46** — *slightly worse
   than the benchmark*. Why? Because it gives equal weight to **commodities and managed futures**,
   the two that lost money. **A naïve equal mix is not good enough** — this is an important, honest
   finding.
2. **Curated mix — drop the losers, keep the workers.** Remove commodities and managed futures;
   keep the income assets (high yield, EM debt) and the diversifier (gold), plus a little
   infrastructure: **HY 35% / EM 30% / gold 20% / infra 15%**. Result: Sharpe **0.52** — better
   than both the equal mix and the benchmark.

| Mix (100% of bonds replaced) | CAGR | Vol | Sharpe | MaxDD | CVaR95 |
|---|---|---|---|---|---|
| Equal-weight (all 6) | 4.3% | 10.1% | 0.46 | −28% | −7.1% |
| **Curated (HY/EM/gold/infra)** | **4.9%** | 10.0% | **0.52** | −28% | −7.0% |

> **Justification of the curated weights.** The composition is not arbitrary: it is read directly
> off Step A. High yield and EM debt are the two income assets that best reproduce what bonds *do*
> (carry), so they get the largest weights (35% + 30%). Gold is the one asset that improved
> risk-adjusted return on its own, so it earns a meaningful 20% as the crisis diversifier.
> Infrastructure adds a little real-asset inflation exposure (15%). Commodities and managed futures
> are **excluded** because Step A shows they only added risk and lost money.
>
> **Important caveat.** The curated mix is chosen *after seeing* the full-sample results, so it is
> **exploratory**, not a promise it would have been picked in advance. It should be validated
> out-of-sample before real use. It illustrates that *instrument selection matters*, not that this
> exact basket is optimal.

## 6. Step C — an optimised (advanced) allocation

Finally, let an optimiser choose the 42% weights to maximise in-sample Sharpe (or minimise risk),
across bonds **and** the six alternatives, with realistic caps (`appendix_optimisation_*.csv`).
These weights *see the whole history*, so they are an optimistic **upper bound**, not an
implementable recommendation.

| Optimised (in-sample) | CAGR | Vol | Sharpe | MaxDD | What it chose |
|---|---|---|---|---|---|
| **Max-Sharpe** | 4.4% | 8.1% | **0.56** | −18% | ~30% Swiss bonds + 12% gold (keeps most bonds!) |
| Min-variance / Min-CVaR | 3.3% | 7.5% | 0.46 | −21% | 42% short world bonds (all bonds) |

**The most important lesson of Step C.** Even the optimiser, free to remove bonds entirely,
**keeps a large bond allocation** and only *adds* a little gold. It never chooses to replace bonds
wholesale. This is the same message as Steps A and B, now from an entirely different method: the
best historical portfolio is *bonds plus a modest gold sleeve*, not *bonds replaced by
alternatives*.

## 7. Does the answer depend on the rate regime? (Q3)

Splitting 2008–2026 into four SNB regimes (`analysis/regime_*.csv`), the net return of replacement
depends heavily on what bonds were doing:

| Regime | AP5 | 100% replaced (equal mix) | Reading |
|---|---|---|---|
| R1 2008–14 low-positive rates | 3.7% | 2.8% | bonds strong → replacement **costs** |
| R2 2015–22 negative rates | 3.4% | 5.1% | bonds ≈ 0 → replacement **helps** |
| R3 2022–24 hikes | −0.2% | −1.6% | everything fell → replacement **costs** |
| R4 2024–26 easing | 6.5% | 10.7% | risk assets rally → replacement **helps** |

Replacement pays when bonds are weak and costs when bonds are strong — it is a **bet on the
regime**, not a free improvement.

## 8. Robustness and crises (brief)

- The conclusion **holds** across rebalancing bands (±5–20%), transaction costs (0–50 bps), the
  hedging assumption, the sample window, and whether bands are monitored per-asset or per-category
  (`analysis/robustness_*.csv`).
- A bootstrap (3,000 re-runs) shows **no** replacement level gives a Sharpe gain distinguishable
  from zero, while **extreme loss (CVaR) gets worse with ≈99–100% probability** as you replace more.
- Two crises point opposite ways: in 2020 (COVID) replacement **hurt** (bonds protected); in 2022
  (rate shock) replacement **helped** (bonds and equities fell together). Replacement changes *which*
  crisis you are exposed to; it does not remove crisis risk.

## 9. Main result and recommendation

> **Replacing bonds raises return but also raises volatility and extreme loss, without a reliable
> improvement in risk-adjusted performance.** It is a change in the portfolio's *risk budget*, not
> the discovery of a better asset than bonds.

Concretely, from the three steps:
- **Step A:** on its own, only **gold** improved risk-adjusted return; the rest matched or worsened
  the benchmark, and two alternatives lost money.
- **Step B:** a **naïve equal mix is worse** than keeping bonds; a **curated mix** helps, but only
  as an *ex-post* illustration that selection matters.
- **Step C:** even a free optimiser **keeps most of the bonds** and only adds a little gold.

**Recommendation.**
- **Do not replace bonds wholesale.** It reliably worsens downside without a reliable Sharpe gain.
- If any replacement is made, keep it **partial** and treat it as a **risk-budget decision** (more
  return accepted in exchange for more downside), not an optimisation.
- The single most useful addition historically is a **modest gold allocation alongside bonds** —
  not instead of them — but this is one concentrated bet on one favourable sample and must be
  stress-tested before use.
- **Keep the bond structure** (Swiss + world, broad + short-duration): they behave differently by
  regime and are not redundant.

## What remains (the author's work)

The empirical analysis (data, portfolios, results, robustness) is complete and reproducible. The
remaining work is the written dissertation — literature review, theoretical framework, references,
and the discussion/conclusion prose — which is the student's to write.
