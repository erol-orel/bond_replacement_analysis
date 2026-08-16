# Alternatives to bonds in a low-rate environment — empirical foundation (2008–2026)

**HEC Lausanne · MSc Finance thesis · CHF, monthly total return, net of fees**

> Reframed brief (agreed with the thesis director, Aug 2026): find **alternatives to the
> bond sleeve** and replace it **over the whole 2008–2026 period**, then read the results
> **regime by regime**. The bond problem is not only low rates — when rates *rise* bonds
> also lose — so the analysis must comment on bond behaviour across *every* SNB regime, not
> only the low-rate windows. This removes the need for a contested "low-rate threshold".

---

## 1. What this is

An empirical replication of the **VZ AP5** mandate (VZ Säule 3a mit ETF, *Anlegerprofil 5*)
built from the **Bloomberg constituent indices** the analyst obtained, extended back to
**January 2008** and run with **VZ Smart Rebalancing**. The 40.75% bond sleeve is then
replaced — in steps of 0 / 33 / 66 / 100% — by a diversified basket of **investable
alternatives**, and every portfolio is measured **net of the agreed fee load** across the
four SNB rate regimes.

Everything is reproducible:
`python src/data_bloomberg.py && python src/data_alternatives.py && python src/build_panel.py && python src/analysis_2008.py`

## 2. Data (real, not synthetic)

| Block | Source | Notes |
|---|---|---|
| AP5 constituents | **Bloomberg** (`data/bloomberg/`) | SBI AAA-BBB (Swiss bonds), Bloomberg Global Aggregate **CHF-hedged** (world bonds), SPI (Swiss equity), MSCI World (foreign equity), SXI Real Estate Funds — monthly CHF total return from 2008 |
| Policy rates | **SNB + Fed** | monthly, used for regimes, the CHF cash index and hedge carry |
| Real VZ AP5 track | **VZ** (VVIA) | actual product NAV 2019–2026 — used to **validate** the reconstruction |
| Allocation history | **VZ** | the real AP5 target and its drift 2017–2026 |
| Alternatives | investable ETF/fund proxies | see §5 — the *replaceable, net-of-fee* instruments the director asked for |

Foreign equity is a Bloomberg *price* index in USD; it is converted to a CHF total-return
proxy (× USD/CHF, plus a constant dividend yield). Because the equity/real-estate/cash
**core is identical in every portfolio compared**, this proxy cancels in all AP5-vs-
replacement contrasts; it only matters for the validation, where it performs well (§4).

## 3. Method

- **Strategic AP5 target** (current VVIA, `Consolidation_allocations.xlsx`): foreign equity
  26.25%, Swiss equity 25%, real estate 5%, **world bonds 23.95%, Swiss bonds 16.8%**
  (bond sleeve = **40.75%**), cash 3%. Applied unchanged back to 2008 per the director.
