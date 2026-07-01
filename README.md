# Bond Replacement Analysis — VZ AP5 in a low-rate CHF world (2019–2026)

Empirical support for the HEC Lausanne MSc Finance thesis
*"Alternatives aux obligations dans la construction de portefeuille en environnement de
taux bas."* We replicate the VZ **Anlageprofil 5 (AP5)** mandate from index/ETF proxies
with **VZ Smart Rebalancing**, then build, optimise and stress-test **bond-replacement**
portfolios over **01 Jul 2019 → 30 Jun 2026**, in CHF total return.

## TL;DR findings
- The 42% bond sleeve earned ≈0% real over the period (Swiss bonds +0.3%/yr, world bonds
  **−1.9%/yr**) — the thesis problem, confirmed in data.
- **Every** bond-replacement portfolio beat the benchmark on return and Sharpe.
- The clean win is **diversifying the defensive sleeve** (AAA CLO + ILS + gold): Sharpe
  0.61 → 0.72, total return +42% → +51%, **same −18% max drawdown** (portfolio `P2` / the
  min-CVaR optimum `O3`).
- **2022 is the proof**: when bonds and equities fell together, every replacement book lost
  less than the benchmark. **2020 is the caveat**: keep a bond core for flight-to-quality.
- For a CHF investor the **USD→CHF hedge cost ran ~3%/yr** — a first-order, often-ignored
  drag that reorders the ranking of US-market bond substitutes.
- **Robust beats optimal**: the in-sample max-Sharpe book overfits; the min-CVaR / static
  diversified book is the recommendation.

➡️ Full write-up: **[`reports/thesis_report.md`](reports/thesis_report.md)**
· Method: **[`docs/methodology.md`](docs/methodology.md)**
· Thesis structure help: **[`docs/thesis_guidance.md`](docs/thesis_guidance.md)**

## Repo layout
```
src/                 pipeline (pure Python: pandas/numpy/scipy/matplotlib/requests)
  config.py          AP5 allocation, bands, proxy map, rate paths, hedging policy
  download_data.py   Yahoo -> CHF total-return series (data/processed/*.csv)
  synth_ils.py       transparent synthetic ILS (Swiss Re cat-bond calibrated)
  engine.py          VZ Smart Rebalancing + calendar/buy-hold + regime switching + metrics
  portfolios.py      AP5 benchmark + P1–P5 replacement books + rate-regime schedules
  optimize.py        max-Sharpe / min-var / min-CVaR / risk-parity (Dimson + CVaR aware)
  run_analysis.py    master pipeline -> analysis/*.csv + reports/figures/*.png
analysis/            output tables (metrics, weights, stress, frontier, ...)
reports/             thesis_report.md + figures/
docs/                methodology.md, thesis_guidance.md, source_materials/ (mandate,
                     PM email, meeting notes, VZ slides, LLM draft, reference article)
data/                proxy_map.csv, raw/ (per-ticker), processed/ (CHF prices & returns)
```

## Reproduce
```bash
pip install pandas numpy scipy matplotlib requests
export REQUESTS_CA_BUNDLE=/root/.ccr/ca-bundle.crt SSL_CERT_FILE=$REQUESTS_CA_BUNDLE
python src/download_data.py     # pull & build data/processed/*.csv
python src/run_analysis.py      # build analysis/*.csv and reports/figures/*.png
```

## Portfolios
| ID | Name | Idea |
|---|---|---|
| P0 | AP5 benchmark | The mandate, Smart-Rebalanced |
| P1 | Swiss bonds → CLO | Narrow structural swap |
| P2 | Swiss bonds → diversified | CLO + ILS + gold (**recommended static**) |
| P3 | Draft recommended | 7-asset replacement of ~20 pts of the sleeve |
| P4 | Dynamic — Swiss replace | Replace only during low-rate windows |
| P5 | Dynamic — broad replace | Replace Swiss + ½ world bonds when rates low |
| O1/O2/O3 | Optimised | max-Sharpe / min-variance / **min-CVaR** |

## Important caveats
Index/ETF **proxies** (not the exact VZ funds); **ILS and pre-2020 CLO are labelled
synthetic/spliced**; **private credit** uses a listed BDC proxy that shows the *true*
(un-smoothed) economic risk; single historical path (no resampling yet). See
`docs/methodology.md` §10. Not investment advice — an academic reproduction.

## Source materials
Everything the analysis is built on is archived under `docs/source_materials/`: the
mandate + meeting notes, the portfolio manager's email (rebalancing = bandwidths; only
bonds hedged to CHF), the VZ VVIA/AP5 slides, the LLM first-draft report, and the Nuveen
2018 reference article.
