# Alternatives aux obligations dans un portefeuille suisse

### Stratégies de diversification pour un portefeuille en CHF — mandat VZ AP5 · mensuel, net de frais · février 2008 – juin 2026

*Version principale de la thèse empirique. Elle reprend la structure claire du premier document
de travail (analyse candidat par candidat, tableau de comparaison, matrice de stress, réallocation
proposée), mais **tous les chiffres qualitatifs d'origine sont remplacés par les résultats réels**
calculés sur données Bloomberg 2008–2026 (`analysis/results_manifest.json`, `analysis/*.csv`).
On dit « obligations » plutôt que « poche obligataire ».*

---

## Résumé exécutif

Un portefeuille équilibré en CHF (VZ **Anlageprofil 5**) détient **42 % en obligations**
(16,8 % suisses + 25,2 % mondiales) — le plus gros bloc du portefeuille. En régime de taux bas ou
négatifs, ces obligations rapportent peu, et lorsque les taux **montent** (2022), elles perdent.
La thèse se demande : *peut-on remplacer une partie des obligations par d'autres actifs
investissables, et à quel prix en risque ?*

Six alternatives investissables, avec un historique complet depuis 2008, sont évaluées : **or,
matières premières, infrastructures, managed futures (CTA), obligations à haut rendement (HY),
dette émergente (EM)**. Chacune est d'abord testée **seule**, puis en **mélange**, puis via une
**allocation optimisée**.

### Conclusions clés

- **Seule l'or**, prise isolément, améliore le rendement ajusté au risque par rapport à l'AP5
  (Sharpe **0,60** contre 0,48), et sans aggraver la pire perte.
- **Les matières premières et les managed futures ont perdu de l'argent** sur 2008–2026 : ils
  dégradent tout portefeuille qui les contient.
- Un **mélange équipondéré** des six alternatives fait **moins bien** que garder les obligations
  (Sharpe 0,46), justement parce qu'il inclut ces deux perdants.
- Un **mélange trié** (HY 35 / EM 30 / or 20 / infra 15), qui écarte les perdants, remonte à
  Sharpe 0,52 — mais c'est un résultat *a posteriori*, à valider hors échantillon.
- Même un **optimiseur** libre de tout enlever **garde la plupart des obligations** et n'ajoute
  qu'un peu d'or.

### Recommandation

**Ne pas remplacer les obligations en totalité.** Le remplacement augmente le rendement mais aussi
la volatilité et surtout les **pertes extrêmes**, sans amélioration fiable du rendement ajusté au
risque. Le seul ajout historiquement utile est **un peu d'or, à côté des obligations, pas à leur
place** — et il s'agit d'un pari concentré sur un échantillon favorable, à stresser avant tout
usage réel. Le remplacement doit se comprendre comme un **choix de budget de risque**, non comme la
découverte d'un actif meilleur que les obligations.

## I. Structure du portefeuille

Le mandat AP5 (profil 5 de VZ) est réparti ainsi : **25 % actions suisses**, **25 % actions
mondiales**, **16,8 % obligations suisses**, **25,2 % obligations mondiales (couvertes CHF)**,
**5 % immobilier**, **3 % liquidités**. Les obligations à traiter représentent **42 %** du total
— le plus gros bloc, et la partie la plus touchée par les régimes de taux bas suisses. Le cœur
actions / immobilier / liquidités (58 %) reste **inchangé** ; seul le bloc de 42 % obligations est
remplacé.

## II. Les régimes de taux depuis 2008

Plutôt qu'un seuil « taux bas » arbitraire, on découpe la période en **quatre régimes de la BNS**,
ce qui permet de lire directement le comportement des obligations dans chaque environnement :

| Régime | Période | Taux directeur BNS | Contexte |
|---|---|---|---|
| **R1** | 2008–2014 | +2,75 % → −0,25 % | taux bas positifs, baisse post-crise |
| **R2** | 2015–2022 | −0,75 % | taux négatifs (NIRP) |
| **R3** | 2022–2024 | −0,25 % → +1,75 % | hausses rapides |
| **R4** | 2024–2026 | +1,50 % → 0,00 % | assouplissement |

