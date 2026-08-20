# Résultats complets — tous les calculs, reliés au code

**Mémoire VZ AP5 · CHF, mensuel, net de frais · février 2008 – juin 2026**

> Ce document rassemble **tous les résultats chiffrés** produits par l'étude. Chaque tableau
> indique **sa source** (le fichier `analysis/*.csv`) **et le code Python** qui l'a calculé
> (`fichier.py:lignes`). La **source unique** de vérité est `analysis/results_manifest.json`.
> Convention : `fichier.py:12-34` = fichier, lignes 12 à 34 ; le **nom de la fonction** reste le
> repère fiable si les lignes se décalent. Rendements/vol/pertes en **% par an** sauf mention.

---

## 1. Validation de la reconstruction (tracking error)

Reconstitution de l'AP5 comparée à la **vraie valeur du produit VZ** (85 mois, 2019–2026).

| Mesure | Valeur |
|---|---|
| Corrélation mensuelle | **0,954** |
| Tracking error (annualisé) | **2,37 %** |
| Bêta (régression VZ = α + β·recon) | 0,970 |
| Alpha (annualisé) | −0,37 % |
| R² | 0,911 |
| Écart mensuel absolu moyen | 0,51 % |
| Rendement cumulé — reconstitué vs VZ réel | +25,25 % vs +21,09 % |

**Source :** `analysis/ap5_validation.csv` · **Code :** `src/analysis_2008.py:112-146`
(`validate_vs_vz`), écriture `:392`.

### 1b. La validation ne dépend pas de la bande de surveillance

| Bande | Corrélation | Tracking error | Bêta | R² |
|---|---|---|---|---|
| ±5 % (base) | 0,9543 | 2,37 % | 0,970 | 0,911 |
| ±8 % (modèle principal) | 0,9540 | 2,38 % | 0,967 | 0,910 |
| ±10 % | 0,9540 | 2,38 % | 0,967 | 0,910 |
| ±20 % | 0,9525 | 2,41 % | 0,969 | 0,907 |

**Source :** `analysis/ap5_validation_band_sensitivity.csv` · **Code :** `src/analysis_2008.py:149-162`
(`validation_band_sensitivity`), écriture `:393`.

## 2. Performance par actif (chaque « ingrédient »)

Sharpe = excès sur le cash CHF. Le CSV contient aussi l'asymétrie (Skew) et le kurtosis (ExKurt).

| Actif | Début | CAGR | Vol | Sharpe | Pire perte |
|---|---|---|---|---|---|
| Obligations suisses (large) | 2008-02 | 1,81 % | 3,62 % | 0,50 | −15,9 % |
| Obligations suisses (1–5 a) | 2008-02 | 1,14 % | 1,68 % | 0,66 | −7,3 % |
| Obligations monde (large) | 2008-02 | 1,07 % | 3,50 % | 0,30 | −18,5 % |
| Obligations monde (1–5 a) | 2008-02 | 0,60 % | 1,79 % | 0,31 | −8,9 % |
| Actions suisses (SPI) | 2008-02 | 6,61 % | 12,59 % | 0,57 | −38,0 % |
| Actions suisses (SLI) | 2008-02 | 6,93 % | 14,45 % | 0,53 | −42,4 % |
| Actions suisses (SPI Extra) | 2008-02 | 6,52 % | 14,44 % | 0,51 | −44,0 % |
| Actions monde (MSCI World) | 2008-02 | 8,57 % | 18,73 % | 0,53 | −41,6 % |
| Actions monde (Small) | 2008-02 | 8,53 % | 20,64 % | 0,50 | −40,8 % |
| Actions émergentes | 2008-02 | 4,72 % | 19,68 % | 0,33 | −49,2 % |
| Immobilier (SXI) | 2008-02 | 6,09 % | 7,74 % | 0,80 | −19,1 % |
| **Or** | 2008-02 | 6,11 % | 16,37 % | 0,44 | −38,0 % |
| **Haut rendement (HY, couvert)** | 2008-02 | 3,87 % | 10,27 % | 0,41 | −29,4 % |
| **Dette émergente (EM, couvert)** | 2008-02 | 3,27 % | 11,50 % | 0,33 | −28,4 % |
| **Infrastructures** | 2008-02 | 4,00 % | 14,77 % | 0,34 | −45,0 % |
| **Managed futures** | 2008-02 | −0,79 % | 13,79 % | 0,01 | −47,1 % |
| **Matières premières** | 2008-02 | −2,02 % | 18,85 % | −0,02 | −75,7 % |
| Convertibles (candidat, dès 2009) | 2009-05 | 9,99 % | 12,58 % | 0,83 | −24,0 % |
| Liquidités (cash BNS) | 2008-02 | 0,06 % | 0,26 % | — | −5,5 % |

