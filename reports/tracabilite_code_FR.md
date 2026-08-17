# Traçabilité — où se trouve chaque chose dans le code

**Mémoire VZ AP5 · pour justifier chaque étape** — ce document relie **chaque chose faite** au
**fichier Python** et aux **lignes exactes**. Les numéros de ligne correspondent à l'état actuel du
dépôt ; si le code bouge, ils peuvent se décaler de quelques lignes (le **nom de la fonction** reste
le repère fiable).

> Convention : `fichier.py:12-34` signifie « fichier.py, lignes 12 à 34 ». On peut cliquer le
> fichier sur GitHub puis aller à la ligne.

## 1. Les hypothèses et réglages (le « paramétrage »)

Tout est centralisé dans **un seul fichier**, `src/config_main.py`, pour éviter toute incohérence.

| Ce qui a été fixé | Fichier : lignes | Valeur |
|---|---|---|
| Composition exacte de l'AP5 (indices) | `src/config_main.py:10-21` | poids VZ Kundendoku |
| Les obligations à remplacer (42 %) | `src/config_main.py:22-25` | 16,8 % CH + 25,2 % monde |
| Les 6 alternatives (panier principal, équipondéré) | `src/config_main.py:30-32` | or, mat. premières, infra, CTA, HY, EM |
| Le mélange trié (curated) | `src/config_main.py:34` | HY 35 / EM 30 / or 20 / infra 15 |
| Les frais (1,37 %/an) | `src/config_main.py:39-41` | 0,12 % + 1,25 % |
| Coûts de transaction (10 pb) | `src/config_main.py:42` | + grille 0–50 pb l.48 |
| Bande de rééquilibrage (±8 %) | `src/config_main.py:46-47` | + grille ±5–20 % |
| Fenêtre commune (fév. 2008 – juin 2026) | `src/config_main.py:52` | `START, END` |
| Doses de remplacement (0,10,…,100 %) | `src/config_main.py:53` | `STEPS` |
| Surveillance par **catégorie** (Smart Rebalancing) | `src/config_main.py:59-67` | `CATEGORY` |
| Les 4 régimes de taux BNS | `src/config_main.py:71-76` | R1–R4 |
| Fenêtres de crise (2020, 2022, 2023) | `src/config_main.py:80-83` | `STRESS` |

## 2. Le moteur de calcul

| Ce qui a été fait | Fichier : lignes |
|---|---|
| Backtest (rééquilibrage par bandes, coûts, régimes) | `src/engine.py:35-153` (fonction `backtest`) |
| Surveillance des bandes **au niveau catégorie** | `src/engine.py:87-100` (`_breach`) |
| Métriques : CAGR, vol, **Sharpe** (excès sur cash), Sortino, pire perte, **CVaR** | `src/engine.py:162-201` (`perf_metrics`) |

## 3. Les étapes de l'analyse (fichier principal `src/analysis_2008.py`)

| Étape (cf. guide global) | Fichier : lignes |
|---|---|
| Construire un portefeuille de remplacement (dose × panier) | `src/analysis_2008.py:46-53` (`replacement_book`) |
| Appliquer les frais **exactement** `(1+r)/(1+m)` | `src/analysis_2008.py:90-96` (`net_of_fee`) |
| Backtester chaque dose 0→100 % | `src/analysis_2008.py:99-108` (`run_books`) |
| **Valider** vs le vrai produit VZ | `src/analysis_2008.py:112-146` (`validate_vs_vz`) |
| Sensibilité de la validation à la bande (5/8/10/20 %) | `src/analysis_2008.py:149-162` (`validation_band_sensitivity`) |
| Statistiques par actif (tableau de comparaison) | `src/analysis_2008.py:164-182` (`descriptive_stats`) |
| Test de redondance obligations suisses/mondiales | `src/analysis_2008.py:184-201` (`bond_redundancy`) |
| Performance **par régime** de taux | `src/analysis_2008.py:216-228` (`regime_metrics`) |
| Comportement des **obligations par régime** | `src/analysis_2008.py:230-242` (`bond_sleeve_by_regime`) |
| Mélange équipondéré vs mélange trié | `src/analysis_2008.py:337-349` (`run_curated`) |
| Fichier de résultats officiel (manifest) | `src/analysis_2008.py:405-432` |

