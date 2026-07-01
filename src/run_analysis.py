"""
Master analysis pipeline. Runs every portfolio, optimises the bond-replacement sleeve,
computes performance / risk / stress-test tables, and writes all CSV outputs to
analysis/ and all figures to reports/figures/.

Run:  python src/run_analysis.py
"""
from __future__ import annotations
import os
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from engine import backtest, perf_metrics, metrics_table
from optimize import optimise, cov_matrix
import portfolios as P
from config import AP5_TARGET

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ANL = os.path.join(HERE, "analysis")
FIG = os.path.join(HERE, "reports", "figures")
os.makedirs(ANL, exist_ok=True)
os.makedirs(FIG, exist_ok=True)
plt.rcParams.update({"figure.dpi": 120, "font.size": 9, "axes.grid": True,
                     "grid.alpha": 0.3, "figure.autolayout": True})

CORE = {"swiss_equity": 0.25, "world_equity": 0.25, "real_estate": 0.05, "cash": 0.03}
SLEEVE = ["swiss_bonds", "world_bonds", "gold", "convertibles", "clo",
          "infrastructure", "managed_futures", "ils", "private_credit"]
CAPS = {"gold": (0, 0.08), "convertibles": (0, 0.05), "clo": (0, 0.15),
        "infrastructure": (0, 0.10), "managed_futures": (0, 0.08), "ils": (0, 0.05),
        "private_credit": (0, 0.03), "swiss_bonds": (0, 0.42), "world_bonds": (0, 0.42)}
ILLIQUID_CAP = [(["ils", "private_credit"], 0.05)]

STRESS = {
    "COVID_crash_2020": ("2020-02-19", "2020-03-23"),
    "COVID_recovery_2020": ("2020-03-23", "2020-08-31"),
    "Rate_shock_2022": ("2022-01-01", "2022-10-20"),
    "SVB_bank_stress_2023": ("2023-03-01", "2023-03-24"),
    "Full_2019_2026": ("2019-07-01", "2026-06-30"),
}


def build_optimised_books(rets):
    cols = list(CORE) + SLEEVE
    R = rets[cols]
    cov = cov_matrix(R)
    books, summary = {}, {}
    for obj, label in [("max_sharpe", "O1_opt_max_sharpe"),
                       ("min_variance", "O2_opt_min_variance"),
                       ("min_cvar", "O3_opt_min_cvar")]:
        r = optimise(R, obj, fixed=CORE, bounds=CAPS,
                     group_caps=ILLIQUID_CAP, cov=cov)
        w = {k: v for k, v in r["weights"].items() if v > 1e-4}
        # renormalise tiny numerical residual
        tot = sum(w.values()); w = {k: v / tot for k, v in w.items()}
        books[label] = P._full({k: round(v, 4) for k, v in w.items()}) \
            if abs(sum(w.values()) - 1) < 1e-6 else _normbook(w)
        summary[label] = r
    return books, summary


def _normbook(w):
    tot = sum(w.values())
    w = {k: v / tot for k, v in w.items()}
    full = {k: 0.0 for k in P.UNIVERSE}; full.update(w)
    # fix rounding to exactly 1
    s = sum(full.values())
    kmax = max(full, key=full.get); full[kmax] += 1 - s
    return full


def run_all_portfolios(px, rets):
    books = dict(P.STATIC_BOOKS)
    opt_books, opt_summary = build_optimised_books(rets)
    books.update(opt_books)

    values, weights_end, meta = {}, {}, {}
    for name, book in books.items():
        bt = backtest(px, book, mode="smart", rel_band=0.20)
        values[name] = bt["value"]
        weights_end[name] = book
        meta[name] = dict(n_rebal=bt["n_rebal"], turnover=bt["turnover"])
    for name, kw in P.DYNAMIC_BOOKS.items():
        bt = backtest(px, mode="smart", rel_band=0.20, **kw)
        values[name] = bt["value"]
        meta[name] = dict(n_rebal=bt["n_rebal"], turnover=bt["turnover"])
    return values, weights_end, meta, opt_summary, books