*Variantes non couvertes (robustesse) : HY 3,84 % / Sharpe 0,40 ; EM 3,24 % / Sharpe 0,33.*

**Source :** `analysis/descriptive_stats.csv` · **Code :** `src/analysis_2008.py:164-182`
(`descriptive_stats`), écriture `:387`.

## 3. Performance par palier de remplacement (0 → 100 %, pas de 10 %)

Remplacement des obligations par le **mélange équipondéré** des six alternatives. Le CSV contient
aussi `Sharpe_rf0` (Sharpe sans risque nul), `Sortino` et `Calmar`.

| Portefeuille | CAGR | Vol | Sharpe | Pire perte | CVaR 95 % |
|---|---|---|---|---|---|
| AP5 (0 %) | 3,55 % | 7,70 % | 0,483 | −20,3 % | −5,24 % |
| Remplacement 10 % | 3,63 % | 7,90 % | 0,482 | −21,1 % | −5,41 % |
| 20 % | 3,71 % | 8,11 % | 0,482 | −21,9 % | −5,56 % |
| 30 % | 3,78 % | 8,32 % | 0,479 | −22,7 % | −5,73 % |
| 40 % | 3,86 % | 8,56 % | 0,478 | −23,5 % | −5,93 % |
| 50 % | 3,95 % | 8,78 % | 0,478 | −24,1 % | −6,11 % |
| 60 % | 4,03 % | 9,02 % | 0,476 | −24,9 % | −6,31 % |
| 70 % | 4,09 % | 9,27 % | 0,472 | −25,7 % | −6,51 % |
| 80 % | 4,18 % | 9,52 % | 0,471 | −26,5 % | −6,71 % |
| 90 % | 4,21 % | 9,78 % | 0,465 | −27,2 % | −6,90 % |
| 100 % | 4,28 % | 10,05 % | 0,461 | −28,0 % | −7,12 % |

**Source :** `analysis/perf_full_net.csv` · **Code :** `src/analysis_2008.py:99-108` (`run_books`)
+ `main` `:379-385`, écriture `:386`. Les **poids** de chaque palier : `analysis/book_weights.csv`
(écriture `:391`).

## 4. Comportement des obligations par régime de taux

Rendement annualisé de chaque tranche d'obligations, par régime BNS.

| Régime | Suisses large | Suisses 1–5 | Monde large | Monde 1–5 | Cash |
|---|---|---|---|---|---|
| R1 2008–14 (taux bas positifs) | +4,10 % | +2,56 % | +4,06 % | +2,47 % | +0,52 % |
| R2 2015–22 (négatifs) | −0,48 % | −0,36 % | −0,35 % | −0,67 % | −0,74 % |
| R3 2022–24 (hausses) | +1,61 % | +0,87 % | **−2,88 %** | −1,19 % | +1,03 % |
| R4 2024–26 (assouplissement) | +2,66 % | +2,03 % | −0,00 % | +0,58 % | +0,55 % |
| Toute la période | +1,81 % | +1,14 % | +1,07 % | +0,60 % | +0,06 % |

**Source :** `analysis/bond_sleeve_by_regime.csv` · **Code :** `src/analysis_2008.py:230-242`
(`bond_sleeve_by_regime`), écriture `:388`.

