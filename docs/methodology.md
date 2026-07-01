# Methodology

Reproducible pipeline for replicating the VZ **AP5** portfolio with index/ETF proxies,
applying **Smart Rebalancing**, and testing **bond-replacement** strategies over
**01 Jul 2019 → 30 Jun 2026**.

---

## 1. Data

- **Source:** Yahoo Finance chart API (`query1.finance.yahoo.com`), daily
  dividend-adjusted close (= total return), pulled via `requests` through the session's
  egress proxy (`src/download_data.py`). No API key.
- **Base currency:** CHF. Everything is a CHF total-return series.
- **Window:** 1827 business days, 2019-07-01 → 2026-06-30.
- **Proxy map:** `data/proxy_map.csv`. SIX-listed **CHF ETFs** are used wherever possible
  so no FX conversion is needed for the AP5 sleeves.

| Sleeve | Proxy | Native ccy | Notes |
|---|---|---|---|
| Swiss equity | `CHSPI.SW` iShares Core SPI | CHF | SPI total return |
| World equity | `XDWL.SW` Xtrackers MSCI World | CHF | **unhedged** (per PM: equities not hedged) |
| Swiss bonds | `CSBGC0.SW` | CHF | SBI-type CHF bond |
| World bonds | `AGGS.SW` Global Aggregate | CHF | **CHF-hedged** (per PM: bonds hedged) |
| Real estate | `CHSRI.SW` | CHF | SXI Real Estate Funds |
| Cash | synthetic | CHF | SNB policy-rate accrual (SARON proxy) |
| Gold | `ZGLD.SW` ZKB Gold | CHF | physical, CHF-priced |
| Convertibles | `ICVT` | USD→CHF-hedged | iShares Convertible |
| AAA CLO | `JAAA` (+`FLOT` splice) | USD→CHF-hedged | see §4 |
| Infrastructure | `IGF` | USD→CHF-hedged | iShares Global Infra |
| Managed futures | `DBMF` | USD→CHF-hedged | iMGP DBi Managed Futures |
| Private credit | `BIZD` | USD→CHF-hedged | public BDC proxy (see caveat) |
| ILS / cat bonds | synthetic | CHF-hedged | Swiss Re Cat Bond-calibrated (see §5) |

## 2. Currency treatment

The PM confirmed VZ **hedges only the global bond sleeve into CHF**; world equities are
unhedged. We follow this exactly:

- **World equity** → CHF-listed *unhedged* ETF (retains FX exposure a CHF investor bears).
- **World bonds** → CHF-*hedged* ETF (native CHF).
- **USD-native replacement candidates** (convertibles, CLO, infrastructure, managed
  futures, private credit) are modelled as **CHF-hedged share classes**: we keep the
  asset's *local* (USD) total return and add the daily hedge carry `(r_CHF − r_USD)/252`
  from the SNB and USD policy-rate paths (`config.SNB_PATH`, `config.USD_PATH`). This
  removes FX spot moves and retains the **interest-rate-differential hedging cost**.
  - **Finding:** over 2019–2024 USD rates sat far above CHF rates, so this cost ran
    **≈ 3% p.a.**, not the 0.5–1.5% the draft assumed. Currency is a first-order drag on
    USD-market bond replacements for a CHF investor — a central result of the analysis.
- **Gold** via `ZGLD.SW` is CHF-priced physical gold (gold-in-CHF), the standard Swiss
  access route; kept unhedged.

## 3. AP5 strategic allocation

`config.AP5_TARGET` (VZ Anlageprofil 5, VVIA index implementation):
Swiss equity 25% · World equity 25% · Swiss bonds 16.8% · World bonds 25.2% ·
Real estate 5% · Cash 3%. **Total bond sleeve = 42%.**

## 4. AAA CLO history splice

`JAAA` (Janus Henderson AAA CLO) begins 2020-10-19, after our start. The 2019-07 → 2020-10
gap is back-filled with `FLOT` (floating-rate IG) daily returns **dampened to JAAA's own
daily volatility** (keeps FLOT's trend, compresses its March-2020 liquidity dislocation
from ~−12% to an AAA-CLO-realistic ~−4%; the draft cites 3–5%). Documented in
`src/download_data.py`; pre-2020-10 CLO is a proxy, not a live track record.

## 5. Synthetic series

- **Cash:** compounds the SNB policy-rate path (daily accrual `rate/360`); captures the
  2019–2022 negative-rate drag on the 3% liquidity sleeve.
- **ILS:** no daily-liquid long-history ETF exists, so `src/synth_ils.py` builds a
  **transparent, seeded** series calibrated to the Swiss Re Global Cat Bond Index:
  risk-free + ~4.5% premium, low day-to-day vol (~3% annualised), with discrete
  **catastrophe drawdowns** (Hurricane Ian, Sep 2022 ≈ −11.5%) and the record 2023
  (+19.7%) / 2024 (+17%) years. **This is a calibrated model, not a realised return.**

## 6. VZ Smart Rebalancing engine (`src/engine.py`)

- Hold units of each sleeve's total-return index; weights drift with prices.
- **Smart (bandwidth) mode:** at each monitoring date (month-end, base case) check whether
  any sleeve's weight has left its **relative tolerance band** `[w*(1−b), w*(1+b)]`. If
  any breaches, **rebalance the whole book to target** (the VZ slide-12 snap-back). Base
  band **b = ±20% relative** (slide shows ±8% relative on equity as a minimum; widened to
  a defensible institutional default and stress-tested at ±10%/±30%).
- **Comparison modes:** calendar quarterly / annual, buy-and-hold.
- **Regime switching:** a `target_schedule` lets the target book change with the rate
  regime; a regime change forces a rebalance (used by the dynamic P4/P5 books).