def rebalancing_comparison(px):
    rows = {}
    for mode, kw, tag in [("smart", dict(rel_band=0.20), "Smart band ±20%"),
                          ("smart", dict(rel_band=0.10), "Smart band ±10%"),
                          ("smart", dict(rel_band=0.30), "Smart band ±30%"),
                          ("calendar", dict(monitor_freq="QE"), "Calendar quarterly"),
                          ("calendar", dict(monitor_freq="YE"), "Calendar annual"),
                          ("buyhold", {}, "Buy & hold")]:
        bt = backtest(px, AP5_TARGET, mode=mode, **kw)
        m = perf_metrics(bt["value"])
        rows[tag] = dict(CAGR=m["CAGR"], Vol=m["Vol"], Sharpe=m["Sharpe"],
                         MaxDD=m["MaxDD"], n_rebal=bt["n_rebal"],
                         turnover=bt["turnover"])
    return pd.DataFrame(rows).T


def stress_table(values):
    px = pd.DataFrame(values)
    rows = {}
    for pf in px.columns:
        v = px[pf]
        rows[pf] = {}
        for label, (s, e) in STRESS.items():
            seg = v.loc[(v.index >= s) & (v.index <= e)]
            rows[pf][label] = seg.iloc[-1] / seg.iloc[0] - 1 if len(seg) > 1 else np.nan
    return pd.DataFrame(rows).T


def efficient_frontier(rets, n=40):
    cols = list(CORE) + SLEEVE
    R = rets[cols]; cov = cov_matrix(R)
    mus = R.mean().values * 252
    lo = optimise(R, "min_variance", fixed=CORE, bounds=CAPS,
                  group_caps=ILLIQUID_CAP, cov=cov)
    hi = optimise(R, "max_return_capvol", fixed=CORE, bounds=CAPS,
                  group_caps=ILLIQUID_CAP, cov=cov, target_vol=0.20)
    targets = np.linspace(lo["ann_vol"], hi["ann_vol"], n)
    pts = []
    for tv in targets:
        try:
            r = optimise(R, "max_return_capvol", fixed=CORE, bounds=CAPS,
                         group_caps=ILLIQUID_CAP, cov=cov, target_vol=tv)
            pts.append((r["ann_vol"], r["ann_ret"]))
        except Exception:
            pass
    return pd.DataFrame(pts, columns=["vol", "ret"])


# ------------------------------------------------------------------------- figures
COLORS = plt.cm.tab10.colors


def fig_cumulative(values):
    fig, ax = plt.subplots(figsize=(9, 5))
    order = ["P0_AP5_benchmark", "P2_swiss_bonds->diversified", "P3_draft_recommended",
             "P4_dynamic_swiss_replace", "P5_dynamic_broad_replace",
             "O1_opt_max_sharpe", "O3_opt_min_cvar"]
    for i, k in enumerate([o for o in order if o in values]):
        lw = 2.4 if k == "P0_AP5_benchmark" else 1.4
        ls = "--" if k.startswith("O") else "-"
        ax.plot(values[k], label=k, lw=lw, ls=ls, color=COLORS[i % 10])
    ax.set_title("Cumulative CHF total return (rebased 100) — AP5 vs bond-replacement portfolios")
    ax.set_ylabel("Index (100 = 2019-07-01)"); ax.legend(fontsize=7, ncol=2)
    fig.savefig(os.path.join(FIG, "01_cumulative_returns.png")); plt.close(fig)


def fig_drawdown(values):
    fig, ax = plt.subplots(figsize=(9, 4.2))
    for i, k in enumerate(["P0_AP5_benchmark", "P2_swiss_bonds->diversified",
                           "P5_dynamic_broad_replace", "O3_opt_min_cvar"]):
        if k not in values: continue
        v = values[k]; dd = v / v.cummax() - 1
        ax.plot(dd * 100, label=k, lw=1.3, color=COLORS[i])
    ax.set_title("Drawdown (%) — selected portfolios"); ax.set_ylabel("Drawdown %")
    ax.legend(fontsize=7); fig.savefig(os.path.join(FIG, "02_drawdown.png")); plt.close(fig)


