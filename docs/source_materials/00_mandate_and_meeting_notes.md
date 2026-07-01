# Source Materials — Mandate, Meeting Notes & Client Inputs

This file transcribes and preserves everything supplied by the student (HEC Lausanne
MSc Finance, intern at VZ VermögensZentrum) and the portfolio manager, so the analysis
is fully reproducible from the repo alone.

---

## 1. The mandate (original message from the student)

> Bonsoir,
> j'espère que vous allez bien ! Je suis en master en finance à la HEC Lausanne et
> devrais le finaliser ce semestre on l'espère avec ma thèse. Je réalise en parallèle
> mon stage chez VZ en tant que financial consultant. Je vous contacte, car j'aurai
> besoin d'un peu d'aide pour ma thèse, notamment pour me guider un peu, j'ai un sujet
> assez vaste discuté avec mon directeur qui est le suivant : **les alternatives aux
> obligations dans le cadre de la construction de portefeuille dans un environnement de
> taux bas.**

**Thesis topic (EN):** *Alternatives to bonds in portfolio construction in a low
interest-rate environment.*

### Work requested (from the person mandated to help)

1. **Priority 1 — Replicate the VZ "AP5" portfolio** using the benchmark/index per
   asset class (a mock portfolio built from indices/ETFs), applying VZ's **Smart
   Rebalancing** and the **weight constraints/bands**, over **01 July 2019 → 30 June
   2026** (7 years).
2. Construct **alternative portfolios** using the different **bond-replacement** options
   and compare their performance against the AP5 benchmark portfolio.
3. Run **portfolio allocation/optimization** to find the best allocation weightings.
4. The replacement is **first on the Swiss bond allocation during low-rate periods**,
   then extended to whatever produces the best portfolio.
5. Discuss performance alongside the **classical risks**: liquidity risk, one-man
   (key-person) risk, etc.

---

## 2. The AP5 target portfolio (VZ "Vermögensverwaltung mit Anlageprofil 5")

Reconstructed from the VZ slide "VV avec placements indiciels (VVIA) — Exemple : profil
d'investisseur 5" and the handwritten meeting notes. VVIA = the index-implemented
version of the VZ discretionary mandate. Top-level strategic asset allocation (sums to
100%):

| Asset class (VZ label)            | Target weight | Benchmark / index                                  |
|-----------------------------------|--------------:|----------------------------------------------------|
| Actions Suisse (Aktien Schweiz)   |     **25.0%** | SPI (split on slide: SPI / SLI / SPI Extra)        |
| Actions Monde (Aktien Welt)       |     **25.0%** | MSCI World (+ Small Caps + Emerging Mkts), **unhedged** |
| Obligations CHF (Zinswerte Schweiz)|    **16.8%** | SBI AAA–BBB Domestic (incl. 1–5y bucket)           |
| Obligations Monde (Zinswerte Welt)|     **25.2%** | Bloomberg Global Aggregate, **CHF-hedged**         |
| Immobilier CH (Immo)              |      **5.0%** | SXI Real Estate Funds                              |
| Liquidités (Liq)                  |      **3.0%** | CHF money market / SARON cash                      |

**Total bond sleeve = 16.8% + 25.2% = 42.0%** — the block this thesis attacks.
This matches the LLM draft's "42% bond sleeve" (it rounded to 18% Swiss / 24% World).

Slide sub-splits (as read from the VVIA bars, approximate):
- Aktien Schweiz 25%: SPI ~11%, SLI ~12%, SPI Extra ~2%.
- Aktien Welt 25%: MSCI World ~19%, MSCI World Small Caps ~3%, MSCI EM ~3%.
- Zinswerte Schweiz 16.8%: SBI AAA-BBB ~11%, SBI AAA-BBB 1–5y ~6%.
- Zinswerte Welt 25.2%: Global Aggregate hedged ~ split into all-maturity + 1–5y buckets.
- Immo CH 5%: SXI Real Estate Funds. Liq 3%.

> For the mock replication we implement at the **top-level asset-class weights** using one
> clean total-return index/ETF per sleeve. Sub-splits are documented but not separately
> modelled in the base case (a sensitivity can add them).

### Currency hedging policy (confirmed by the PM — see §4)
- **World bonds: hedged into CHF.** (Slide footnote "*abgesichert in CHF*.")
- **World equities: NOT hedged** (no hedge footnote on the equity bar).
- PM quote: *"we only hedge global bonds into CHF."*

---

## 3. VZ Smart Rebalancing (rebalancing methodology)

From slide 12 ("Fidélité élevée à la stratégie – Le Smart Rebalancing VZ") and the PM email.

- Rebalancing is **bandwidth/threshold-based, NOT calendar-based.** The portfolio is
  rebalanced when an asset-class weight **deviates beyond a predefined tolerance band**
  around its target, not at fixed dates.
- Slide example (equity sleeve, target 50%):
  - **Pondération cible (target): 50%**
  - **Limite supérieure (upper hard limit): 54%**  → +4 pts absolute (= +8% relative)
  - **Limite inférieure (lower hard limit): 46%**  → −4 pts absolute (= −8% relative)
  - Inner dashed trigger lines shown at ~48% and ~52%.
  - Labelled events:
    - **A** — equity share drifts **up** in a positive market (passive drift).
    - **B** — equity share **reduced** because deviation from target too large (trim).
    - **C** — equity share drifts **down** in a negative market (passive drift).
    - **D** — equity share **increased** because deviation from target too large (top-up).
