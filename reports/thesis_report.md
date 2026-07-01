# Bond Replacement in a Low-Rate CHF Portfolio
### An empirical replication and stress test of the VZ AP5 mandate, 2019–2026

*Analytical report / thesis working draft — supports the HEC Lausanne MSc Finance thesis
"Alternatives aux obligations dans la construction de portefeuille en environnement de
taux bas."*

All figures are computed from the reproducible pipeline in this repo
(`src/`, `analysis/`, `reports/figures/`). Methodology and caveats: `docs/methodology.md`.

---

## 1. Question and approach

A CHF-denominated balanced mandate (VZ **Anlageprofil 5**) holds **42% in AAA–BBB
sovereign bonds** (16.8% Swiss + 25.2% world). In a zero/negative-rate regime this sleeve
delivers near-zero-to-negative real return while consuming the largest block of the book.
The thesis asks: **can liquid and semi-liquid alternatives replace part of the bond sleeve
and improve the portfolio — first on the Swiss bond allocation, during low-rate periods?**

We answer empirically in four steps:

1. **Replicate AP5** from index/ETF proxies with VZ **Smart Rebalancing** over
   01 Jul 2019 → 30 Jun 2026 (the benchmark, `P0`).
2. **Build bond-replacement portfolios** (`P1–P5`), starting with the Swiss bond sleeve
   and during low-rate regimes, then extending.
3. **Optimise** the 42% sleeve (`O1–O3`) to find the best allocation weightings.
4. **Compare** on performance, drawdown, crisis behaviour, and the **classical risks**
   (liquidity, key-person, tail, etc.).
5. **Stress the conclusions** with an out-of-sample walk-forward and a 3,000-path block
   bootstrap (§7) so the findings are robust, not a single-path or in-sample artefact.

## 2. The building blocks (2019-07 → 2026-06, CHF total return)

| Asset (proxy) | CAGR | Vol | Sharpe | MaxDD | Corr to World Eq |
|---|---|---|---|---|---|
| Swiss equity | 8.9% | 14.8% | 0.65 | −25.9% | 0.67 |
| World equity | 10.2% | 17.9% | 0.63 | −34.7% | 1.00 |
| Real estate | 8.1% | 15.4% | 0.58 | −29.3% | 0.72 |
| **Swiss bonds** | **0.3%** | 7.2% | 0.08 | −19.2% | −0.04 |
| **World bonds (hedged)** | **−1.9%** | 5.1% | −0.35 | −20.0% | 0.00 |
| Gold (CHF) | 12.2% | 15.4% | 0.83 | −21.8% | 0.08 |
| Convertibles (hedged) | 10.6% | 17.0% | 0.68 | −34.2% | **0.42** |
| **AAA CLO (hedged)** | 1.1% | **1.9%** | 0.55 | **−4.0%** | 0.17 |
| Infrastructure (hedged) | 5.4% | 18.5% | 0.38 | −42.2% | 0.36 |
| Managed futures (hedged) | 5.6% | 12.2% | 0.51 | −23.8% | 0.15 |
| Private credit (BDC proxy) | 4.1% | **24.7%** | 0.29 | **−55.5%** | 0.40 |
| ILS (synthetic) | 8.8% | 3.0% | 2.83* | −17.3% | 0.00 |
| Cash (SNB path) | 0.1% | 0.0% | — | −1.6% | 0.01 |

\* ILS Sharpe reflects the calibrated model; treat as illustrative.

**What the raw data already says:**
- The bond sleeve *did the damage the thesis predicts*: Swiss bonds returned **+0.3%/yr**,
  world bonds **−1.9%/yr** (the 2022 crash). Together, 42% of the book earned ≈0.
- **AAA CLO** is the standout *structural* bond substitute: IG, **1.9% vol, −4% max DD**,
  low equity correlation — the "cleanest replacement," exactly as the draft argued. But
  its CHF-hedged return is only ~1.1% because the **USD→CHF hedge cost ate ~3%/yr**.
- **Gold, managed futures, ILS** are the true *diversifiers* (corr ≈ 0 to equities).
- **Convertibles (0.42) and private credit (0.40)** carry high equity correlation — they
  are return enhancers, not bond substitutes.
- The **hedging-cost result is first-order**: any USD-market replacement loses ~3%/yr to
  the CHF hedge in this rate regime. This reshapes the whole ranking for a CHF investor.

See `reports/figures/06_correlation_heatmap.png` and `05_rolling_correlation.png`.

## 3. Portfolios tested