## 5. Performance des portefeuilles par régime

Résumé AP5 vs remplacements (CAGR ; Sharpe entre parenthèses). Le **détail des 11 paliers** par
régime (CAGR/Vol/Sharpe/MaxDD) est dans les fichiers `regime_*.csv`.

| Régime | AP5 | 20 % | 50 % | 100 % |
|---|---|---|---|---|
| R1 2008–14 | 3,74 % (0,43) | 3,6 % | 3,3 % | 2,80 % (0,26) |
| R2 2015–22 | 3,35 % (0,59) | 3,7 % | 4,2 % | 5,12 % (0,63) |
| R3 2022–24 | −0,18 % (−0,08) | −0,4 % | −0,8 % | −1,58 % (−0,18) |
| R4 2024–26 | 6,49 % (0,93) | 7,4 % | 8,7 % | 10,69 % (1,32) |
| Toute la période | 3,55 % (0,48) | 3,71 % | 3,95 % | 4,28 % (0,46) |

**Source :** `analysis/regime_R1…R4_*.csv` et `regime_Full_2008-26.csv` · **Code :**
`src/analysis_2008.py:216-228` (`regime_metrics`), écriture `:390`.

### 5b. Les obligations suisses et mondiales ne sont pas redondantes

| Corrélation | R² (variance partagée) | Bêta (suisses sur mondiales) | Corrélation en R3 |
|---|---|---|---|
| 0,787 | 0,619 | 0,813 | 0,831 |

**Source :** `analysis/results_manifest.json` (clé `bond_redundancy`) · **Code :**
`src/analysis_2008.py:184-201` (`bond_redundancy`).

## 6. Étape A — remplacer par UNE seule alternative (100 %)

| 100 % des obligations → | CAGR | Vol | Sharpe | Pire perte | CVaR 95 % |
|---|---|---|---|---|---|
| **Or** | 5,87 % | 10,36 % | **0,598** | −20,7 % | −6,83 % |
| Mélange trié (rappel) | 4,89 % | 10,02 % | 0,521 | −27,6 % | −7,04 % |
| **AP5 (référence)** | 3,55 % | 7,70 % | **0,483** | −20,3 % | −5,24 % |
| Haut rendement | 4,56 % | 10,33 % | 0,478 | −30,8 % | −7,25 % |
| Dette émergente | 4,43 % | 10,27 % | 0,469 | −26,0 % | −7,28 % |
| Mélange équipondéré (rappel) | 4,28 % | 10,05 % | 0,461 | −28,0 % | −7,12 % |
| Infrastructures | 4,63 % | 12,82 % | 0,413 | −39,1 % | −9,40 % |
| Managed futures | 2,86 % | 10,17 % | 0,322 | −26,3 % | −6,34 % |
| Matières premières | 2,36 % | 13,13 % | 0,239 | −39,1 % | −9,71 % |

**Source :** `analysis/single_alt_full_replacement.csv` · **Code :** `src/single_alternatives.py:47-58`
(`full_replacement_table`), écriture `:81`.

### 6b. Sharpe (et pire perte) selon la dose, par alternative

| Alternative | Sharpe 25 % | 50 % | 75 % | 100 % |
|---|---|---|---|---|
| Or | 0,538 | 0,581 | 0,599 | 0,598 |
| Haut rendement | 0,489 | 0,488 | 0,483 | 0,478 |
| Dette émergente | 0,484 | 0,486 | 0,481 | 0,469 |
| Infrastructures | 0,465 | 0,443 | 0,425 | 0,413 |
| Managed futures | 0,447 | 0,409 | 0,359 | 0,322 |
| Matières premières | 0,414 | 0,345 | 0,285 | 0,239 |

*(Les colonnes de pire perte par dose sont aussi dans le CSV.)* **Source :**
`analysis/single_alt_sweep.csv` · **Code :** `src/single_alternatives.py:60-71` (`sweep_table`),
écriture `:82`.

