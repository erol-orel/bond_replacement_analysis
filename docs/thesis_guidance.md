# Thesis Guidance — structuring the MSc dissertation

The mandate was partly *"me guider un peu"*. This note turns the empirical work in this
repo into a defensible academic dissertation. Topic: **Alternatives to bonds in portfolio
construction under a low-rate regime**, using the VZ AP5 mandate as the case study.

## 1. Framing / research questions

Narrow the "vast" topic your director flagged into 2–3 testable questions:

- **RQ1 (descriptive):** In a CHF balanced mandate, how much return and diversification
  did the 42% AAA–BBB bond sleeve actually cost/provide over 2019–2026?
- **RQ2 (constructive):** Can liquid/semi-liquid alternatives replace part of that sleeve
  and improve risk-adjusted return *without* worsening crisis drawdowns?
- **RQ3 (conditional):** Does *conditioning the replacement on the rate regime* (replace
  only when rates are low) add value net of turnover and estimation error?

A good thesis answers a **falsifiable** question. "Alternatives are better" is not
falsifiable; "a diversified defensive sleeve raises Sharpe without increasing max drawdown
vs the AP5 bond sleeve" is — and this repo shows it holds (P2 vs P0).

## 2. Suggested chapter structure

1. **Introduction** — the low-rate problem, the CHF/Swiss angle (SNB NIRP 2015–2022,
   return to 0% in 2025), why 42% in ~0%-yielding bonds is the live problem. State RQ1–3.
2. **Literature review** — (a) the low-yield/duration problem (use the archived Nuveen
   2018 piece and its Callan evidence); (b) each alternative asset class; (c) portfolio
   construction under non-Gaussian assets (Markowitz → CVaR, Dimson 1979 smoothing,
   DCC-GARCH). Cite the *four functions* framing (crisis hedge, income, vol-damping,
   liquidity) as your analytical lens.
3. **Data & methodology** — lift from `docs/methodology.md`. Be explicit and honest about
   proxies, CHF hedging, and the synthetic ILS/CLO-splice. Examiners reward transparency
   about limitations far more than they punish the limitations themselves.
4. **The benchmark: replicating AP5** — Smart Rebalancing, band sensitivity, the
   buy-and-hold vs rebalanced result. Establishes your baseline credibly.
5. **Bond-replacement portfolios** — P1–P5: motivate each, present performance + drawdown
   + crisis tables. Lead with the *hedging-cost* and *2022-vs-2020* findings.
6. **Optimisation** — efficient frontier, max-Sharpe/min-var/min-CVaR, Dimson correction.
   Emphasise the **in-sample overfitting caveat** and why you carry min-CVaR forward.
7. **Risk analysis** — the classical-risk register (liquidity, key-person, tail, smoothing,
   currency, concentration). This chapter is what separates an MSc thesis from a backtest.
8. **Conclusion & recommendation** — keep a bond core, diversify the rest; prefer the
   static/robust book over dynamic timing. State limitations and extensions.

## 3. The three findings to build the narrative around

1. **The CHF hedging cost is first-order (~3%/yr, not ~1%).** It reorders the entire
   ranking and is under-appreciated in the (US-centric) literature. This is your original
   contribution — most bond-replacement papers are USD-based and ignore it.
2. **2020 vs 2022 is the crux.** Bonds hedge deflationary/flight-to-quality crashes (2020)
   but *fail* inflationary/rate-shock crashes (2022). No single asset hedges both — the
   answer is a *combination*. This reframes "replace bonds" as "diversify the defensive
   sleeve."
3. **Robust ≻ optimal.** The in-sample max-Sharpe book is a trap; the min-CVaR/static
   diversified book wins once you account for estimation error, turnover, and the
   qualitative risks. Great material for a methodological-humility section examiners love.

## 4. Methodological rigor checklist (to pre-empt examiner questions)

- [ ] Justify proxies; show a robustness run with alternative proxies if time allows.
- [ ] Report **net-of-cost** results and a turnover budget (you have turnover already).
- [ ] Address **look-ahead / in-sample bias** explicitly (walk-forward or at least the
      caveat + min-CVaR choice).
- [ ] Use **CVaR and Dimson-adjusted** risk for the non-Gaussian/smoothed assets — don't
      let a naïve MV optimiser over-allocate to private credit/ILS.
- [ ] Discuss **regime dependence of correlations** (rolling-corr figure; ideally
      DCC-GARCH as an extension).
- [ ] Separate **asset-class risk** from **manager/key-person risk** — crucial for CTAs
      and private credit.
- [ ] State the **Swiss institutional frame** (OPP2/BVG alternative-investment caps) if you
      pitch this for a pension/VZ context.

## 5. Extensions that would raise the grade
- Block-bootstrap / Monte-Carlo to report *distributions* of outcomes, not one path.
- DCC-GARCH conditional covariance and a conditional-CVaR optimisation.
- A formal out-of-sample walk-forward (estimate weights on 2019–2022, test 2023–2026).
- Sensitivity of conclusions to the hedge-cost assumption (the finding most sensitive to
  method).

## 6. On working with VZ / the PM
- The PM confirmed (i) **bandwidth** Smart Rebalancing and (ii) **only bonds are
  CHF-hedged**. Cite this as the authoritative implementation detail and keep the email in
  `docs/source_materials/` as an appendix.
- If you can obtain the actual VZ fund line-up and the "Kundendoku" slide 12, replace the
  proxies for a production-grade replication — but the index-level replication here is the
  correct *academic* approach and is fully reproducible.