| ID | Name | Idea |
|---|---|---|
| **P0** | AP5 benchmark | The mandate, replicated with Smart Rebalancing |
| **P1** | Swiss bonds → CLO | Replace the 16.8% Swiss sleeve entirely with AAA CLO |
| **P2** | Swiss bonds → diversified | Replace it with CLO 8.4% + ILS 4.2% + gold 4.2% |
| **P3** | Draft recommended | Replace ~20 pts of the 42% sleeve with a 7-asset mix |
| **P4** | Dynamic — Swiss replace | *During low-rate windows only*, run P2; else AP5 |
| **P5** | Dynamic — broad replace | *During low-rate windows only*, replace Swiss + ½ world bonds; else AP5 |
| **O1** | Optimised max-Sharpe | Best in-sample Sharpe (overfit — upper bound) |
| **O2** | Optimised min-variance | Robust low-risk sleeve |
| **O3** | Optimised min-CVaR | Robust, fat-tail-aware — **recommended optimised book** |

Low-rate regime = SNB policy rate ≤ +0.25%. In-sample this gives two windows,
**2019-07 → 2022-09** and **2025-03 → 2026-06**, separated by the 2022–2025 tightening.

## 4. Headline results

| Portfolio | CAGR | Vol | Sharpe | Sortino | MaxDD | Calmar | Total ret | Turnover |
|---|---|---|---|---|---|---|---|---|
| P0 AP5 benchmark | 4.99% | 8.5% | 0.61 | 0.72 | −18.5% | 0.27 | +42.3% | 12% |
| P1 Swiss→CLO | 5.11% | 8.4% | 0.63 | 0.73 | −18.4% | 0.28 | +43.5% | 12% |
| **P2 Swiss→diversified** | **5.89%** | 8.4% | **0.72** | 0.83 | **−18.1%** | 0.32 | **+51.4%** | 18% |
| P3 draft recommended | 6.40% | 9.0% | 0.74 | 0.83 | −21.1% | 0.30 | +56.8% | 24% |
| **O3 opt min-CVaR** | 5.67% | **8.3%** | 0.71 | 0.81 | **−18.2%** | 0.31 | +49.2% | **10%** |
| O2 opt min-variance | 5.41% | 8.3% | 0.67 | 0.78 | −18.4% | 0.29 | +46.5% | 11% |
| O1 opt max-Sharpe† | 7.99% | 9.0% | 0.90 | 1.00 | −19.8% | 0.40 | +74.5% | 18% |
| P4 dynamic Swiss | 5.63% | 8.5% | 0.69 | 0.80 | −18.3% | 0.31 | +48.8% | **80%** |
| P5 dynamic broad | 6.57% | 9.1% | 0.75 | 0.84 | −21.1% | 0.31 | +58.6% | **110%** |

†In-sample overfit; shown as an upper bound, not a recommendation.
Figures: `01_cumulative_returns.png`, `02_drawdown.png`, `03_risk_return.png`.

### Reading the table
- **Every bond-replacement portfolio beat the benchmark** on total return and Sharpe over
  2019–2026. The bond sleeve set a very low bar (≈0% real).
- **Replacing Swiss bonds with AAA CLO alone (P1) barely moves the needle** (+0.12% CAGR).
  After the CHF hedge cost, "the cleanest replacement" is a wash on its own — a crucial,
  slightly counter-intuitive result for a CHF investor.
- **The win comes from *diversifying* the defensive sleeve (P2):** CLO + ILS + gold lifts
  CAGR to 5.9% and Sharpe to 0.72 **while keeping the same −18% drawdown**. Best
  risk-adjusted improvement that does *not* worsen tail risk.
- **Going further (P3, P5) buys return but reintroduces drawdown** (−21%): infrastructure
  and convertibles are equity-like and give back some crisis protection — the exact
  trade-off the draft's "variance-covariance test" predicted.
- **The robust optimised book is O3 (min-CVaR):** +49% total return, lowest CVaR, lowest
  turnover (2 rebalances), and it **keeps 22% in bonds** (world 15.6% + Swiss 6.4%) plus
  CLO 15% and ILS 5%. The optimiser independently rediscovers the draft's thesis: *don't
  abandon bonds — replace part of them and diversify what's left.*