- **VZ Smart Rebalancing** (`engine.py`): predefined **±20% relative bands**, monthly
  monitoring; the book snaps back to target only when a sleeve leaves its band (confirmed by
  the VZ *Kundendoku* slide and the PM's email). 10 bps one-way transaction cost.
- **Fees**: a constant **1.37%/yr** load = **0.12% product + 1.25% management** (the figures
  agreed with the internship director), applied as a monthly drag to every portfolio.
- **Replacement by steps** (no need to justify the steps): move 0 / 33 / 66 / 100% of the
  40.75% bond sleeve into the diversified basket; the equity/RE/cash core stays fixed.

## 4. Validation — the reconstruction is real

Reconstructed AP5 (indices → Smart Rebalancing → net of fees, using VZ's **real allocation
drift** for the validation window) vs the **actual VZ VVIA track record**, 2019–2026 (85
months, fig. 02):

| | value |
|---|---|
| Correlation of monthly returns | **0.95** |
| Annualised tracking error | **2.5%** |
| Mean absolute monthly gap | 0.5% |
| Total return: reconstruction vs real VZ | +24.9% vs +21.1% |

**Is 2.5%/yr tracking error acceptable?** Yes, for this purpose. Context: a passive index
fund tracks its benchmark at ~0.1–0.5%/yr; an *active* fund runs 2–6%/yr; a **proxy
reconstruction that uses different instruments** (public index series, not VZ's exact
CHF-share-class ETFs) and public data sits naturally in the 2–3% range. We decomposed it:
the residual is **not** tactical drift (using VZ's real allocation path only moved it
2.7% → 2.5%) — it is the **foreign-equity leg**, a USD *price* index converted with spot FX
and a constant dividend, standing in for 51% of the book. Two things make this immaterial to
the thesis: (i) the equity/RE/cash **core is identical in AP5 and in every replacement
book, so this proxy error cancels exactly in all comparisons**; (ii) the reconstruction
still reproduces AP5's *dynamics* — correlation 0.95 and a visual match through COVID, the
2022 sell-off and the recovery. That is all the validation needs to do: license extending
the same machinery back to 2008.

## 5. The alternatives (investable, long-history, net-of-fee)

Equal-weight basket of the **six** instruments with a clean investable history to 2008
(convertibles start 2009 and are analysed separately). Descriptive statistics 2008–2026:

| Instrument (proxy) | Role | CHF FX | CAGR | Vol | Sharpe | MaxDD |
|---|---|---|---|---|---|---|
| Swiss bonds *(SBI AAA-BBB)* | *sleeve replaced* | — | 1.8% | 3.6% | 0.51 | −15.9% |
| World bonds *(Global Agg, hedged)* | *sleeve replaced* | CHF-hedged | 1.1% | 3.5% | 0.32 | −18.5% |
| Gold *(GLD)* | crisis hedge | unhedged | 6.2% | 16.3% | 0.45 | −38.0% |
| Commodities *(DBC)* | inflation | unhedged | −1.6% | 18.9% | 0.01 | −75.7% |
| Infrastructure *(IGF)* | real income | unhedged | 3.7% | 14.8% | 0.32 | −45.0% |
| Managed futures *(RYMFX)* | crisis-alpha | unhedged | −0.7% | 13.8% | 0.02 | −47.1% |
| High yield *(HYG)* | credit carry | CHF-hedged | 3.7% | 10.3% | 0.41 | −29.5% |
| EM debt *(EMB)* | credit carry | CHF-hedged | 3.3% | 11.5% | 0.34 | −28.5% |
| *Convertibles (CWB, from 2009)* | hybrid | unhedged | 10.0% | 12.6% | 0.82 | −24.0% |

Only fixed-income-like replacements (HY, EM debt) are **CHF-hedged**, mirroring VZ's rule
that *only bonds are hedged to CHF* (PM email). Honest note: **commodities and managed
futures lost money outright over 2008–2026** — they diversify but are not free; the basket
carries them at equal weight so results are not cherry-picked.

## 6. The core problem, seen regime by regime

The bond sleeve's own annualised return in each SNB regime (fig. 05) — this is the problem
the thesis targets, and it is **not** confined to low rates:

| SNB regime | Swiss bonds | World bonds | Cash |
|---|---|---|---|
| **R1 2008–14** low positive | **+4.0%** | **+4.1%** | +0.5% |
| **R2 2015–22** negative | **−0.8%** | **−0.6%** | −0.8% |
| **R3 2022–24** hikes & plateau | +2.9% | **−2.0%** | +1.2% |
| **R4 2024–26** easing | +2.4% | −0.3% | +0.5% |

Bonds delivered their defensive premium **only when rates fell (R1)**. In the negative-rate
era (R2) the whole fixed-income + cash sleeve earned **≈ 0 or less**; when rates *rose* (R3)
world bonds **lost 2%/yr** on duration. Swiss bonds were more resilient than world bonds in
R3 — the two are correlated (**0.79**) but **not redundant**, so the sleeve should keep both
rather than collapse to a single index.

## 7. Does replacing bonds help? — regime by regime

Net-of-fee annualised return, AP5 vs replacement steps (fig. 04):

| Regime | AP5 | 33% | 66% | 100% | Read |
|---|---|---|---|---|---|
| R1 2008–14 (bonds strong) | **4.0** | 3.8 | 3.4 | 3.1 | replacement **costs** you |
| R2 2015–22 (negative) | 4.4 | 5.0 | 5.7 | **6.3** | replacement **wins** |
| R3 2022–24 (hikes) | 2.8 | 2.9 | 2.9 | 2.9 | roughly **neutral** |
| R4 2024–26 (easing) | 5.2 | 6.3 | 7.4 | **8.4** | replacement **wins** |

Full period, net of fees:

| Book | CAGR | Vol | Sharpe | MaxDD | CVaR₉₅ |
|---|---|---|---|---|---|
| AP5 benchmark | 3.74% | 7.9% | **0.51** | −19.3% | −5.2% |
| Replace 33% | 4.03% | 8.5% | 0.51 | −22.0% | −5.8% |
| Replace 66% | 4.25% | 9.2% | 0.50 | −24.5% | −6.4% |
| Replace 100% | 4.47% | 9.9% | 0.49 | −26.8% | −7.0% |

**The honest headline:** over the *full* 2008–2026 cycle, replacing bonds adds **return but
proportional risk** — Sharpe is essentially flat (0.51 → 0.49) and drawdown worsens by
~7.5pp at full replacement. There is **no free lunch across the whole sample**. The value of
replacement is **conditional on the regime**: it is strongly positive precisely in the
regimes the thesis cares about (negative rates R2, easing R4), neutral during hikes (R3),
and negative only when bonds do their job (falling rates, R1).

## 8. Recommendation

- **Do not replace the bond sleeve wholesale.** Full replacement buys 0.7%/yr of return for
  7.5pp more drawdown and no Sharpe gain over the cycle.
- **A partial replacement (≈ 33–66%) is the balanced choice**: it captures most of the
  regime upside (R2/R4) while limiting the drawdown penalty, and it keeps a bond core for
  the flight-to-quality regimes (R1-type falling-rate shocks).
- **Keep both bond sub-indices.** Swiss and world bonds diverge in the hiking regime and are
  only 0.79 correlated — the sleeve is not reducible to one index.
- **Mind the weak diversifiers.** Equal-weighting commodities and managed futures (both
  negative over the sample) drags the basket; a curated basket (gold + credit + real income)
  would likely dominate the naïve one — a natural robustness extension.

## 8b. Basket construction matters — curated vs naïve (fig. 08)

The naïve basket equal-weights all six alternatives, including the two that **lost money**
over 2008–2026 (commodities −1.6%, managed futures −0.7%). A **curated** basket that drops
those two and tilts toward the defensive credit carry plus a gold hedge — the instruments
that actually resemble a *bond* replacement — dominates it at every step (net of fees):

| Book | CAGR | Vol | Sharpe | MaxDD |
|---|---|---|---|---|
| AP5 benchmark | 3.74% | 7.9% | 0.51 | −19.3% |
| Replace 100% — **naïve** (equal-weight 6) | 4.47% | 9.9% | 0.49 | −26.8% |
| Replace 100% — **curated** (HY 35 / EM 30 / gold 20 / infra 15) | **5.00%** | 9.9% | **0.55** | −26.6% |

The curated basket lifts Sharpe **above** the AP5 benchmark (0.55 vs 0.51) at every
replacement step, where the naïve basket did not. Lesson for the thesis: the replacement
result is **as much about *which* alternatives as about *how much*** — a point worth making
explicitly, and a natural place to note that even the curated basket still carries more
drawdown than the bond core, so a partial replacement remains the balanced call.

## Appendix A. Optimisation (secondary / theoretical)

Kept out of the headline at the director's request. If one optimises the 40.75% sleeve
in-sample over 2008–2026 (equity/RE/cash core fixed, across bonds + the six alternatives,
realistic caps; `src/appendix_optimization.py`), net of fees:

| Optimised sleeve | CAGR | Vol | Sharpe | MaxDD | Sleeve holds |
|---|---|---|---|---|---|
| Min-variance | 3.61% | 7.9% | 0.49 | −19.5% | **100% world bonds** |
| Min-CVaR | 3.61% | 7.9% | 0.49 | −19.5% | **100% world bonds** |
| Max-Sharpe | 4.56% | 8.2% | **0.59** | −18.4% | 29% Swiss bonds + 12% gold (cap) |

The message reinforces the main analysis rather than competing with it: given free rein and
full hindsight, the risk-minimising optimisers **keep the sleeve entirely in bonds**, and
the return-maximising one keeps a large Swiss-bond position plus a capped gold hedge — *no
optimiser abandons bonds wholesale*. These weights are **in-sample and optimistic** (they
see the whole path); they are a descriptive upper bound, not an implementable rule, which is
exactly why the analysis leads with the transparent step/curated books instead.

## 9. Caveats

Investable ETF/fund proxies (not the exact VZ funds); monthly frequency understates
intra-month drawdowns; foreign equity is a USD-price index converted to CHF TR (cancels in
comparisons, validated at 0.94 corr); convertibles start 2009; commodity/CTA proxies bear
real tracking error to institutional vehicles; single historical path. Portfolio
optimisation is deliberately kept as a **secondary/appendix** exercise (the director judged
it too theoretical to headline). Academic reproduction, not investment advice.
