"""
Figures (300 dpi, French labels) for the main thesis version (these_principale_FR.md).
Focus on the single-alternative / mix / trade-off story that the other figure scripts don't cover.

Outputs: reports/figures_fr/T1_..T4_*.png
Run:  python src/figures_these.py   (after build_panel.py)
"""
from __future__ import annotations
import os
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from engine import backtest, perf_metrics
from config_main import (AP5, PRIMARY_BASKET, PRIMARY_W, CURATED_W, BAND_BASE, TC_BPS,
                         CATEGORY, PER, START, STEPS, step_name)
from analysis_2008 import replacement_book, net_of_fee
from single_alternatives import LABEL

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROC = os.path.join(HERE, "data", "processed")
FIGFR = os.path.join(HERE, "reports", "figures_fr")
os.makedirs(FIGFR, exist_ok=True)
plt.rcParams.update({"figure.dpi": 300, "savefig.dpi": 300, "font.size": 10,
                     "axes.grid": True, "grid.alpha": 0.3, "figure.autolayout": True})

SHORT = {"gold": "Or", "commodities": "Mat. premières", "infrastructure": "Infrastructures",
         "managed_futures": "Managed futures", "high_yield": "Haut rendement", "em_debt": "Dette émerg."}


def _net(px, book):
    bt = backtest(px, book, mode="smart", rel_band=BAND_BASE, monitor_freq="ME",
                  tc_bps=TC_BPS, group_map=CATEGORY)
    return net_of_fee(bt["value"])


def main():
    px = pd.read_csv(os.path.join(PROC, "panel_levels_monthly.csv"), index_col=0, parse_dates=True)
    px = px.loc[px.index >= pd.Timestamp(START)]
    cash = px["cash"].pct_change()

    # ---- T1 : Étape A — Sharpe de chaque alternative SEULE (100% des obligations) vs AP5 ----
    ap5_sharpe = perf_metrics(_net(px, AP5), periods=PER, rf_series=cash)["Sharpe"]
    single = {SHORT[a]: perf_metrics(_net(px, replacement_book(1.0, {a: 1.0})), periods=PER,
                                     rf_series=cash)["Sharpe"] for a in PRIMARY_BASKET}
    s = pd.Series(single).sort_values()
    fig, ax = plt.subplots(figsize=(9, 5))
    colors = ["tab:green" if v >= ap5_sharpe else "tab:red" for v in s.values]
    ax.barh(s.index, s.values, color=colors)
    ax.axvline(ap5_sharpe, color="black", ls="--", lw=1.5, label=f"AP5 (référence) = {ap5_sharpe:.2f}")
    for i, v in enumerate(s.values):
        ax.text(v + 0.005, i, f"{v:.2f}", va="center", fontsize=9)
    ax.set_xlabel("Sharpe (rendement ajusté au risque, excès sur cash CHF)")
    ax.set_title("Étape A — remplacer 100 % des obligations par UNE seule alternative\n"
                 "(vert = mieux que l'AP5 ; rouge = moins bien). Seule l'or dépasse l'AP5.")
    ax.legend(loc="lower right", fontsize=9)
    fig.savefig(os.path.join(FIGFR, "T1_etape_A_une_alternative.png")); plt.close(fig)

    # ---- T2 : la courbe de compromis — rendement vs pire perte, à mesure qu'on remplace ----
    rows = []
    for p in STEPS:
        book = AP5 if p == 0 else replacement_book(p / 100, PRIMARY_W)
        m = perf_metrics(_net(px, book), periods=PER, rf_series=cash)
        rows.append((p, m["CAGR"] * 100, m["MaxDD"] * 100, m["Sharpe"]))
    d = pd.DataFrame(rows, columns=["pct", "CAGR", "MaxDD", "Sharpe"])
    fig, ax = plt.subplots(figsize=(9, 5))
    sc = ax.scatter(-d["MaxDD"], d["CAGR"], c=d["pct"], cmap="viridis", s=60, zorder=3)
    for _, r in d.iterrows():
        ax.annotate(f"{int(r['pct'])}%", (-r["MaxDD"], r["CAGR"]), fontsize=8,
                    xytext=(4, 4), textcoords="offset points")
    ax.plot(-d["MaxDD"], d["CAGR"], color="grey", lw=1, zorder=2)
    cb = fig.colorbar(sc, ax=ax); cb.set_label("% des obligations remplacé")
    ax.set_xlabel("Pire perte (drawdown, %) →  plus de risque")
    ax.set_ylabel("Rendement annualisé (%) →  plus de rendement")
    ax.set_title("La courbe de compromis (mélange équipondéré)\n"
                 "Plus on remplace, plus le rendement ET le risque montent")
    fig.savefig(os.path.join(FIGFR, "T2_courbe_compromis.png")); plt.close(fig)

    # ---- T3 : Sharpe vs % remplacé, une courbe par alternative seule ----
    fig, ax = plt.subplots(figsize=(9.5, 5.5))
    fracs = [0, 25, 50, 75, 100]
    for a in PRIMARY_BASKET:
        ys = []
        for f in fracs:
            book = AP5 if f == 0 else replacement_book(f / 100, {a: 1.0})
            ys.append(perf_metrics(_net(px, book), periods=PER, rf_series=cash)["Sharpe"])
        ax.plot(fracs, ys, "o-", label=SHORT[a], lw=1.8)
    ax.axhline(ap5_sharpe, color="black", ls="--", lw=1.2, label="AP5 (0 %)")
    ax.set_xlabel("% des obligations remplacé par cette seule alternative")
    ax.set_ylabel("Sharpe"); ax.set_title("Étape A (détail) — Sharpe selon la dose de remplacement")
    ax.legend(fontsize=8, ncol=2)
    fig.savefig(os.path.join(FIGFR, "T3_sharpe_par_dose.png")); plt.close(fig)

    # ---- T4 : rendement cumulé — AP5 vs 100% or vs mélange trié ----
    fig, ax = plt.subplots(figsize=(9.5, 5))
    ax.plot(_net(px, AP5), label="AP5 (référence)", lw=2.4, color="black")
    ax.plot(_net(px, replacement_book(1.0, {"gold": 1.0})), label="100 % or", lw=1.6, color="tab:orange")
    ax.plot(_net(px, replacement_book(1.0, CURATED_W)), label="100 % mélange trié", lw=1.6, color="tab:green")
    ax.plot(_net(px, replacement_book(1.0, PRIMARY_W)), label="100 % mélange égal", lw=1.3,
            color="tab:red", ls="--")
    ax.set_ylabel("Indice (100 = févr. 2008)"); ax.set_xlabel("Année")
    ax.set_title("Rendement cumulé, net de frais — AP5 vs remplacements à 100 %")
    ax.legend(fontsize=9)
    fig.savefig(os.path.join(FIGFR, "T4_cumule_ap5_or_melange.png")); plt.close(fig)

    print("Figures thèse (300 dpi) écrites :")
    for f in sorted(os.listdir(FIGFR)):
        if f.startswith("T"):
            print("  ", f)


if __name__ == "__main__":
    main()