- PM email quote: *"VZ Smart Rebalancing is primarily based on predefined bandwidths.
  This means that the portfolio is not rebalanced at fixed time intervals, but rather
  when allocations deviate from their target weights beyond certain thresholds."*
- Meeting note: *"Réallocation vs les 3 mois"* → interpreted as **monitoring roughly
  quarterly** (band checked on a schedule; trade only if breached). We implement monthly
  monitoring as the base case and test quarterly as a robustness variant.
- **Evaluation & conclusion (slide):** continuous monitoring + upper/lower fluctuation
  band per asset class ensures rigorous adherence to the strategy.

### Our implementation of Smart Rebalancing (documented assumption)
- Each asset class has target `w*` and a **relative tolerance band** (base case **±20%
  relative**, i.e. trigger if weight leaves `[0.8·w*, 1.2·w*]`; e.g. 25% → [20%,30%],
  16.8% → [13.4%,20.2%]). This mirrors the slide's ±8% relative on equities as a *minimum*
  and is widened to a defensible institutional default; band width is a parameter and is
  stress-tested.
- On any breach at a monitoring date, **rebalance the whole portfolio back to target
  weights** (full reset — the VZ chart shows a return toward the target line).
- Comparison scenarios: (i) calendar quarterly, (ii) calendar annual, (iii) buy-and-hold
  (no rebalancing), (iv) band width sensitivity.

---

## 4. Portfolio manager email (Merel → Erta) — verbatim

> Hi Erta,
> Thank you for your message.
>
> **Regarding the rebalancing:**
> VZ Smart Rebalancing is primarily based on predefined bandwidths. This means that the
> portfolio is not rebalanced at fixed time intervals, but rather when allocations
> deviate from their target weights beyond certain thresholds. I've attached the
> "Kundendoku", which explains this mechanism in more detail on slide 12.
>
> **On your second point:**
> Yes, the columns *"Fondswährung"* and *"Handelswährung"* indicate the fund currency and
> the trading currency. Based on this, your understanding is correct; we only hedge global
> bonds into CHF.
>
> I hope this helps. Let me know if anything is unclear.
> Best regards, Merel

---

## 5. Handwritten meeting notes (GESICA notepad) — transcription

- Header: `2019 → 2008 → 2025   AP5`
- `01/07/19 → 30/06/26 : 7 ans` ; `2022 → Fin Juin 2026`
- `→ Réallocation vs les 3 mois` (rebalancing / quarterly check)
- `2008` stress-test box (apply a GFC-style shock).
- `AP5: 25% Swiss ; 25% World (hedged?) ; (12.5% USD)` — note: PM later clarified only
  **bonds** are hedged; the "12.5% USD" is the student's own note on residual USD exposure.
- `16.8% Bond Swiss` ; world bonds `25.2%` ; `Immo` ; `Liq 3%`.
- `2008 → VZ Smart Rebalancing`.
- `L2 / Python → Portfolio optimisation → Definition [benchmark]`.
- Metrics to report: `Max Drawdown, Vol, Sharpe ratio`.
- Stress list referenced: France / Italy / others (regional equity references).

### Interpretation for the build
1. Backtest window **01/07/2019 → 30/06/2026**.
2. Replicate AP5 with indices, apply Smart Rebalancing + bands.
3. Overlay a **2008-style stress scenario** on the current portfolio (historical GFC
   returns applied to the sleeves) in addition to the in-sample 2020 & 2022 stress.
4. Deliverables: performance stats (return, vol, Sharpe, Sortino, **max drawdown**),
   plus optimization in Python.

---

## 6. LLM first-draft report (archived docx)

`LLM_first_draft_bond_replacement_analysis.docx` — treat as a **qualitative first draft**,
not ground truth. Its seven bond-replacement candidates (ranked by liquidity) frame our
investable candidate set:

1. Gold  2. Convertible bonds  3. Senior AAA–AA CLO tranches  4. Listed infrastructure
5. Managed futures / CTAs  6. Insurance-Linked Securities (ILS / cat bonds)  7. Private
credit / direct lending.

Its numeric return/vol/correlation figures are *assumptions*; this project replaces them
with **realised data** over 2019–2026 where an investable proxy exists, and flags the
draft's three methodological caveats (regime-dependent covariance, non-Gaussian tails,
CHF hedging cost).

## 7. Reference article (archived pdf)

`nuveen_fixed_income_strategies_low_rising_rates_2018.pdf` (Nuveen / Brian Nick, Winter
2018) — "Fixed-income strategies for low and rising rates." Institutional-investor framing
of the same problem, focused on *within-fixed-income* diversifiers (EM debt, high yield,
floating-rate loans, preferred securities, middle-market senior loans, mezzanine debt).
Useful correlation/return tables (Figures 3–6) and the core thesis that **low yields, not
rising rates, are the more serious long-term risk** — directly supportive of the thesis.
