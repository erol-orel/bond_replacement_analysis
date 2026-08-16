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

## Validation — la réplication est fiable

Reconstitution de l'AP5 (indices → Smart Rebalancing → net de frais, dérive d'allocation réelle
de VZ) contre la **VNI réelle du produit VZ**, 2019–2026 : **corrélation 0,955**, **tracking
error 2,35 %/an**, suivi visuel fidèle à travers le COVID, la chute de 2022 et la reprise. La
TE résiduelle provient du volet actions étrangères (indice de prix USD converti en CHF) —
**elle s'annule dans toutes les comparaisons AP5-vs-remplacement**, le cœur identique partout.

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

**Sur le cycle complet, pas de repas gratuit** : le remplacement intégral fait passer le
rendement de 3,43 % à 4,30 %/an mais le drawdown de −21 % à −28 %, avec un **ratio de Sharpe
quasi inchangé** (pic léger ~0,49 vers 20–40 %). La valeur du remplacement est **conditionnelle
au régime**.

## Recommandation

- **Ne pas remplacer intégralement.** Un remplacement **partiel (≈ 20–40 %)** se situe au pic
  de Sharpe, capte le gain de régime (R2/R4) et conserve un cœur obligataire pour les fuites
  vers la qualité (chocs de type R1).
- **Le choix des instruments compte autant que le montant.** Un panier **curated** (haut
  rendement 35 / dette émergente 30 / or 20 / infrastructure 15, écartant les deux
  perdants — matières premières et managed futures) **domine** le panier naïf : Sharpe
  **0,53 vs 0,47** à 100 % de remplacement, **au-dessus de l'AP5 (0,47)**.
- **Conserver la structure obligataire** (suisses + mondiales, larges + courtes 1-5).
- **Écartés (avec justification)** : ILS, private equity/credit et fonds hypothécaires suisses
  — aucun ne satisfait le critère *investissable / liquide / net de frais* (pas de série
  publique valorisée au marché).

## Note d'honnêteté & annexe

Matières premières (−1,6 %/an) et managed futures (−0,7 %/an) ont **perdu de l'argent** sur
2008–2026 ; le panier naïf les porte à poids égal — rien n'est trié sur le volet. L'optimisation
est reléguée en **annexe** (jugée trop théorique) : même optimisée en échantillon, la poche
minimum-variance/CVaR se met **100 % en obligations mondiales courtes (1-5)** et la poche
max-Sharpe conserve des obligations suisses + une allocation en or plafonnée — **aucun
optimiseur n'abandonne les obligations**. Proxys ETF/fonds investissables (non les fonds VZ exacts) ; fréquence
mensuelle ; un seul chemin historique. Reproduction académique, pas un conseil en placement.