def fig_risk_return(metrics):
    fig, ax = plt.subplots(figsize=(7.5, 5.5))
    for i, k in enumerate(metrics.index):
        x, y = metrics.loc[k, "Vol"] * 100, metrics.loc[k, "CAGR"] * 100
        mk = "*" if k.startswith("O") else ("D" if k.startswith("P0") else "o")
        ax.scatter(x, y, s=90 if k.startswith("P0") else 55, marker=mk,
                   color=COLORS[i % 10], zorder=3)
        ax.annotate(k.replace("_", " "), (x, y), fontsize=6.5,
                    xytext=(4, 3), textcoords="offset points")
    ax.set_xlabel("Annualised volatility %"); ax.set_ylabel("CAGR %")
    ax.set_title("Risk / return — all portfolios (2019-07 → 2026-06)")
    fig.savefig(os.path.join(FIG, "03_risk_return.png")); plt.close(fig)


def fig_frontier(frontier, metrics):
    fig, ax = plt.subplots(figsize=(7.5, 5.5))
    ax.plot(frontier["vol"] * 100, frontier["ret"] * 100, "-", color="navy",
            lw=1.8, label="Efficient frontier (sleeve reallocated, core fixed)")
    for k in ["P0_AP5_benchmark", "O1_opt_max_sharpe", "O2_opt_min_variance",
              "O3_opt_min_cvar"]:
        if k in metrics.index:
            ax.scatter(metrics.loc[k, "Vol"] * 100, metrics.loc[k, "CAGR"] * 100,
                       s=70, zorder=3, label=k)
    ax.set_xlabel("Annualised volatility %"); ax.set_ylabel("CAGR %")
    ax.set_title("Efficient frontier vs benchmark & optimised books")
    ax.legend(fontsize=7); fig.savefig(os.path.join(FIG, "04_efficient_frontier.png"))
    plt.close(fig)


def fig_rolling_corr(rets):
    fig, ax = plt.subplots(figsize=(9, 4.5))
    eq = rets["world_equity"]
    for i, c in enumerate(["swiss_bonds", "world_bonds", "gold", "clo",
                           "managed_futures", "ils", "convertibles"]):
        rc = rets[c].rolling(126).corr(eq)
        ax.plot(rc, label=c, lw=1.1, color=COLORS[i])
    ax.axhline(0, color="k", lw=0.6)
    ax.set_title("Rolling 6-month correlation to World Equity")
    ax.set_ylabel("correlation"); ax.legend(fontsize=7, ncol=2)
    fig.savefig(os.path.join(FIG, "05_rolling_correlation.png")); plt.close(fig)


def fig_corr_heatmap(rets):
    cols = ["swiss_equity", "world_equity", "real_estate", "swiss_bonds", "world_bonds",
            "gold", "convertibles", "clo", "infrastructure", "managed_futures",
            "ils", "private_credit"]
    c = rets[cols].corr()
    fig, ax = plt.subplots(figsize=(8, 7))
    im = ax.imshow(c.values, cmap="RdBu_r", vmin=-1, vmax=1)
    ax.set_xticks(range(len(cols))); ax.set_xticklabels(cols, rotation=90, fontsize=7)
    ax.set_yticks(range(len(cols))); ax.set_yticklabels(cols, fontsize=7)
    for i in range(len(cols)):
        for j in range(len(cols)):
            ax.text(j, i, f"{c.values[i,j]:.2f}", ha="center", va="center", fontsize=6)
    fig.colorbar(im, fraction=0.046); ax.set_title("Full-period correlation matrix (daily CHF returns)")
    fig.savefig(os.path.join(FIG, "06_correlation_heatmap.png")); plt.close(fig)