## 7. Étape B — mélange équipondéré vs mélange trié

| Portefeuille | CAGR | Vol | Sharpe | Pire perte | CVaR 95 % |
|---|---|---|---|---|---|
| Équipondéré 33 % | 3,80 % | 8,40 % | 0,479 | −22,9 % | −5,80 % |
| Équipondéré 67 % | 4,07 % | 9,18 % | 0,473 | −25,4 % | −6,44 % |
| Équipondéré 100 % | 4,28 % | 10,05 % | 0,461 | −28,0 % | −7,12 % |
| **Trié 33 %** | 4,04 % | 8,40 % | 0,506 | −22,6 % | −5,72 % |
| **Trié 67 %** | 4,45 % | 9,17 % | 0,514 | −25,1 % | −6,34 % |
| **Trié 100 %** | 4,89 % | 10,02 % | **0,521** | −27,6 % | −7,04 % |

**Source :** `analysis/curated_vs_naive.csv` · **Code :** `src/analysis_2008.py:337-349`
(`run_curated`), écriture `:377`.

## 8. Étape C — allocation optimisée (en échantillon)

| Optimisation | CAGR | Vol | Sharpe | Pire perte | CVaR 95 % |
|---|---|---|---|---|---|
| Max-Sharpe | 4,39 % | 8,12 % | **0,563** | −18,4 % | −5,57 % |
| Variance minimale | 3,26 % | 7,53 % | 0,455 | −20,5 % | −5,12 % |
| CVaR minimale | 3,26 % | 7,53 % | 0,455 | −20,5 % | −5,12 % |

**Poids choisis pour les 42 %** (cœur actions/immobilier/liquidités fixé) :

| Optimisation | Obligations suisses | Obligations monde 1–5 | Or |
|---|---|---|---|
| Max-Sharpe | 30 % | 0 % | 12 % |
| Variance / CVaR minimale | 0 % | 42 % | 0 % |

**Source :** `analysis/appendix_optimisation_perf.csv` et `..._weights.csv` · **Code :**
`src/appendix_optimization.py:52-87`, algorithme `src/optimize.py:80` (`optimise`).

## 8b. Benchmarks de comparaison (actions, cash, remplacement asymétrique)

Trois portefeuilles de contrôle, mêmes hypothèses que tout le reste :

| 100 % des obligations → | CAGR | Vol | Sharpe | Pire perte | CVaR 95 % |
|---|---|---|---|---|---|
| AP5 (référence) | 3,55 % | 7,70 % | 0,483 | −20,3 % | −5,24 % |
| Mix égal des 6 alternatives | 4,28 % | 10,05 % | 0,461 | −28,0 % | −7,12 % |
| **Actions (mix AP5 renormalisé)** | 6,04 % | 13,54 % | 0,497 | −36,0 % | −9,12 % |
| **Cash (BNS)** | 3,07 % | 7,44 % | 0,434 | −20,9 % | −5,04 % |
| **Oblig. mondiales seules → mix égal (suisses gardées)** | 4,07 % | 9,05 % | 0,479 | −24,9 % | −6,35 % |

Sharpe par dose (25/50/75/100 % ; les colonnes de pire perte sont dans le CSV) :

| Benchmark | 25 % | 50 % | 75 % | 100 % |
|---|---|---|---|---|
| Obligations → actions | 0,489 | 0,494 | 0,496 | 0,497 |
| Obligations → cash | 0,474 | 0,458 | 0,447 | 0,434 |
| Oblig. mondiales seules → mix égal | 0,484 | 0,482 | 0,482 | 0,479 |

*Lecture : le mix d'alternatives ne bat pas de simples actions en Sharpe (0,46 < 0,50) — son
surplus de rendement est surtout du risque de marché ; il bat en revanche le cash (0,43) ; et le
remplacement **asymétrique** (mondiales seulement) préserve le Sharpe de l'AP5 (0,48) avec un
downside moins dégradé que le remplacement total.*