### Optimised 42%-sleeve weights (%)
| Book | Swiss bd | World bd | Gold | Conv | CLO | Infra | Mgd fut | ILS | Priv cr |
|---|---|---|---|---|---|---|---|---|---|
| O1 max-Sharpe | 3.5 | 0.0 | 8.0 | 5.0 | 12.5 | 0.0 | 8.0 | 5.0 | 0.0 |
| O2 min-variance | 13.7 | 12.3 | 0.0 | 0.0 | 15.0 | 0.0 | 0.0 | 1.1 | 0.0 |
| **O3 min-CVaR** | 6.4 | 15.6 | 0.0 | 0.0 | 15.0 | 0.0 | 0.0 | 5.0 | 0.0 |

Note how **CLO hits its 15% cap in every low-risk optimum** — it *is* the structural bond
substitute. Gold/managed-futures only enter when the objective chases return (O1).

## 5. Crisis behaviour (the real test)

Return over each stress window (`analysis/stress_windows.csv`,
`reports/figures/07_stress_windows.png`):

| Portfolio | COVID crash 2020 | 2022 rate shock | SVB Mar-2023 |
|---|---|---|---|
| P0 AP5 benchmark | −18.5% | **−15.1%** | −0.3% |
| P2 Swiss→diversified | −18.1% | −14.4% | −0.7% |
| P3 draft recommended | −21.1% | −13.1% | −1.1% |
| O1 max-Sharpe | −19.8% | **−10.3%** | −2.0% |
| O3 min-CVaR | −18.2% | −13.9% | −1.0% |
| P5 dynamic broad | −21.1% | −11.7% | −0.2% |

- **2022 is the thesis's smoking gun.** When bonds AND equities fell together, the
  benchmark lost −15.1%; **every** replacement book lost less (−10 to −14%), because
  gold and managed futures rose while bonds sank. This is the regime where the 42% bond
  sleeve *failed its job* and diversifiers earned their place.
- **2020 COVID is the counter-example.** In a fast flight-to-quality crash, *sovereign
  bonds rallied* and equity-like alternatives (infrastructure, convertibles) fell — so
  the return-chasing books (P3, P5) drew down **more** (−21%) than the benchmark. This is
  why **O3/P2 keep a bond core** and avoid the equity-like sleeves: they match the
  benchmark's −18% instead of worsening it.
- **Conclusion:** the goal is not "bonds vs alternatives" but **a defensive sleeve that is
  robust across *both* crisis types**. CLO (carry) + ILS (uncorrelated) + gold/CTA
  (inflation/rate-shock hedge) + a retained bond core (deflation/flight-to-quality hedge)
  is the combination that survives 2020 *and* 2022. Bonds alone survive only 2020.

## 6. The dynamic (rates-driven) strategy — does timing help?

P4/P5 switch into replacements **only during low-rate windows** and revert to AP5 when
rates normalise — the literal mandate. They **do** add return (P5 +58.6% vs +42.3%) and
cushion 2022 well. **But:**

- Turnover explodes to **80–110%** (42–43 rebalances) because the volatile alternatives
  keep breaching bands and each regime flip forces a full rebalance. At 10 bps that is
  ~8–11 bps/yr of drag; at realistic CHF retail spreads/taxes it is materially more.
- The static diversified book **P2 achieves 90% of P5's benefit at 1/6th the turnover**
  and a *smaller* drawdown.
- **Takeaway:** regime timing of bond replacement is real but **operationally expensive
  and fragile** (it depends on correctly calling the rate regime). A *permanent*
  diversified defensive sleeve dominates on a cost/robustness basis. Tactically tilting
  *within* that sleeve when rates are low is the pragmatic compromise.

## 7. Robustness — out-of-sample walk-forward & Monte Carlo

A single 2019–2026 path and full-sample optimisation invite two objections: *look-ahead
bias* (the optimiser saw the whole history) and *sampling luck* (one path). We address both.

### 7.1 Out-of-sample walk-forward (`src/walkforward.py`, fig. 08–09)

Weights are re-estimated **using only data available at each date** (expanding window,
24-month burn-in, re-estimated every 6 months) and applied to the *following, unseen*
block. Chaining the blocks gives a genuine OOS track record over **2021-07 → 2026-06
(≈5 years)**.

| Strategy | OOS CAGR | OOS Vol | OOS Sharpe | OOS MaxDD | In-sample (look-ahead) Sharpe | Overfit gap |
|---|---|---|---|---|---|---|
| AP5 benchmark | 3.32% | 7.8% | **0.46** | −17.2% | — | — |
| WF max-Sharpe | 6.20% | 7.8% | **0.81** | −12.8% | 0.81 | **+0.01** |
| WF min-variance | 3.95% | 7.5% | 0.55 | −16.0% | 0.56 | +0.01 |
| WF min-CVaR | 3.72% | 7.5% | 0.52 | −17.0% | 0.59 | +0.07 |

