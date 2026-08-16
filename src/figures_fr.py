"""
Versions françaises haute résolution (300 dpi) des figures clés, pour insertion dans le
mémoire. Réutilise les calculs de analysis_2008.py ; ne fait que ré-étiqueter et exporter.

Sortie : reports/figures_fr/*.png   (300 dpi, titres et légendes en français)
Lancer :  python src/figures_fr.py   (après build_panel.py)
"""
from __future__ import annotations
import os
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from analysis_2008 import (run_books, validate_vs_vz, regime_metrics,
                           bond_sleeve_by_regime, run_curated, REGIMES, PROC)
from config_main import START

FIGFR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                     "reports", "figures_fr")
os.makedirs(FIGFR, exist_ok=True)
plt.rcParams.update({"figure.dpi": 300, "savefig.dpi": 300, "font.size": 10,
                     "axes.grid": True, "grid.alpha": 0.3, "figure.autolayout": True})

LBL = {"AP5": "AP5 (référence)", "repl_20": "Remplacement 20 %", "repl_40": "Remplacement 40 %",
       "repl_60": "Remplacement 60 %", "repl_80": "Remplacement 80 %", "repl_100": "Remplacement 100 %"}
REG_FR = {"R1_2008-14_low_positive": "R1 2008–14\ntaux bas positifs",
          "R2_2015-22_negative": "R2 2015–22\ntaux négatifs",
          "R3_2022-24_hikes_plateau": "R3 2022–24\nhausses",
          "R4_2024-26_easing": "R4 2024–26\nassouplissement"}


def save(fig, name):
    fig.savefig(os.path.join(FIGFR, name)); plt.close(fig)


def main():
    px = pd.read_csv(os.path.join(PROC, "panel_levels_monthly.csv"),
                     index_col=0, parse_dates=True)
    px = px.loc[px.index >= pd.Timestamp(START)]      # common sample window (audit 4)
    _, _, net, _ = run_books(px)
    r, v, _ = validate_vs_vz(px)
    reg_tables = regime_metrics(net)
    bond_reg = bond_sleeve_by_regime(px)
    curated_net, _ = run_curated(px)

    # 01 — rendement cumulé
    fig, ax = plt.subplots(figsize=(9.5, 5))
    for k in ["AP5","repl_20","repl_40","repl_60","repl_80","repl_100"]:
        ax.plot(net[k], label=LBL[k], lw=2.4 if k == "AP5" else 1.4)
    ax.axvspan(pd.Timestamp(REGIMES["R2_2015-22_negative"][0]),
               pd.Timestamp(REGIMES["R2_2015-22_negative"][1]), color="grey", alpha=0.08)
    ax.set_title("Rendement total cumulé en CHF, net de frais (2008–2026)\nAP5 vs remplacement obligataire")
    ax.set_ylabel("Indice (100 = janv. 2008)"); ax.set_xlabel("Année")
    ax.legend(fontsize=9); save(fig, "01_rendement_cumule.png")

    # 02 — validation
    fig, ax = plt.subplots(figsize=(9, 4.8))
    ax.plot(v, label="VZ AP5 réel (VVIA)", lw=2.4, color="black")
    ax.plot(r, label="AP5 reconstitué (indices, net de frais)", lw=1.6, ls="--", color="tab:red")
    ax.set_title("Validation : AP5 reconstitué vs performance réelle VZ\n(base 100, 2019–2026)")
    ax.set_ylabel("Indice"); ax.set_xlabel("Année")
    ax.legend(fontsize=9); save(fig, "02_validation.png")

    # 04 — rendement par régime
    regs = [k for k in REGIMES if k != "Full_2008-26"]
    fig, ax = plt.subplots(figsize=(9.5, 5))
    x = np.arange(len(regs)); w = 0.38
    for i, b in enumerate(["AP5", "repl_100"]):
        vals = [reg_tables[rg].loc[b, "CAGR"] * 100 for rg in regs]
        ax.bar(x + (i - 0.5) * w, vals, w, label=LBL[b])
    ax.set_xticks(x); ax.set_xticklabels([REG_FR[rg] for rg in regs], fontsize=8.5)
    ax.axhline(0, color="k", lw=0.8)
    ax.set_ylabel("Rendement annualisé %")
    ax.set_title("Rendement annualisé par régime de taux (BNS)")
    ax.legend(fontsize=9); save(fig, "04_rendement_par_regime.png")

    # 05 — comportement obligataire par régime
    bond_lbl = {"swiss_bonds": "Oblig. suisses", "world_bonds": "Oblig. mondiales", "cash": "Liquidités"}
    fig, ax = plt.subplots(figsize=(9.5, 5))
    x = np.arange(len(regs)); w = 0.27
    for i, c in enumerate(["swiss_bonds", "world_bonds", "cash"]):
        ax.bar(x + (i - 1) * w, [bond_reg.loc[rg, c] * 100 for rg in regs], w, label=bond_lbl[c])
    ax.set_xticks(x); ax.set_xticklabels([REG_FR[rg] for rg in regs], fontsize=8.5)
    ax.axhline(0, color="k", lw=0.8)
    ax.set_ylabel("Rendement annualisé %")
    ax.set_title("Comportement de la poche obligataire par régime de taux\n(le problème visé par le mémoire)")
    ax.legend(fontsize=9); save(fig, "05_obligations_par_regime.png")

    # 08 — panier curated vs naïf
    fig, ax = plt.subplots(figsize=(9.5, 5))
    ax.plot(net["AP5"], label="AP5 (référence)", lw=2.4, color="black")
    ax.plot(net["repl_100"], label="Panier naïf (100 %)", lw=1.5, color="tab:orange")
    ax.plot(curated_net["curated_100"], label="Panier curated (100 %)", lw=1.8, color="tab:green")
    ax.set_title("Panier curated vs naïf (100 % remplacé, net de frais)")
    ax.set_ylabel("Indice (100 = janv. 2008)"); ax.set_xlabel("Année")
    ax.legend(fontsize=9); save(fig, "08_curated_vs_naif.png")

    print("Figures FR (300 dpi) écrites dans reports/figures_fr/ :")
    for f in sorted(os.listdir(FIGFR)):
        print("  ", f)


if __name__ == "__main__":
    main()
