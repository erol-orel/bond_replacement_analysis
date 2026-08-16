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

Indices **Bloomberg** des composantes réelles du mandat AP5 (SBI AAA-BBB, Bloomberg Global
Aggregate **couvert en CHF**, SPI, MSCI World, SXI Real Estate), taux directeurs **BNS + Fed**
mensuels, et la **performance réelle du produit VZ VVIA**. Frais retenus : **0,12 % (produit)
+ 1,25 % (gestion) = 1,37 %/an**. Poche obligataire = **40,75 %** (mondiales 23,95 % +
suisses 16,8 %).

## Validation — la réplication est fiable

Reconstitution de l'AP5 (indices → Smart Rebalancing → net de frais) contre la **VNI réelle
du produit VZ**, 2019–2026 : **corrélation 0,95**, **tracking error 2,5 %/an**, suivi visuel
fidèle à travers le COVID, la chute de 2022 et la reprise. La TE résiduelle provient du
volet actions étrangères (indice de prix USD converti en CHF) — **elle s'annule dans toutes
les comparaisons AP5-vs-remplacement**, le cœur actions/immobilier/liquidités étant
identique partout.

## Le problème obligataire, par régime (fig. 05)

| Régime BNS | Oblig. suisses | Oblig. mondiales | Liquidités |
|---|---|---|---|
| **R1 2008–14** — taux bas positifs | **+4,0 %** | **+4,1 %** | +0,5 % |
| **R2 2015–22** — taux négatifs | **−0,8 %** | **−0,6 %** | −0,8 % |
| **R3 2022–24** — hausses et palier | +2,9 % | **−2,0 %** | +1,2 % |
| **R4 2024–26** — assouplissement | +2,4 % | −0,3 % | +0,5 % |

Les obligations n'ont joué leur rôle défensif **que lorsque les taux baissaient (R1)**. En
régime négatif (R2) la poche obligataire + liquidités a rapporté ≈ 0 ; lorsque les taux
**montent (R3)**, les obligations mondiales perdent **2 %/an** (duration). Obligations
suisses et mondiales restent corrélées (**0,79**) mais **non redondantes** → conserver les
deux indices.

## Le remplacement est-il payant ? — par régime (rendement annualisé net)

| Régime | AP5 | 33 % | 66 % | 100 % | Lecture |
|---|---|---|---|---|---|
| R1 2008–14 (oblig. fortes) | **4,0** | 3,8 | 3,4 | 3,1 | le remplacement **coûte** |
| R2 2015–22 (négatif) | 4,4 | 5,0 | 5,7 | **6,3** | le remplacement **gagne** |
| R3 2022–24 (hausses) | 2,8 | 2,9 | 2,9 | 2,9 | **neutre** |
| R4 2024–26 (assoupl.) | 5,2 | 6,3 | 7,4 | **8,4** | le remplacement **gagne** |

**Sur le cycle complet, pas de repas gratuit** : le remplacement intégral fait passer le
rendement de 3,74 % à 4,47 %/an mais le drawdown de −19 % à −27 %, avec un **ratio de Sharpe
quasi inchangé (0,51 → 0,49)**. La valeur du remplacement est **conditionnelle au régime**.

## Recommandation

- **Ne pas remplacer intégralement.** Un remplacement **partiel (≈ 33–66 %)** capte
  l'essentiel du gain de régime (R2/R4) tout en limitant le surcroît de drawdown, et
  conserve un cœur obligataire pour les fuites vers la qualité (chocs de type R1).
- **Le choix des instruments compte autant que le montant.** Un panier **curated** (haut
  rendement 35 / dette émergente 30 / or 20 / infrastructure 15, écartant les deux
  perdants — matières premières et managed futures) **domine** le panier naïf : Sharpe
  **0,55 vs 0,49** à 100 % de remplacement, **au-dessus de l'AP5 (0,51)**.
- **Conserver les deux indices obligataires** (suisses plus résilients que mondiaux en R3).

## Note d'honnêteté & annexe

Matières premières (−1,6 %/an) et managed futures (−0,7 %/an) ont **perdu de l'argent** sur
2008–2026 ; le panier naïf les porte à poids égal — rien n'est trié sur le volet. L'optimisation
est reléguée en **annexe** (jugée trop théorique) : même optimisée en échantillon, la poche
minimum-variance/CVaR reste **100 % obligataire** et la poche max-Sharpe conserve des
obligations suisses + une allocation en or plafonnée — **aucun optimiseur n'abandonne les
obligations**. Proxys ETF/fonds investissables (non les fonds VZ exacts) ; fréquence
mensuelle ; un seul chemin historique. Reproduction académique, pas un conseil en placement.
