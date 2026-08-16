# Assumptions register

Every non-trivial modelling choice, its status (observed fact vs assumption), and how it is
tested. Base-case values live in `src/config_main.py`.

| # | Assumption | Status | Base | Tested by |
|---|---|---|---|---|
| A1 | AP5 index composition (SPI/SLI/… weights) | **Observed** (VZ slide 5) | slide values | — |
| A2 | Strategic weights held fixed back to 2008 | Assumption (director) | fixed | counterfactual by design |
| A3 | Rebalancing = band monitoring, not calendar | **Observed** (VZ doc/PM) | — | — |
| A4 | Band **width** (general rule) | **Assumption** (slide shows only ±8% at 50%) | ±20% rel | band grid ±5/8/10/15/20% |
| A5 | Only bonds hedged to CHF (AP5 core) | **Observed** (PM email) | hedged | — |
| A6 | HY/EM replacements hedged to CHF | **Assumption** | hedged | hedged vs unhedged variant |
| A7 | CHF hedge = policy-rate-implied approximation | Assumption | (r_CHF−r_USD)/12 | (ignores fwd points/basis) |
| A8 | Foreign-equity CHF TR = USD price × FX + fixed div | Assumption | div 2.1%/2.6% ex-ante | validation regression |
| A9 | Cash = SNB policy-rate proxy, full pass-through | Assumption | snb/12 | (SARON refinement noted) |
| A10 | Fee load 1.37%/yr (0.12%+1.25%) on every book | **Agreed** (director) | 1.37% | fee applied equally |
| A11 | Transaction cost 10 bps one-way | Assumption | 10 bps | cost grid 0/5/10/25/50 |
| A12 | Short world-bond splice pre-2010 (broad→short) | Assumption | splice | re-run from 2010 |
| A13 | Primary basket = equal-weight 6 alts | **Pre-specified** | 1/6 each | — |
| A14 | Curated basket (HY35/EM30/gold20/infra15) | **Ex-post / exploratory** | — | labelled, not used for recommendation |
| A15 | Regime dates (SNB) | **Observed** (SNB decisions) | 4 regimes | — |

Excluded candidates (ILS, private equity/credit, Swiss mortgage funds) and their reasons are
in `docs/methodology.md` §7.