**The overfitting gap is negligible (0.01–0.07 Sharpe).** Estimating the replacement sleeve
on *past* data only still delivered **0.81 OOS Sharpe vs the benchmark's 0.46**, with a
**smaller drawdown (−12.8% vs −17.2%)**. The advantage is *structural* (gold, CTAs, CLO and
ILS diversify by construction), not a curve-fit — the strategy that "worked" was knowable in
real time. Note the OOS window is a tougher benchmark test (it opens just before 2022), which
is exactly why the diversified books separate from AP5 so clearly here.

### 7.2 Block-bootstrap Monte Carlo (`src/montecarlo.py`, fig. 10–12)

We resample the realised daily returns with a **stationary block bootstrap** (mean block ≈ 20
trading days, whole rows drawn jointly so cross-asset correlation is preserved) into **3,000
synthetic 7-year paths**, evaluate each constant-mix book, and read off the distribution.

| Book | Median Sharpe | Sharpe p5–p95 | Median MaxDD | **P(beat AP5 Sharpe)** | **P(smaller MaxDD than AP5)** |
|---|---|---|---|---|---|
| AP5 benchmark | 0.65 | 0.02–1.33 | −18.4% | — | — |
| P1 Swiss→CLO | 0.67 | 0.04–1.35 | −18.1% | 65% | 72% |
| **P2 Swiss→diversified** | 0.76 | 0.12–1.44 | −17.7% | **98.4%** | **82%** |
| P3 draft recommended | 0.79 | 0.12–1.49 | −19.6% | 97.2% | 28% |
| O1 max-Sharpe | 0.96 | 0.29–1.66 | −18.3% | 99.6% | 53% |
| O2 min-variance | 0.72 | 0.09–1.40 | −17.8% | 98.4% | 88% |
| **O3 min-CVaR** | 0.75 | 0.12–1.43 | −17.6% | 98.9% | **90%** |

**Reading the distributions:**
- **The core result is highly robust.** P2 and the O2/O3 optima beat the benchmark on Sharpe
  in **~98–99% of resampled histories** *and* have a smaller drawdown in **82–90%** of them.
  This is the statistical backbone the single-path result needed.
- **The return-chasers are exposed.** P3 and O1 beat on Sharpe/return ~97–99% of the time but
  have a **smaller drawdown in only 28% / 53%** of paths — in most histories they draw down
  *more* than the benchmark. Their edge is return, not safety.
- **CLO alone (P1) is genuinely marginal:** only a 65% chance of beating the benchmark's
  Sharpe — the CHF hedge cost keeps it close to a wash, exactly as §4 argued.
- **Verdict:** the books that win on *both* dimensions with high probability are **P2 and
  O3** — the diversified defensive sleeve with a retained bond core. Robustness confirms the
  point recommendation rather than the aggressive one.

## 8. Classical risks (beyond mean/variance)

Performance is necessary but not sufficient — the mandate explicitly asks about the
*qualitative* risks. Each candidate is scored below. This is where several "high-return"
options fail despite good backtest numbers.

| Candidate | Liquidity risk | Key-person / "one-man" risk | Tail / model risk | Transparency | Capacity | Other |
|---|---|---|---|---|---|---|
| **AAA CLO** | Low (daily UCITS ETF); can gap in stress | **Low** (rules-based, but manager selection of collateral matters) | Structured-credit complexity; correlated-up in a systemic credit crisis | Medium (opaque underlying loans) | High | CHF **hedge cost ~3%/yr** is the binding issue |
| **ILS / cat bonds** | **Medium** (monthly dealing; thin secondary) | Medium (specialist boutiques — Twelve, Plenum, LGT) | **High, non-Gaussian** — a single hurricane/quake ⇒ −15/−30% | Low (peril models) | Medium | Genuinely uncorrelated; size-capped by liquidity+tail |
| **Gold** | **Very low** (deep, intraday) | None | Sentiment/real-rate driven; high vol; no income | High | Very high | No carry — a hedge, not a yield source |
| **Managed futures / CTA** | Low (daily UCITS) | **High** — model/manager dispersion is wide | Negative skew in sharp reversals | Low (black-box) | High | Best 2022 hedge; "crisis alpha" is regime-dependent |
| **Convertibles** | Low (daily) | Medium | Equity-correlated in stress (fails F1) | Medium | Medium | Return enhancer, not a bond substitute |
| **Listed infrastructure** | Low (daily) | Low | High equity beta in crashes; regulatory/political risk | High | High | Inflation linkage, but −42% max DD |
| **Private credit** | **Severe** — 4–7yr lock, capital calls, no secondary | **Very high** — outcome hinges on one GP's underwriting | Default losses lag; **NAV smoothing hides true vol** | **Very low** | Medium | OPP2/BVG caps; reported 2–4% vol is fictitious (Dimson ⇒ 6–10%) |