**Source :** `analysis/benchmark_portfolios.csv` et `benchmark_portfolios_sweep.csv` · **Code :**
`src/benchmark_portfolios.py:43-51` (`world_only_book`), `:54-58` (définition des trois
benchmarks), `:61-90` (`main`).

## 9. Robustesse statistique — bootstrap (3 000 rejeux)

Différences (remplacement − AP5). « P(…) » = probabilité que la différence aille dans ce sens.

| Palier | P(ΔCAGR>0) | ΔSharpe [5 % ; 95 %] | P(ΔSharpe>0) | P(pire drawdown) | P(pire CVaR95) | P(pire CVaR90) |
|---|---|---|---|---|---|---|
| 10 % | 83 % | [−0,016 ; +0,016] | 44 % | 82 % | 98,0 % | 98,0 % |
| 20 % | 84 % | [−0,031 ; +0,031] | 45 % | 83 % | 99,8 % | 99,5 % |
| 30 % | 82 % | [−0,046 ; +0,043] | 42 % | 85 % | 100 % | 99,9 % |
| 50 % | 84 % | [−0,072 ; +0,068] | 42 % | 87 % | 100 % | 100 % |
| 100 % | 82 % | [−0,137 ; +0,106] | 36 % | 92 % | 100 % | 100 % |

**Source :** `analysis/robustness_bootstrap_ci.csv` · **Code :** `src/robustness.py:83-118`
(`bootstrap_ci`), écriture `:210`.

## 10. Robustesse — matrice de sensibilité

La conclusion survit-elle en changeant les hypothèses ? `partial_ge_AP5` = le remplacement partiel
(20 %) fait-il au moins aussi bien que l'AP5 en Sharpe ? `full_worse_CVaR95` = le remplacement
total aggrave-t-il la perte extrême ?

| Spécification | AP5 Sharpe | 20 % Sharpe | 100 % Sharpe | 20 % ≥ AP5 ? | 100 % pire CVaR ? |
|---|---|---|---|---|---|
| Bande ±5 % | 0,481 | 0,477 | 0,458 | non | oui |
| Bande ±8 % (base) | 0,483 | 0,482 | 0,461 | non | oui |
| Bande ±10 % | 0,480 | 0,475 | 0,461 | non | oui |
| Bande ±15 % | 0,474 | 0,482 | 0,461 | **oui** | oui |
| Bande ±20 % | 0,494 | 0,479 | 0,464 | non | oui |
| Coûts 0 pb | 0,484 | 0,482 | 0,462 | non | oui |
| Coûts 50 pb | 0,480 | 0,478 | 0,459 | non | oui |
| HY/EM **non couverts** | 0,483 | 0,476 | 0,442 | non | oui |
| Depuis 2010 (sans 2008-09) | 0,621 | 0,628 | 0,623 | **oui** | oui |

*Le remplacement total aggrave la pire perte **et** la CVaR dans **toutes** les spécifications.*
**Source :** `analysis/robustness_sensitivity.csv` · **Code :** `src/robustness.py:120-159`
(`sensitivity`), écriture `:211`.

## 11. Robustesse — bandes par catégorie vs par constituant

| Architecture | AP5 (CAGR/Sharpe/MaxDD) | 20 % | 100 % | Nb rééquilibrages (AP5/20/100) |
|---|---|---|---|---|
| Par **catégorie** (principale) | 3,5 % / 0,483 / −20,3 % | 3,7 % / 0,482 / −21,9 % | 4,3 % / 0,461 / −28,0 % | 36 / 37 / 37 |
| Par **constituant** | 3,5 % / 0,475 / −20,4 % | 3,6 % / 0,475 / −21,8 % | 4,3 % / 0,460 / −27,9 % | 61 / 92 / 96 |

*Beaucoup plus d'opérations en granulaire, mais résultats quasi identiques → la conclusion ne
dépend pas de l'architecture.* **Source :** `analysis/robustness_granular_vs_category.csv` ·
**Code :** `src/robustness.py:161-177` (`granular_vs_category`), écriture `:212`.

