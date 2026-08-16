# Résumé exécutif — Alternatives aux obligations dans la construction de portefeuille

**Mémoire de master, HEC Lausanne · Réplication du mandat VZ AP5 · CHF, mensuel, rendement
total net de frais · 2008–2026**

---

## Problématique (reformulée)

Remplacer la **poche obligataire** du portefeuille VZ AP5 par des actifs alternatifs **sur
l'ensemble de la période**, puis analyser le résultat **régime par régime**. Le problème
n'est pas seulement les taux bas : lorsque les taux *montent*, les obligations perdent
aussi. Lire l'analyse par régime de la BNS supprime le besoin d'un seuil « taux bas »
contesté.

## Données (réelles, pas de proxys synthétiques du cœur)

Indices **Bloomberg** des composantes **exactes** du mandat AP5 (VZ Kundendoku, planche 5) :
actions suisses **SPI 11 / SLI 12 / SPI Extra 2**, actions monde **MSCI World 19 / Small 3 /
EM 3**, obligations suisses **SBI AAA-BBB 10,8 / 1-5 6**, obligations monde **Global Aggregate
couvert CHF 16,8 / 1-5 8,4**, immobilier SXI 5, liquidités 3. Taux **BNS + Fed** mensuels et la
**VNI réelle du produit VZ VVIA**. Frais : **0,12 % (produit) + 1,25 % (gestion) = 1,37 %/an**.
**Poche obligataire = 42 %** (suisses 16,8 % + mondiales 25,2 %), conservant sa structure
duration longue / courte (1-5).

## Validation — un benchmark stylisé (non une réplique exacte)

Reconstitution de l'AP5 (indices → rebalancement par bandes → net de frais, dérive
d'allocation réelle de VZ) contre la **VNI réelle du produit VZ**, 2019–2026 : **corrélation
0,955**, régression **β 0,97 / α −0,35 %/an / R² 0,91**, **tracking error 2,35 %/an**, écart
cumulé +25,1 % vs +21,1 %. La TE résiduelle provient surtout du volet actions étrangères
(indice de prix USD converti en CHF) ; ce cœur est commun à tous les portefeuilles comparés,
donc son biais est partagé (effet de second ordre sous rebalancement par bandes). On la traite
comme un **benchmark stylisé**, non une reconstruction exacte des transactions de VZ.

## Le problème obligataire, par régime — la duration compte (fig. 05)

| Régime BNS | Oblig. CH large | Oblig. CH 1-5 | Oblig. monde large | Oblig. monde 1-5 |
|---|---|---|---|---|
| **R1 2008–14** — taux bas positifs | **+4,0 %** | +2,5 % | **+4,1 %** | +2,5 % |
| **R2 2015–22** — taux négatifs | −0,8 % | −0,4 % | −0,6 % | −0,7 % |
| **R3 2022–24** — hausses | +2,9 % | +1,5 % | **−2,0 %** | **−0,8 %** |
| **R4 2024–26** — assouplissement | +2,4 % | +1,9 % | −0,3 % | +0,5 % |

Les obligations n'ont joué leur rôle défensif **que lorsque les taux baissaient (R1)**. En
régime négatif (R2) la poche a rapporté ≈ 0 ; lorsque les taux **montent (R3)**, les obligations
mondiales larges perdent **2 %/an** — mais la tranche **courte (1-5) ne perd que −0,8 %** : la
duration est le canal. Suisses/mondiales corrélées (**0,79**) mais **non redondantes**.

## Le remplacement est-il payant ? — par régime (rendement annualisé net)

| Régime | AP5 | 20 % | 50 % | 100 % | Lecture |
|---|---|---|---|---|---|
| R1 2008–14 (oblig. fortes) | **3,6** | 3,6 | 3,4 | 3,0 | le remplacement **coûte** |
| R2 2015–22 (négatif) | 4,0 | 4,5 | 5,1 | **6,1** | le remplacement **gagne** |
| R3 2022–24 (hausses) | 3,1 | 2,8 | 2,7 | 2,8 | **neutre** |
| R4 2024–26 (assoupl.) | 5,1 | 5,9 | 6,9 | **8,3** | le remplacement **gagne** |

**Résultat central — la courbe de compromis** : plus on remplace, plus le rendement, la
volatilité et le drawdown augmentent, pour un **Sharpe quasi inchangé** (CAGR 3,43 %→4,30 %,
MaxDD −20,6 %→−27,7 %, Sharpe ≈0,47).

**Statistiques (bootstrap par blocs, 3 000 tirages)** : **aucun** niveau de remplacement ne
produit un gain de Sharpe distinguable de zéro (IC de ΔSharpe englobent 0). Le drawdown penche
vers le pire mais son IC à 95 % **inclut encore zéro** (*suggestif*) ; en revanche la **perte
extrême (CVaR) est pire avec ≈95–100 % de probabilité** dès 20 % de remplacement (*établi*).

**Dépend du type de crise** : le remplacement a *nui* lors du choc déflationniste 2020
(−10,4 % vs AP5 −6,9 %) mais *aidé* lors du choc de taux 2022 (−6,6 % vs −11,9 %).

## Recommandation

- **On ne remplace pas « les obligations » mais *une partie de ce qu'elles font*** (portage,
  une part de diversification/inflation) — **pas** la duration ni la « fuite vers la qualité »,
  d'où la dégradation du risque de queue.
- **Privilégier un remplacement partiel plutôt qu'intégral.** Le pic de Sharpe (estimation
  ponctuelle) se situe vers **20 %**, mais 20/30/40 % ne sont **pas distinguables
  statistiquement**. Le remplacement intégral n'est **pas** soutenu (perte extrême fiablement
  pire, pas de gain de Sharpe fiable, perte de la protection « fuite vers la qualité » de 2020).
- **Conserver la structure obligataire** (suisses + mondiales, larges + courtes 1-5).
- **Le choix des instruments compte** : un panier « curated » (HR 35 / dette ém. 30 / or 20 /
  infra 15) fait mieux (Sharpe 0,53), mais c'est un résultat **ex-post exploratoire**, non la
  recommandation — à valider hors échantillon.
- **Écartés (avec justification)** : ILS, private equity/credit et fonds hypothécaires suisses
  — aucun ne satisfait le critère *investissable / liquide / net de frais*.
- **Robustesse** : la conclusion survit à toutes les variations (bande, coûts, couverture,
  raccord 2008-09).

## Note d'honnêteté & annexe

Matières premières (−1,6 %/an) et managed futures (−0,7 %/an) ont **perdu de l'argent** sur
2008–2026 ; le panier naïf les porte à poids égal — rien n'est trié sur le volet. L'optimisation
est reléguée en **annexe** (jugée trop théorique) : même optimisée en échantillon, la poche
minimum-variance/CVaR se met **100 % en obligations mondiales courtes (1-5)** et la poche
max-Sharpe conserve des obligations suisses + une allocation en or plafonnée — **aucun
optimiseur n'abandonne les obligations**. Proxys ETF/fonds investissables (non les fonds VZ exacts) ; fréquence
mensuelle ; un seul chemin historique. Reproduction académique, pas un conseil en placement.