**Cross-cutting risk points for the thesis:**
1. **Liquidity is the master constraint.** The rebalancing engine can only work if sleeves
   are tradable at the monitoring dates. Private credit (locked) and ILS (monthly) cannot
   be Smart-Rebalanced; they must be sized so the *illiquid bucket ≤ ~5%* (our optimiser
   cap). This is why the daily-liquid CLO/gold/CTA/ILS mix dominates in practice.
2. **Key-person / "one-man" risk** is highest exactly where the backtest looks best:
   CTAs and private credit are *manager bets*, not asset-class bets. Dispersion across
   CTA funds in 2022 was enormous. Mitigation: multi-manager, rules-based ETFs, and
   treating single-manager sleeves as satellites.
3. **Smoothing illusion (private credit).** Its low *reported* volatility is a
   mark-to-model artefact. Our public BDC proxy shows the honest economic risk: 24.7% vol,
   −55% drawdown. A naïve mean-variance optimiser fed smoothed NAVs would massively
   over-allocate — hence the **Dimson correction** and the CVaR objective.
4. **Non-Gaussian tails (ILS).** σ understates cat-bond risk. Size with CVaR/scenario, not
   variance. A single bad hurricane season can erase years of premium.
5. **Currency risk / hedging cost** is the CHF investor's silent tax: ~3%/yr in this
   regime on USD-market replacements. It is the single biggest reason the "obvious" US
   credit substitutes underwhelm net of costs.
6. **Concentration / factor overlap.** Infrastructure and real estate share a "real-asset"
   factor; convertibles overlap equities. Replacements must be checked against the
   *existing* 50% equity + 5% real-estate exposure, not in isolation.

## 9. Recommendation

For a CHF AP5 investor seeking to de-risk the low-yielding 42% bond sleeve **without
giving up crisis protection**:

- **Keep a ~20–22% bond core** (favouring the CHF-hedged world sleeve for the
  flight-to-quality hedge that only sovereigns provide — 2020 proves this).
- **Replace the remaining ~20 pts with a *daily-liquid, diversified* defensive sleeve:**
  AAA CLO ~10–15% (structural substitute), ILS ~3–5% (uncorrelated, size-capped for
  tails), gold ~3–4% and managed futures ~3–4% (the 2022 hedge bonds cannot provide).
- **Prefer the static diversified book (P2) / min-CVaR optimum (O3)** over the dynamic
  regime strategy: ~90% of the benefit, a smaller drawdown, and a fraction of the turnover
  and operational/key-person risk.
- **Avoid sizing convertibles, infrastructure or private credit as bond substitutes** —
  they are equity-like or illiquid and reintroduce the risks bonds were there to hedge.

This is precisely the draft's conclusion, now backed by realised 2019–2026 CHF data **and
confirmed out-of-sample and across 3,000 bootstrap histories** (§7): **the problem was never
that the portfolio held bonds — it was that 42% shared a single failure mode (rate-driven
loss). Diversifying the defensive sleeve, not abandoning it, is the cleanest path to a more
robust CHF portfolio** — and the choice that wins on both return and drawdown with ~90–98%
probability is the *robust* diversified book (P2 / min-CVaR O3), not the aggressive one.

## 10. Suggested thesis extensions
- ~~Out-of-sample walk-forward~~ ✓ done (§7.1) — negligible overfitting gap.
- ~~Monte-Carlo / block-bootstrap resampling~~ ✓ done (§7.2) — 3,000 paths.
- DCC-GARCH conditional covariance (the draft's caveat #1) for regime-aware correlations.
- Explicit OPP2/BVG constraint set for a Swiss pension framing.
- Realised OIS/forward-points hedge cost instead of stepwise policy-rate carry.
- A transaction-cost/turnover budget as a hard optimisation constraint.

*Tables: `analysis/*.csv`. Figures: `reports/figures/*.png`. Full method: `docs/methodology.md`.*