def fig_stress(stress):
    show = ["P0_AP5_benchmark", "P2_swiss_bonds->diversified", "P3_draft_recommended",
            "P5_dynamic_broad_replace", "O3_opt_min_cvar"]
    ev = ["COVID_crash_2020", "Rate_shock_2022", "SVB_bank_stress_2023"]
    sub = stress.loc[[s for s in show if s in stress.index], ev] * 100
    fig, ax = plt.subplots(figsize=(9, 4.8))
    x = np.arange(len(ev)); w = 0.15
    for i, pf in enumerate(sub.index):
        ax.bar(x + i * w, sub.loc[pf].values, w, label=pf, color=COLORS[i])
    ax.set_xticks(x + w * (len(sub) - 1) / 2); ax.set_xticklabels(ev, fontsize=8)
    ax.axhline(0, color="k", lw=0.6); ax.set_ylabel("Return over window %")
    ax.set_title("Crisis-window performance"); ax.legend(fontsize=7)
    fig.savefig(os.path.join(FIG, "07_stress_windows.png")); plt.close(fig)


def main():
    px = pd.read_csv(os.path.join(HERE, "data/processed/prices_chf.csv"),
                     index_col=0, parse_dates=True)
    rets = pd.read_csv(os.path.join(HERE, "data/processed/returns_daily.csv"),
                       index_col=0, parse_dates=True)

    values, weights_end, meta, opt_summary, books = run_all_portfolios(px, rets)

    # metrics table
    mt = metrics_table(values)
    mt = mt.assign(n_rebal=[meta[k]["n_rebal"] for k in mt.index],
                   turnover=[meta[k]["turnover"] for k in mt.index])
    mt.to_csv(os.path.join(ANL, "portfolio_metrics.csv"))

    # value series
    pd.DataFrame(values).to_csv(os.path.join(ANL, "portfolio_values.csv"))

    # weights of static/optimised books
    wdf = pd.DataFrame({k: books[k] for k in books}).T
    wdf.to_csv(os.path.join(ANL, "portfolio_weights.csv"))

    # rebalancing comparison
    rc = rebalancing_comparison(px)
    rc.to_csv(os.path.join(ANL, "rebalancing_comparison.csv"))

    # stress table
    st = stress_table(values)
    st.to_csv(os.path.join(ANL, "stress_windows.csv"))

    # optimiser summary (sleeve weights + stats)
    osum = pd.DataFrame({k: {**{a: v["weights"].get(a, 0) for a in SLEEVE},
                             "ann_ret": v["ann_ret"], "ann_vol": v["ann_vol"],
                             "sharpe": v["sharpe"], "cvar95": v["cvar95"]}
                         for k, v in opt_summary.items()}).T
    osum.to_csv(os.path.join(ANL, "optimiser_sleeve_weights.csv"))

    # efficient frontier
    frontier = efficient_frontier(rets)
    frontier.to_csv(os.path.join(ANL, "efficient_frontier.csv"), index=False)

    # asset-level stats
    astats = {}
    for c in rets.columns:
        m = perf_metrics(px[c])
        astats[c] = dict(CAGR=m["CAGR"], Vol=m["Vol"], Sharpe=m["Sharpe"],
                         MaxDD=m["MaxDD"], CorrEq=rets[c].corr(rets["world_equity"]))
    pd.DataFrame(astats).T.to_csv(os.path.join(ANL, "asset_stats.csv"))

    # figures
    fig_cumulative(values); fig_drawdown(values); fig_risk_return(mt)
    fig_frontier(frontier, mt); fig_rolling_corr(rets); fig_corr_heatmap(rets)
    fig_stress(st)

    # console summary
    pd.set_option("display.width", 200, "display.max_columns", 30)
    show = ["CAGR", "Vol", "Sharpe", "Sortino", "MaxDD", "Calmar", "CVaR95",
            "n_rebal", "turnover"]
    print("\n=== PORTFOLIO METRICS ===")
    print((mt[show] * [100, 100, 1, 1, 100, 1, 100, 1, 100]).round(2).to_string())
    print("\n=== OPTIMISER SLEEVE WEIGHTS (%) ===")
    print((osum[SLEEVE] * 100).round(1).to_string())
    print("\n=== STRESS WINDOWS (%) ===")
    print((st * 100).round(1).to_string())
    print("\nSaved analysis/*.csv and reports/figures/*.png")


if __name__ == "__main__":
    main()