Comportement des obligations par régime (rendement annualisé) : fortes en R1 (+4 %/an), quasi
nulles en R2, et en R3 les obligations **mondiales larges perdent −2,9 %/an** tandis que les
**suisses restent positives** (+1,6 %). *Les obligations ne « paient » que dans certains régimes* —
c'est le cœur du problème.

## III. Les fonctions des obligations

Avant de chercher des remplaçants, il faut fixer ce que les obligations **font** dans ce
portefeuille. Tout remplacement doit en préserver le plus possible :

- **F1 — Refuge / diversification.** Monter quand les actions chutent (fuite vers la qualité).
- **F2 — Revenu / portage.** Verser un coupon régulier.
- **F3 — Amortisseur de volatilité.** Faible volatilité qui stabilise le portefeuille.
- **F4 — Liquidité.** Se vendre vite et sans décote.
- (**Duration** — sensibilité aux taux, qui sous-tend F1 et F3.)

Aucune alternative ne reproduit les cinq à la fois : c'est la tension que l'analyse mesure. On
classe les candidats de **plus liquide (meilleur) à moins liquide (pire)**.

## IV. Les candidats au remplacement

Pour chaque candidat : (i) ce que c'est, (ii) rendement réel 2008–2026, (iii) ajustement
variance-covariance (corrélations aux actions et aux obligations), (iv) ressemblances avec les
obligations, (v) différences et risques, (vi) meilleur usage. Sharpe = excès sur le cash CHF ;
« seul à 100 % » = Sharpe du portefeuille si l'on remplace **toutes** les obligations par ce seul
actif.

### #1 — Or (ETF adossés à l'or physique, part CHF) · liquidité ★★★★★

- **Ce que c'est :** or physique alloué via ETF suisses (ZKB, UBS, Swisscanto). La Suisse est le
  hub mondial du raffinage — accès CHF naturel, marché très profond.
- **Rendement 2008–2026 :** **+6,1 %/an**, volatilité 16,4 %, pire perte −38 %. **Seul à 100 % :
  Sharpe 0,60** (le meilleur des candidats).
- **Variance-covariance :** corrélation aux actions **−0,02** (diversificateur quasi parfait), aux
  obligations +0,24.
- **Ressemblances :** refuge de crise puissant (2008, 2020) ; bénéficie des taux réels bas, comme
  les obligations ; aucun risque de crédit (préserve **F1**).
- **Différences :** **aucun revenu / portage** (échoue **F2**) ; volatilité proche des actions
  (affaiblit **F3**) ; pas de duration ; prix spéculatif à court terme.
- **Meilleur usage :** 3–6 % comme **couverture de régime**, à côté des obligations — pas un
  substitut structurel.

### #2 — Obligations à haut rendement (HY, couvert CHF) · liquidité ★★★★★

- **Ce que c'est :** obligations d'entreprises sous-investment-grade (proxy HYG couvert CHF).
- **Rendement 2008–2026 :** **+3,9 %/an**, volatilité 10,3 %, pire perte −29 %. **Seul à 100 % :
  Sharpe 0,48** (≈ AP5).
- **Variance-covariance :** corrélation aux actions **+0,56** (élevée), aux obligations +0,49.
- **Ressemblances :** vrai **revenu / portage** (préserve **F2**) ; structure juridiquement
  obligataire.
- **Différences :** se comporte en partie comme des actions (corr 0,56) — mauvais **F1** ; pire
  perte plus profonde que les obligations d'État.
- **Meilleur usage :** pilier du panier trié (le **portage**), poids important.

### #3 — Dette émergente (EM, couvert CHF) · liquidité ★★★★

- **Ce que c'est :** obligations souveraines/corporate de pays émergents (proxy EMB couvert CHF).
- **Rendement 2008–2026 :** **+3,3 %/an**, volatilité 11,5 %, pire perte −28 %. **Seul à 100 % :
  Sharpe 0,47**.
- **Variance-covariance :** corrélation aux obligations **+0,65** — **le plus « obligataire » des
  candidats** ; aux actions +0,39.
- **Ressemblances :** revenu / portage ; profil de duration proche des obligations (le meilleur
  substitut *structurel*).
