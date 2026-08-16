# Alternatives to bonds in a low-rate environment — empirical foundation (2008–2026)

**HEC Lausanne · MSc Finance thesis · CHF, monthly total return, net of fees**

> Reframed brief (agreed with the thesis director): find **alternatives to the bond sleeve**
> and replace it **over the whole 2008–2026 period**, then read the results **regime by
> regime**. Bonds are a problem not only when rates are *low* but also when they *rise*, so
> the analysis comments on bonds in *every* SNB regime — which removes the need for a contested
> "low-rate threshold". Every methodological step is documented in `docs/methodology.md`.

---

## 1. What this is

An empirical replication of the **VZ AP5** mandate (VZ Säule 3a mit ETF, *Anlageprofil 5*,
implemented as **VVIA**) built from its **exact Bloomberg index constituents** (VZ *Kundendoku*
slide 5), extended back to **January 2008** and run with **VZ Smart Rebalancing**. The 42% bond
sleeve is then replaced — in **10% steps** — by a diversified basket of **investable
alternatives**, measured **net of the agreed fee load** across the four SNB rate regimes.

Reproducible end-to-end: see `docs/methodology.md` §10.

## 2. The exact AP5 allocation (VZ Kundendoku slide 5)

We reproduce the mandate at the **index level**, not the asset-class level:

| Category | Indices (weight) |
|---|---|
| Swiss equity 25% | SPI 11% · SLI 12% · SPI Extra 2% |
| World equity 25% | MSCI World 19% · MSCI World Small 3% · MSCI EM 3% |
| Swiss bonds 16.8% | SBI AAA-BBB 10.8% · SBI AAA-BBB 1-5 6% |
| World bonds 25.2% (CHF-hedged) | Global Aggregate 16.8% · Global Aggregate 1-5 8.4% |
| Real estate 5% | SXI Real Estate Funds |
| Cash 3% | CHF cash (SNB path) |

**Equity 50% · bonds 42% · real estate 5% · cash 3%.** The **bond sleeve to be replaced = 42%**,
and it keeps its **broad/short-duration split** — the short (1-5) tranches are what limit the
damage when rates rise (§6). These strategic weights are applied unchanged back to 2008.

## 3. Data & method (summary; full detail in `docs/methodology.md`)

- **Sources**: Bloomberg index levels; SNB + Fed policy rates; the **real VZ AP5 NAV**
  (2019–2026, for validation); the VZ allocation-drift history — all provided by the analyst.
- **Currency**: only bonds (and the credit-like replacements) are **CHF-hedged**, per the VZ PM.
- **Cash**: built from the SNB path, so it goes **negative** over 2015–2022.
- **Fees**: **1.37%/yr** (0.12% product + 1.25% management) applied to every book.
- **Rebalancing**: VZ Smart Rebalancing, ±20% relative bands, monthly, 10 bps cost.

## 4. Validation — the reconstruction is real