- **Transaction costs:** 10 bps one-way on traded turnover.

### Rebalancing sensitivity (AP5 benchmark)
| Policy | CAGR | Vol | Sharpe | MaxDD | # rebal | turnover |
|---|---|---|---|---|---|---|
| Smart ±20% (base) | 4.99% | 8.5% | 0.61 | −18.5% | 2 | 12% |
| Smart ±10% | 4.98% | 8.5% | 0.61 | −18.5% | 7 | 25% |
| Smart ±30% | 5.16% | 8.8% | 0.62 | −18.5% | 1 | 12% |
| Calendar quarterly | 4.92% | 8.3% | 0.62 | −18.0% | 28 | 41% |
| Calendar annual | 4.90% | 8.3% | 0.61 | −18.0% | 8 | 22% |
| Buy & hold | 5.53% | 9.1% | 0.63 | −18.5% | 0 | 0% |

Over this equity-bull window buy-and-hold edged the rebalanced books (letting equities run
paid off); Smart Rebalancing delivers the *same* Sharpe at **a fraction of the turnover**
of calendar rebalancing — its real value is discipline and cost control, not extra return.

## 7. Optimisation (`src/optimize.py`)

Long-only, box + group-budget constrained. The AP5 equity/real-estate/cash **core (58%)
is held fixed**; only the **42% bond sleeve** is reallocated across Swiss bonds, world
bonds and the 7 replacements — matching the mandate. Caps encode liquidity/prudence:
gold ≤8%, convertibles ≤5%, CLO ≤15%, infra ≤10%, managed futures ≤8%, ILS ≤5%, private
credit ≤3%, and **(ILS + private credit) ≤5%** total illiquid.

Objectives: `max_sharpe`, `min_variance`, `min_cvar` (95%), `risk_parity`,
`max_return_capvol`. Two corrections from the draft's caveats are applied to risk inputs:

1. **Dimson-adjusted volatility** for smoothed/illiquid assets (private credit, ILS):
   regress on contemporaneous + 2 lagged market returns, scale observed vol by the
   true/contemporaneous beta ratio — recovers understated risk.
2. **CVaR objective** for fat-tailed assets, since mean-variance understates ILS
   catastrophe tails and private-credit smoothing.

> **In-sample caveat.** `max_sharpe` is fitted to what worked in 2019–2026 (gold, managed
> futures, CLO) and its Sharpe (~0.90) is optimistic/overfit. The **min-variance** and
> **min-CVaR** books are far more stable across estimation windows and are the ones we
> carry forward as *robust* recommendations.

## 8. Metrics & stress tests

- Per portfolio: CAGR, annualised vol, Sharpe, Sortino, max drawdown + duration, Calmar,
  VaR/CVaR 95% & 99%, turnover.
- **Crisis windows:** COVID crash (2020-02-19→03-23) & recovery, 2022 rate shock
  (2022-01→10), SVB bank stress (Mar-2023), plus the full period. Results in
  `analysis/stress_windows.csv`.

## 8b. Robustness: out-of-sample & Monte Carlo

- **Walk-forward** (`src/walkforward.py`): expanding-window, look-ahead-free optimisation.
  Initial 24-month burn-in, re-estimate every 6 months on all data up to that date, apply
  to the next unseen block (reusing the engine's `target_schedule`). OOS window
  2021-07 → 2026-06. We report OOS metrics and the **in-sample-vs-OOS Sharpe gap** against a
  full-sample look-ahead optimum (the "cheating" upper bound). Outputs:
  `analysis/walkforward_*.csv`, figures 08–09.
- **Block-bootstrap Monte Carlo** (`src/montecarlo.py`): stationary bootstrap (Politis-Romano;
  geometric blocks, mean ≈ 20 trading days) resampling **whole return rows jointly** to
  preserve cross-asset correlation, into **3,000 synthetic 7-year paths**. Portfolios are
  evaluated **constant-mix** (daily-rebalanced) — a path maps to portfolio returns by a
  matrix product; calendar/regime books (P4/P5, walk-forward) are excluded because bootstrap
  shuffling destroys their time alignment. We report percentile distributions of
  CAGR/vol/Sharpe/MaxDD and **P(beat AP5 benchmark)**. Outputs:
  `analysis/montecarlo_*.csv`, figures 10–12.

## 9. Reproduce

```bash
pip install pandas numpy scipy matplotlib requests
export REQUESTS_CA_BUNDLE=/root/.ccr/ca-bundle.crt SSL_CERT_FILE=$REQUESTS_CA_BUNDLE
python src/download_data.py      # -> data/processed/*.csv
python src/run_analysis.py       # -> analysis/*.csv, reports/figures/01-07*.png
python src/walkforward.py        # -> analysis/walkforward_*.csv, figures 08-09
python src/montecarlo.py         # -> analysis/montecarlo_*.csv, figures 10-12
```

## 10. Known limitations

1. Index/ETF **proxies**, not the exact VZ instrument line-up; sub-sleeve splits (SLI/SPI
   Extra, EM, small caps, bond maturity buckets) are collapsed to one proxy per sleeve.
2. **ILS and pre-2020 CLO are modelled series** — clearly labelled; treat their standalone
   stats as illustrative.
3. **Private credit** uses a listed BDC proxy (`BIZD`): daily-liquid and volatile, the
   *opposite* of true direct-lending's smoothed NAV. It brackets the honest truth — real
   private credit's low reported vol is a smoothing artefact (see Dimson adjustment).
4. Single historical path (2019–2026). No Monte-Carlo/bootstrap resampling yet (a natural
   thesis extension).
5. Hedge carry uses stepwise policy-rate paths, not realised OIS/forward points.
