# Legacy — exploratory 2019–2026 study (NOT used in the thesis results)

These files are the **earlier** exploratory project and are kept only for history. They are
**not part of the canonical 2008–2026 thesis pipeline** and must not be cited as results.

- `config.py`, `portfolios.py` — the old 2019–2026 setup with a **low-rate threshold**
  (SNB ≤ +0.25%) and CLO / ILS / private-credit portfolios. This framing was **abandoned**
  when the thesis moved to a whole-period, regime-by-regime analysis.
- `download_data.py`, `run_analysis.py` — the old Yahoo daily pipeline.
- `walkforward.py`, `montecarlo.py` — walk-forward / bootstrap on the **old** daily 13-asset
  universe (different dataset and design; their numbers, e.g. a ~0.81 walk-forward Sharpe, are
  **not comparable** to the main study and should not be quoted alongside it).
- `synth_ils.py` — a **synthetic** ILS series. ILS is *excluded* from the thesis precisely
  because it lacks an investable history; this file is retained only to document that the
  synthetic series never entered the final analysis.

The canonical study lives in `src/` (`config_main.py`, `data_bloomberg.py`,
`data_alternatives.py`, `build_panel.py`, `analysis_2008.py`, `robustness.py`,
`appendix_optimization.py`, `figures_fr.py`) with tests in `tests/`.