- **Différences :** risque pays et devise ; pire perte plus profonde ; moins de refuge en crise.
- **Meilleur usage :** pilier du panier trié (portage + proximité obligataire).

### #4 — Infrastructures cotées (global core, couvert CHF) · liquidité ★★★★

- **Ce que c'est :** actions d'infrastructures (péages, énergie, utilities ; proxy IGF).
- **Rendement 2008–2026 :** **+4,0 %/an**, volatilité 14,8 %, pire perte −45 %. **Seul à 100 % :
  Sharpe 0,41**.
- **Variance-covariance :** corrélation aux actions **+0,72** — **se comporte comme des actions** ;
  aux obligations +0,27.
- **Ressemblances :** revenu réel, exposition inflation.
- **Différences :** très corrélé aux actions (mauvais **F1**) ; pire perte profonde (−45 %).
- **Meilleur usage :** petit poids pour l'exposition « actifs réels / inflation », pas comme
  diversificateur.

### #5 — Managed futures / trend-following (CTA liquides) · liquidité ★★★★

- **Ce que c'est :** fonds systématiques suivant les tendances sur tous marchés (proxy RYMFX).
- **Rendement 2008–2026 :** **−0,8 %/an** (a **perdu de l'argent**), volatilité 13,8 %, pire perte
  −47 %. **Seul à 100 % : Sharpe 0,32**.
- **Variance-covariance :** corrélation aux actions +0,25, aux obligations −0,18 (décorrélé).
- **Ressemblances :** décorrélation ; potentiel de gain en crise prolongée (a aidé en 2022).
- **Différences :** rendement **négatif** sur la période ; aucun revenu ; longues périodes de
  sous-performance.
- **Meilleur usage :** **écarté** du panier — perd de l'argent en moyenne malgré la décorrélation.

### #6 — Matières premières (large, non couvert) · liquidité ★★★★

- **Ce que c'est :** panier diversifié de matières premières (proxy DBC).
- **Rendement 2008–2026 :** **−1,6 %/an** (a **perdu de l'argent**), volatilité 18,9 %, pire perte
  **−76 %**. **Seul à 100 % : Sharpe 0,24** (le pire).
- **Variance-covariance :** corrélation aux actions +0,39, aux obligations −0,25.
- **Ressemblances :** couverture d'inflation ; faible corrélation aux obligations.
- **Différences :** rendement **négatif**, volatilité extrême, pire perte catastrophique (−76 %) ;
  aucun revenu.
- **Meilleur usage :** **écarté** du panier — le plus mauvais candidat sur la période.

### Candidats considérés puis écartés

- **Obligations convertibles :** hybride actions ; la corrélation aux actions monte en marché
  haussier *et* en krach — échoue le test de diversification exactement quand on en a besoin ;
  historique propre seulement depuis 2009. *Rehausseur de rendement, pas substitut obligataire.*
- **Tranches CLO AAA :** intéressantes en théorie (senior, taux variable), mais **aucune série
  Bloomberg fiable dans nos données**, et le coût de couverture USD→CHF ronge le rendement.
  *Non retenues faute de données propres.*
- **ILS / obligations catastrophe :** pas d'historique public total-return propre, semi-liquides.
  *Écartées (critère investissable / liquide non satisfait).*
- **Private credit / dette privée :** illiquide, VNI lissée (volatilité artificiellement basse),
  blocage 4–7 ans. *Écartée.*

## V. Tableau de comparaison principal (2008–2026, par actif)

Sharpe = excès sur cash CHF. Les quatre premières lignes sont les obligations à remplacer.

| Actif (proxy) | CAGR | Vol | Sharpe | Pire perte | Corr. actions | Corr. oblig. |
|---|---|---|---|---|---|---|
| Obligations suisses (large) | 1,8 % | 3,6 % | 0,50 | −16 % | — | — |
| Obligations suisses (1–5 a) | 1,1 % | 1,7 % | 0,66 | −7 % | — | — |
| Obligations monde (large) | 1,1 % | 3,5 % | 0,30 | −18 % | — | — |
| Obligations monde (1–5 a) | 0,6 % | 1,8 % | 0,31 | −9 % | — | — |
| **Or** | 6,1 % | 16,4 % | 0,44 | −38 % | **−0,02** | +0,24 |
| **Haut rendement (HY)** | 3,9 % | 10,3 % | 0,41 | −29 % | +0,56 | +0,49 |
| **Dette émergente (EM)** | 3,3 % | 11,5 % | 0,33 | −28 % | +0,39 | **+0,65** |
| **Infrastructures** | 4,0 % | 14,8 % | 0,34 | −45 % | +0,72 | +0,27 |
| **Managed futures** | −0,8 % | 13,8 % | 0,01 | −47 % | +0,25 | −0,18 |
| **Matières premières** | −1,6 % | 18,9 % | 0,00 | −76 % | +0,39 | −0,25 |
| *Rappel : actions monde* | 8,6 % | 18,7 % | 0,53 | −42 % | 1,00 | — |

**Ce que le tableau dit déjà :** l'or est le seul vrai **diversificateur** (corr ≈ 0 aux actions) ;
la dette émergente est le plus **obligataire** (corr 0,65 aux obligations) ; HY et infrastructures
sont **trop proches des actions** ; matières premières et managed futures ont **perdu de l'argent**.

## VI. Matrice de stress par crise (rendement total, net de frais)

| Fenêtre de crise | AP5 (0 %) | Remplacement 100 % (mélange égal) | Lecture |
|---|---|---|---|
| Krach COVID 2020 (janv.–avr.) | **−6,1 %** | −10,3 % | obligations protègent → remplacer **nuit** |
| Choc de taux 2022 (déc.21–oct.22) | −11,7 % | **−6,1 %** | obligations *et* actions chutent → remplacer **aide** |
| Stress bancaire 2023 (févr.–mai) | 0,0 % | −1,4 % | léger avantage aux obligations |

Les deux grandes crises pointent en sens opposés : le remplacement **change contre quelle crise on
est protégé**, il ne supprime pas le risque de crise.

## VII. Réallocation proposée — portefeuille cible

On procède en trois étapes, du plus simple au plus avancé. Voici d'abord la **carte de tout ce qui
est testé** — ce qui est remplacé, par quoi, et de combien (le cœur actions/immobilier/liquidités
de 58 % ne bouge jamais) :

| Portefeuille | Ce qui est remplacé | Par quoi | De combien |
|---|---|---|---|
| **AP5** (référence) | rien | — | 0 % |
| **Étape A** (× 6) | obligations | **une seule** alternative | 0 → 100 % (pas de 10 %) |
| **Étape B — égal** | obligations | mélange équipondéré des 6 | 0 → 100 % |
| **Étape B — trié** | obligations | HY 35 / EM 30 / or 20 / infra 15 | 0 → 100 % |
| **Étape C** | obligations + poche | poids choisis par l'optimiseur | en échantillon |

### Étape A — remplacer les obligations par UNE alternative à la fois

En remplaçant **100 % des obligations** par un seul actif (`analysis/single_alt_full_replacement.csv`),
classé par Sharpe :

| 100 % des obligations → | CAGR | Sharpe | Pire perte |
|---|---|---|---|
| **Or seul** | 5,9 % | **0,60** | −21 % |
| **AP5 (référence)** | 3,6 % | **0,48** | −20 % |
| Haut rendement seul | 4,6 % | 0,48 | −31 % |
| Dette émergente seule | 4,4 % | 0,47 | −26 % |
| Infrastructures seules | 4,6 % | 0,41 | −39 % |
| Managed futures seuls | 2,9 % | 0,32 | −26 % |
| Matières premières seules | 2,4 % | 0,24 | −39 % |

**Conclusion de l'Étape A :** seule l'or, isolée, bat la référence sur le Sharpe (voir **figure
T1**). Tous les autres font aussi bien ou moins bien, et deux perdent de l'argent.

Et si l'on ne remplace qu'**une partie** des obligations (25 / 50 / 75 %) par une seule
alternative, le classement ne change pas — l'or domine à toutes les doses, les perdants restent
derrière l'AP5 (**figure T3**) :

| Sharpe si l'on remplace… | 25 % | 50 % | 75 % | 100 % |
|---|---|---|---|---|
| par de l'or | 0,54 | 0,58 | 0,60 | 0,60 |
| par du haut rendement | 0,49 | 0,49 | 0,48 | 0,48 |
| par de la dette émergente | 0,48 | 0,49 | 0,48 | 0,47 |
| par des infrastructures | 0,47 | 0,44 | 0,43 | 0,41 |
| par des managed futures | 0,45 | 0,41 | 0,36 | 0,32 |
| par des matières premières | 0,41 | 0,35 | 0,29 | 0,24 |
| *(rappel AP5 = 0,48)* | | | | |

### Étape B — remplacer par un MÉLANGE (et pourquoi ce mélange)

Un actif unique est fragile (tous les œufs dans le même panier, surtout l'or). On diversifie donc.
L'Étape A dit **exactement comment composer le mélange** :

| Mélange (100 % des obligations remplacé) | CAGR | Sharpe | Pire perte |
|---|---|---|---|
| Équipondéré (les 6) | 4,3 % | 0,46 | −28 % |
| **Trié (HY 35 / EM 30 / or 20 / infra 15)** | 4,9 % | **0,52** | −28 % |

Le mélange **équipondéré** fait *moins bien* que garder les obligations (0,46 < 0,48) car il donne
autant de poids aux matières premières et aux managed futures — les deux perdants. Le mélange
**trié** écarte ces deux-là et pondère les actifs de portage (HY, EM) plus l'or diversificateur :
Sharpe 0,52.

> **Justification des poids :** HY et EM sont les deux actifs de **portage** qui reproduisent le
> mieux ce que font les obligations (35 % + 30 %) ; l'or est le seul à améliorer le rendement
> ajusté au risque seul, d'où **20 %** comme diversificateur ; l'infrastructure ajoute un peu
> d'exposition réelle (15 %). Matières premières et managed futures sont **exclus**.
>
> **Réserve importante :** ce mélange trié est choisi *après avoir vu* les résultats — il est
> **exploratoire**, pas une promesse. À valider hors échantillon.

### Étape C — une allocation optimisée (avancée)

On laisse enfin un optimiseur choisir les poids des 42 % pour maximiser le Sharpe en échantillon
(`analysis/appendix_optimisation_*.csv`) — un **majorant optimiste**, non implémentable tel quel.

| Optimisé (en échantillon) | CAGR | Sharpe | Ce qu'il choisit |
|---|---|---|---|
| **Max-Sharpe** | 4,4 % | **0,56** | ≈ 30 % obligations suisses + 12 % or (garde les obligations !) |
| Variance / CVaR minimale | 3,3 % | 0,46 | 42 % obligations monde courtes (tout en obligations) |

**Leçon de l'Étape C :** même libre de tout retirer, l'optimiseur **garde une large part
d'obligations** et n'ajoute qu'un peu d'or. Il ne remplace jamais les obligations en totalité —
même message que les Étapes A et B, par une méthode totalement différente.

### Recommandation finale

Le résultat central se lit d'un coup d'œil sur la **courbe de compromis** (**figure T2**) : chaque
palier de remplacement pousse le portefeuille vers le haut *et* vers la droite — plus de rendement,
mais plus de risque — sans jamais améliorer le Sharpe. Le rendement cumulé (**figure T4**) montre la
même chose : les remplacements finissent plus haut mais avec des chutes plus profondes.

- **Ne pas remplacer les obligations en totalité.** Cela aggrave la pire perte et la perte extrême
  sans gain de Sharpe fiable, et retire la protection de type 2020.
- Un remplacement **partiel** est un **compromis de budget de risque** (plus de rendement contre
  plus de risque baissier), pas une optimisation.
- L'ajout le plus utile historiquement est **un peu d'or, à côté des obligations** — un pari
  concentré, à stresser avant tout usage.
- **Conserver la structure obligataire** (suisses + mondiales, longues + courtes) : elles se
  comportent différemment selon les régimes et ne sont pas redondantes.

## Ce qui reste à faire (travail de rédaction)

L'analyse empirique (données, portefeuilles, résultats, robustesse) est complète et reproductible.
Restent à écrire par l'étudiante : la **revue de littérature**, le **cadre théorique**, les
**références**, l'introduction, la discussion et la conclusion rédigées.