## 12. Robustesse — longueur des blocs du bootstrap

| Longueur de bloc | P(20 % pire CVaR95) | P(100 % pire CVaR95) | P(20 % ΔSharpe>0) |
|---|---|---|---|
| 3 mois | 99,7 % | 100 % | 46,9 % |
| 6 mois | 99,8 % | 100 % | 44,9 % |
| 12 mois | 99,8 % | 100 % | 44,0 % |

**Source :** `analysis/robustness_block_length.csv` · **Code :** `src/robustness.py:203-208`
(boucle sur `bootstrap_ci`), écriture `:214`.

## 13. Comportement en crise (rendement total, net de frais)

| Fenêtre de crise | AP5 | 20 % | 50 % | 100 % |
|---|---|---|---|---|
| Krach COVID 2020 (janv.–avr.) | −6,08 % | −6,91 % | −8,17 % | −10,29 % |
| Choc de taux 2022 (déc.21–oct.22) | −11,66 % | −10,57 % | −9,01 % | −6,09 % |
| Stress bancaire 2023 (févr.–mai) | +0,03 % | −0,27 % | −0,72 % | −1,39 % |

**Source :** `analysis/stress_periods.csv` · **Code :** `src/robustness.py:179-192`
(`stress_table`), écriture `:213`.

## 14. Récapitulatif — chaque résultat, sa source et son code

| Résultat | Fichier CSV | Code (fonction) |
|---|---|---|
| Validation / tracking error | `ap5_validation.csv` | `analysis_2008.py:112-146` |
| Validation par bande | `ap5_validation_band_sensitivity.csv` | `analysis_2008.py:149-162` |
| Performance par actif | `descriptive_stats.csv` | `analysis_2008.py:164-182` |
| Performance par palier 10 % | `perf_full_net.csv` | `analysis_2008.py:99-108` |
| Poids par palier | `book_weights.csv` | `analysis_2008.py:391` |
| Obligations par régime | `bond_sleeve_by_regime.csv` | `analysis_2008.py:230-242` |
| Performance par régime | `regime_*.csv` | `analysis_2008.py:216-228` |
| Redondance obligations | `results_manifest.json` | `analysis_2008.py:184-201` |
| Étape A (une alternative) | `single_alt_full_replacement.csv` | `single_alternatives.py:47-58` |
| Étape A (par dose) | `single_alt_sweep.csv` | `single_alternatives.py:60-71` |
| Mélanges (trié vs égal) | `curated_vs_naive.csv` | `analysis_2008.py:337-349` |
| Benchmarks (actions / cash / asymétrique) | `benchmark_portfolios.csv` (+ `_sweep`) | `benchmark_portfolios.py:43-90` |
| Optimisations (perf) | `appendix_optimisation_perf.csv` | `appendix_optimization.py:52-87` |
| Optimisations (poids) | `appendix_optimisation_weights.csv` | `appendix_optimization.py:52-87` |
| Bootstrap | `robustness_bootstrap_ci.csv` | `robustness.py:83-118` |
| Sensibilité | `robustness_sensitivity.csv` | `robustness.py:120-159` |
| Catégorie vs constituant | `robustness_granular_vs_category.csv` | `robustness.py:161-177` |
| Longueur de bloc | `robustness_block_length.csv` | `robustness.py:203-208` |
| Crises | `stress_periods.csv` | `robustness.py:179-192` |
| **Synthèse officielle** | `results_manifest.json` | `analysis_2008.py:405-432` |

> **Note.** Le dépôt contient aussi d'anciens fichiers de l'étude 2019 (`walkforward_*.csv`,
> `montecarlo_*.csv`, `efficient_frontier.csv`, `asset_stats.csv`, `portfolio_*.csv`,
> `rebalancing_comparison.csv`, `stress_windows.csv`) : ils sont **périmés** et **remplacés** par
> l'étude 2008–2026 ci-dessus. Ne pas les citer.

Le détail « quelle ligne fait quoi » est dans `reports/tracabilite_code_FR.md`.