## 4. Remplacer par UNE alternative à la fois (Étape A)

| Ce qui a été fait | Fichier : lignes |
|---|---|
| Chaque alternative seule à 100 % + les deux mélanges | `src/single_alternatives.py:47-58` (`full_replacement_table`) |
| Balayage 25/50/75/100 % par alternative | `src/single_alternatives.py:60-71` (`sweep_table`) |
| Sorties CSV | `src/single_alternatives.py:81-82` |

## 5. Robustesse et tests statistiques

| Ce qui a été fait | Fichier : lignes |
|---|---|
| **Bootstrap** (3 000 rejeux) — ΔCAGR/ΔSharpe/ΔMaxDD/ΔCVaR | `src/robustness.py:83-118` (`bootstrap_ci`) |
| Sensibilité (bande, coûts, couverture, période) + CVaR | `src/robustness.py:120-159` (`sensitivity`) |
| Comparaison **catégorie vs par constituant** | `src/robustness.py:161-177` (`granular_vs_category`) |
| Table de stress par crise | `src/robustness.py:179-192` (`stress_table`) |

## 6. Allocation avancée (Étape C — optimiseur)

| Ce qui a été fait | Fichier : lignes |
|---|---|
| Mise en place (poches, plafonds, appel de l'optimiseur, frais exacts) | `src/appendix_optimization.py:32-87` |
| L'algorithme d'optimisation lui-même (max-Sharpe / min-variance / min-CVaR) | `src/optimize.py:80` (`optimise`) |

## 7. Les figures

| Figure | Fichier : lignes |
|---|---|
| **T1** — Étape A : une seule alternative vs AP5 | `src/figures_these.py:44-59` |
| **T2** — courbe de compromis (rendement vs risque) | `src/figures_these.py:61-79` |
| **T3** — Sharpe selon la dose, par alternative | `src/figures_these.py:81-94` |
| **T4** — rendement cumulé AP5 vs or vs mélanges | `src/figures_these.py:96-106` |
| Figures françaises 01/02/04/05/08 (cumul, validation, régimes) | `src/figures_fr.py:38-102` |

## 8. Les tests automatiques (preuve que le moteur est correct)

Fichier `tests/test_engine.py` — se lance avec `python tests/test_engine.py` :

| Ce qui est vérifié | Fichier : ligne |
|---|---|
| Les poids somment à 1 | `tests/test_engine.py:25` |
| Pas de rééquilibrage à l'intérieur de la bande | `tests/test_engine.py:31` |
| Rééquilibrage quand la bande est franchie | `tests/test_engine.py:39` |
| Frais **exacts** `(1+r)/(1+m)` | `tests/test_engine.py:48` |
| Coût de transaction = rotation × coût | `tests/test_engine.py:58` |
| Les bandes **catégorie** ignorent la dérive intra-catégorie | `tests/test_engine.py:71` |
| Pas de « look-ahead » (aucune info du futur utilisée) | `tests/test_engine.py:89` |

## 9. Comment tout relancer (l'ordre du pipeline)

```
python src/build_panel.py          # 1. construit le panneau mensuel (données)
python src/analysis_2008.py        # 2. analyse principale + validation + manifest + figures
python src/single_alternatives.py  # 3. Étape A : une alternative à la fois
python src/robustness.py           # 4. bootstrap + sensibilités + stress + catégorie-vs-granulaire
python src/appendix_optimization.py# 5. Étape C : optimiseur (annexe)
python src/figures_these.py        # 6. figures T1–T4 de la thèse
python src/figures_fr.py           # 7. figures françaises 300 dpi
python reports/docx/build_docx.py  # 8. génère les fichiers Word
python tests/test_engine.py        # (à tout moment) lance les 7 tests
```

Chaque chiffre cité dans la thèse provient d'un de ces fichiers ; la **source unique** de
référence est `analysis/results_manifest.json` (généré à l'étape 2).
