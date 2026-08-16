# Thesis structure guidance (aligned to the current 2008–2026 study)

How to turn the empirical results in this repo into the written MSc dissertation. The
*empirical* work is done (`reports/thesis_report.md`); this is the academic scaffolding the
author writes around it. All numbers come from `analysis/results_manifest.json`.

## Research question

*Which functions of the AP5 bond sleeve — return, carry/income, diversification, liquidity,
flight-to-quality, duration — can a diversified set of investable alternatives reproduce, and
at what risk cost, across SNB rate regimes over 2008–2026?* Bonds are a problem both when
rates are **low** (negative-rate era, ≈0 return) and when they **rise** (duration losses), so
the analysis is read regime-by-regime rather than via a contested "low-rate threshold".

## Hypotheses (state which are supported)

- **H1** Partial replacement raises long-run return. → **supported** (monotonic).
- **H2** Full replacement raises downside risk vs AP5. → **supported & statistically reliable**
  (P(worse drawdown) ≈ 91%).
- **H3** The effect is regime-dependent. → **supported** (sign flips across regimes / crisis type).
- **H4** Partial beats full on the return–risk trade-off. → **qualified**: partial is the better
  *compromise*, but Sharpe differences are **within bootstrap noise** — no unique optimum.

## Suggested chapter structure

1. **Introduction** — the low-rate/negative-rate CHF problem; the VZ AP5 case; research question.
2. **Literature review** *(author writes)* — bond return decomposition & duration;
   low/negative-rate environments; strategic asset allocation & diversification; the
   alternatives (gold, commodities, infrastructure, HY, EM debt, managed futures, convertibles);
   downside risk (CVaR); regime dependence. Cite sources for every factual claim.
3. **Theoretical framework** — the six functions of bonds; what each alternative can/can't proxy
   (duration substitute vs income substitute vs inflation hedge vs crisis diversifier).
4. **Data** — Bloomberg constituents, SNB/Fed rates, VZ NAV; see `docs/data_dictionary.md` and
   `docs/source_register.md`.
5. **Methodology** — `docs/methodology.md` (granular AP5, band assumption + sensitivity, fees,
   currency/hedge approximation, cash proxy, regimes); `docs/assumptions.md` register.
6. **Reconstruction & validation of AP5** — stylised benchmark; corr 0.955, β 0.97/α −0.35%/R² 0.91.
7. **Bond performance across rate regimes** — the R1–R4 table; broad vs short duration.
8. **Bond-replacement portfolios** — the **trade-off curve** (0–100% in 10% steps) as the
   primary result; net-of-fee CAGR/vol/Sharpe/MaxDD/CVaR.
9. **Statistical robustness** — bootstrap CIs (ΔSharpe straddles zero; drawdown reliably worse);
   sensitivity matrix (band/cost/hedge/splice); stress table (2020 vs 2022).
10. **Discussion & implementation risk** — per-instrument risks (gold FX/no income; commodities
    roll; infra equity beta; HY/EM spread & correlation; managed-futures dispersion;
    convertibles convexity); why instrument *selection* matters; the ex-post curated caveat.
11. **Conclusion** — favour partial over wholesale replacement; no unique optimum; keep the bond
    core; validate basket selection out-of-sample.
12. **References / Appendices** — optimisation appendix (secondary, in-sample, not independent).

## Checklist (examiner-proofing — mostly done in the repo)

- [x] Real VZ data, granular AP5 composition, validation against the actual NAV.
- [x] Rebalancing band treated as an **assumption** with sensitivity (not "the VZ rule").
- [x] Fees, hedging and cash stated as explicit (approximate) assumptions.
- [x] **Statistical uncertainty** (bootstrap CIs) — do not quote point-estimate Sharpe gaps.
- [x] Excluded assets (ILS, private credit, mortgage funds) justified; no synthetic series used.
- [ ] **Literature review with citations** — author to write.
- [ ] Optionally: a rate-beta decomposition to move the duration claim from "consistent with"
      toward causal; a SARON cash refinement; an out-of-sample basket-selection test.

## Extensions worth a sentence (not required)

Rate-beta/duration regression; SARON-based cash; out-of-sample curated-basket selection;
institutional Swiss-mortgage NAV if VZ can supply one. **Do not** add DCC-GARCH or more
econometric machinery — the priority is consistency and correct inference, not more methods.
