"""
Build Word (.docx) versions of the executive summary (FR) and the full report (EN) from the
Markdown sources, via pandoc, with the key figures embedded as a captioned appendix.

Run:  python reports/docx/build_docx.py   (needs pandoc; figures already generated)
"""
from __future__ import annotations
import os, subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
FIG = os.path.join(ROOT, "reports", "figures")
FIGFR = os.path.join(ROOT, "reports", "figures_fr")

EN_FIGS = [
    ("01_cumulative_2008.png", "Cumulative CHF total return, net of fees (2008–2026)."),
    ("02_ap5_validation.png", "Validation: reconstructed AP5 vs the real VZ VVIA track record."),
    ("04_regime_returns.png", "Annualised return by SNB rate regime."),
    ("05_bonds_by_regime.png", "Bond-sleeve behaviour by rate regime."),
    ("06_correlation.png", "Monthly return correlations (2008–2026)."),
    ("07_rolling_corr.png", "Rolling 24-month equity–bond correlation."),
    ("09_bootstrap_ci.png", "Bootstrap ΔSharpe vs AP5 (CI straddles zero) and P(worse drawdown)."),
    ("08_curated_vs_naive.png", "Curated vs naïve replacement basket — ex-post (100% replaced)."),
]
FR_FIGS = [
    ("01_rendement_cumule.png", "Rendement total cumulé en CHF, net de frais (2008–2026)."),
    ("02_validation.png", "Validation : AP5 reconstitué vs performance réelle VZ."),
    ("04_rendement_par_regime.png", "Rendement annualisé par régime de taux (BNS)."),
    ("05_obligations_par_regime.png", "Comportement de la poche obligataire par régime."),
    ("08_curated_vs_naif.png", "Panier curated vs naïf (100 % remplacé)."),
]

# figure set specific to the main thesis version (single-alt / mix / trade-off)
THESE_FIGS = [
    ("T1_etape_A_une_alternative.png",
     "Étape A — remplacer 100 % des obligations par une seule alternative (seule l'or dépasse l'AP5)."),
    ("T3_sharpe_par_dose.png", "Étape A (détail) — Sharpe selon la dose de remplacement, par alternative."),
    ("T2_courbe_compromis.png", "La courbe de compromis : plus on remplace, plus rendement ET risque montent."),
    ("T4_cumule_ap5_or_melange.png", "Rendement cumulé net de frais — AP5 vs remplacements à 100 %."),
    ("05_obligations_par_regime.png", "Comportement des obligations par régime de taux."),
    ("04_rendement_par_regime.png", "Rendement annualisé par régime de taux (BNS)."),
    ("02_validation.png", "Validation : AP5 reconstitué vs performance réelle VZ."),
]


def build(md_src, figdir, figs, out_docx, title, heading, toc=False):
    with open(md_src, encoding="utf-8") as f:
        body = f.read()
    lines = [body]
    if figs:
        lines += ["", f"\n\\newpage\n", f"## {heading}", ""]
        for i, (fn, cap) in enumerate(figs, 1):
            path = os.path.join(figdir, fn).replace("\\", "/")
            lines += [f"**Figure {i} — {cap}**", "", f"![]({path})", ""]
    tmp = os.path.join(HERE, "_tmp_" + os.path.basename(out_docx) + ".md")
    with open(tmp, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    cmd = ["pandoc", tmp, "-o", out_docx, "--from", "gfm",
           "-V", "geometry:margin=2cm", f"--metadata=title:{title}"]
    if toc:
        cmd += ["--toc", "--toc-depth=2"]
    subprocess.run(cmd, check=True)
    os.remove(tmp)
    print("wrote", os.path.relpath(out_docx, ROOT))


def main():
    # version principale de la thèse (FR), structurée comme le premier document
    build(os.path.join(ROOT, "reports", "these_principale_FR.md"), FIGFR, THESE_FIGS,
          os.path.join(HERE, "These_principale_FR.docx"),
          "Alternatives aux obligations dans un portefeuille suisse (VZ AP5, 2008–2026)",
          "Figures", toc=True)
    build(os.path.join(ROOT, "reports", "guide_pas_a_pas.md"), FIGFR, FR_FIGS,
          os.path.join(HERE, "Guide_pas_a_pas_FR.docx"),
          "Guide pas à pas — comprendre et justifier l'analyse (VZ AP5, 2008–2026)",
          "Figures (illustrations)", toc=True)
    build(os.path.join(ROOT, "reports", "tracabilite_code_FR.md"), FIGFR, [],
          os.path.join(HERE, "Tracabilite_code_FR.docx"),
          "Traçabilité — où se trouve chaque chose dans le code (VZ AP5)",
          "", toc=True)
    build(os.path.join(ROOT, "reports", "resume_executif.md"), FIGFR, FR_FIGS,
          os.path.join(HERE, "Resume_executif_FR.docx"),
          "Résumé exécutif — Alternatives aux obligations (VZ AP5, 2008–2026)",
          "Figures")
    build(os.path.join(ROOT, "reports", "thesis_report.md"), FIG, EN_FIGS,
          os.path.join(HERE, "Bond_replacement_full_report_EN.docx"),
          "Alternatives to bonds — empirical foundation (VZ AP5, 2008–2026)",
          "Figures", toc=True)


if __name__ == "__main__":
    main()