Reconstructed AP5 (indices → Smart Rebalancing → net of fees, using VZ's real allocation drift)
vs the **actual VZ VVIA NAV**, 2019–2026 (85 months, fig. 02):

| | value |
|---|---|
| Correlation of monthly returns | **0.955** |
| Annualised tracking error | **2.35%** |
| Mean absolute monthly gap | 0.5% |
| Total return: reconstruction vs real VZ | +25.1% vs +21.1% |

For a **proxy reconstruction** (public index series, not VZ's exact CHF-share-class ETFs), a
2–3%/yr tracking error is expected; a passive fund runs 0.1–0.5%, an active fund 2–6%. The
residual here is the foreign-equity leg (a USD price index + FX proxying 50% of the book) and
**cancels exactly in every AP5-vs-replacement comparison** because the equity core is identical
across all books. Correlation 0.955 and the visual match through COVID and 2022 are what the
validation needs to license extending the machinery back to 2008.

## 5. The replacement candidates — included and excluded

**Included** (investable, liquid, mark-to-market, ≤2009 history): gold, commodities,
infrastructure, convertibles, managed futures, high yield (hedged), EM debt (hedged). Naïve
basket = equal weight of the six with full 2008 history. Descriptive stats 2008–2026:

| Instrument | CAGR | Vol | Sharpe | MaxDD | note |
|---|---|---|---|---|---|
| Gold | 6.2% | 16.3% | 0.45 | −38% | positive skew (crisis hedge) |
| Commodities | **−1.6%** | 18.9% | 0.01 | −76% | **lost money** |
| Infrastructure | 3.7% | 14.8% | 0.32 | −45% | equity-like |
| Convertibles (2009) | 10.0% | 12.6% | 0.82 | −24% | equity-linked |
| Managed futures | **−0.7%** | 13.8% | 0.02 | −47% | **lost money**, crisis-alpha |
| High yield (hedged) | 3.7% | 10.3% | 0.41 | −29% | credit carry, fat tails |
| EM debt (hedged) | 3.3% | 11.5% | 0.34 | −28% | credit carry, fat tails |

**Excluded, with reasons** (all fail the director's *investable / net-of-fee / liquid* bar):
- **ILS / cat bonds** — no clean public daily/monthly total-return history to 2008; semi-liquid.
- **Private equity / private credit** — unlisted, appraisal-**smoothed** NAV, lock-ups; a listed
  proxy shows equity risk, not the private return, and can't be rebalanced monthly.
- **Swiss mortgage funds** — institutional investment foundations: unlisted, appraisal-based NAV,
  semi-annual liquidity; **no public series/benchmark found** (we searched). A natural CHF
  addition *if* VZ can supply an institutional NAV series.

## 6. The core problem, seen regime by regime — duration matters

Annualised return of each bond tranche in each SNB regime (fig. 05):

| SNB regime | Swiss broad | Swiss 1-5 | World broad | World 1-5 | Cash |
|---|---|---|---|---|---|
| **R1 2008–14** low positive | +4.0% | +2.5% | +4.1% | +2.5% | +0.5% |
| **R2 2015–22** negative | −0.8% | −0.4% | −0.6% | −0.7% | −0.8% |
| **R3 2022–24** hikes | +2.9% | +1.5% | **−2.0%** | **−0.8%** | +1.2% |
| **R4 2024–26** easing | +2.4% | +1.9% | −0.3% | +0.5% | +0.5% |

Two readings the thesis needs:
1. **Bonds delivered their premium only when rates fell (R1).** In the negative-rate era (R2)
   the whole fixed-income + cash sleeve earned **≈ 0 or less**; when rates *rose* (R3) broad
   world bonds **lost 2%/yr**.
2. **Duration is the transmission channel.** In the 2022–24 hikes, the **short (1-5)** world
   tranche lost only −0.8% vs the broad −2.0% — VZ's own short-duration split already cushions
   the rate shock. Swiss and world bonds are correlated (0.79) but **not redundant** (they
   diverge sharply in R3), so the sleeve should keep both, broad and short.

## 7. Does replacing bonds help? — regime by regime

Net-of-fee annualised return, AP5 vs replacement steps (fig. 04; full 0–100% grid in
`analysis/`):

| Regime | AP5 | 20% | 50% | 100% | Read |
|---|---|---|---|---|---|
| R1 2008–14 (bonds strong) | **3.6** | 3.6 | 3.4 | 3.0 | replacement **costs** you |
| R2 2015–22 (negative) | 4.0 | 4.5 | 5.1 | **6.1** | replacement **wins** |
| R3 2022–24 (hikes) | 3.1 | 2.8 | 2.7 | 2.8 | roughly **neutral** |
| R4 2024–26 (easing) | 5.1 | 5.9 | 6.9 | **8.3** | replacement **wins** |

Full period, net of fees (selected steps):

| Book | CAGR | Vol | Sharpe | MaxDD | CVaR₉₅ |
|---|---|---|---|---|---|
| AP5 (0%) | 3.43% | 7.8% | 0.47 | −20.6% | −5.2% |
| Replace 20% | 3.72% | 8.1% | **0.49** | −21.8% | −5.6% |
| Replace 50% | 3.95% | 8.8% | 0.48 | −24.1% | −6.1% |
| Replace 100% | 4.30% | 10.1% | 0.47 | −27.7% | −7.0% |

**The honest headline:** over the full 2008–2026 cycle, replacing bonds adds **return but
proportional risk** — Sharpe is essentially flat (it peaks only mildly, ~0.49 around a **20–40%**
replacement, then fades) while drawdown worsens steadily to −27.7% at full replacement. There is
**no free lunch across the whole sample**; the value of replacement is **conditional on the
regime** — strongly positive in the negative-rate (R2) and easing (R4) regimes, neutral in
hikes (R3), negative only when bonds do their job (R1).

## 8. Basket construction matters — curated vs naïve (fig. 08)

The naïve basket carries the two money-losers (commodities, managed futures). A **curated**
basket that drops them and tilts to defensive carry + a gold hedge dominates it at every step:

| Book (100% replaced) | CAGR | Vol | Sharpe | MaxDD |
|---|---|---|---|---|
| AP5 benchmark | 3.43% | 7.8% | 0.47 | −20.6% |
| Naïve basket | 4.30% | 10.1% | 0.47 | −27.7% |
| **Curated** (HY 35 / EM 30 / gold 20 / infra 15) | **4.91%** | 10.1% | **0.53** | −27.5% |

The curated basket lifts Sharpe **above** the AP5 benchmark at every step, where the naïve one
did not — the replacement result is **as much about *which* alternatives as *how much*.**

## 9. Recommendation

- **Do not replace the bond sleeve wholesale.** Full replacement buys ~0.9%/yr of return for
  ~7pp more drawdown and no Sharpe gain over the cycle.
- **A partial replacement (≈ 20–40%) is the balanced choice**: it sits at the mild Sharpe peak,
  captures the regime upside (R2/R4), and keeps a bond core for flight-to-quality (R1).
- **Keep the sleeve's structure** — both Swiss and world, both broad and short-duration (the
  short tranche is what absorbs rate shocks).
- **Curate the basket** — a defensive carry + hedge basket beats the naïve equal-weight one.

## Appendix A. Optimisation (secondary / theoretical)

Kept out of the headline at the director's request. Optimising the 42% sleeve in-sample over
2008–2026 (core fixed, realistic caps; `src/appendix_optimization.py`), net of fees:

| Optimised sleeve | CAGR | Vol | Sharpe | MaxDD | Sleeve holds |
|---|---|---|---|---|---|
| Min-variance | 3.20% | 7.7% | 0.45 | −20.8% | **100% short world bonds** |
| Min-CVaR | 3.20% | 7.7% | 0.45 | −20.8% | **100% short world bonds** |
| Max-Sharpe | 4.31% | 8.2% | **0.56** | −19.7% | 30% Swiss bonds + 12% gold (cap) |

The message reinforces the main analysis: given full hindsight, the risk-minimisers put the
sleeve entirely into the **safest bond tranche** (short-duration world bonds), and the
return-maximiser keeps a large Swiss-bond position plus a capped gold hedge — **no optimiser
abandons bonds**. These weights are in-sample and optimistic; a descriptive upper bound, not a
rule, which is why the analysis leads with the transparent step/curated books.

## 10. Caveats

Investable ETF/fund proxies (not the exact VZ funds); monthly frequency understates intra-month
drawdowns; foreign equity is a USD price index converted to CHF TR (cancels in comparisons,
validated at 0.955 corr); convertibles start 2009 and the short world-bond index is spliced
pre-2010; commodity/CTA proxies carry real tracking error; single historical path. See
`docs/methodology.md`. Academic reproduction, not investment advice.
