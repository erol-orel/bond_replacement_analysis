# Guide pas à pas — comprendre et justifier l'analyse

**Mémoire HEC Lausanne · « Alternatives à la poche obligataire dans un portefeuille suisse »
· VZ AP5 · CHF, mensuel, net de frais · 2008–2026**

> But de ce document : expliquer **simplement et une étape à la fois** ce qui a été fait, et
> pourquoi, pour que chaque décision puisse être justifiée. Aucun jargon n'est utilisé sans être
> expliqué en une phrase. Les chiffres cités sont ceux du fichier de résultats officiel
> (`analysis/results_manifest.json`).

---

## 1. L'objectif, en une phrase

Savoir si l'on peut **remplacer la poche obligataire (42 %)** du portefeuille VZ **AP5** par
d'autres actifs (or, matières premières, infrastructures, etc.), et **à quel prix en termes de
risque** — sur toute la période 2008–2026 et selon l'environnement de taux d'intérêt.

Autrement dit : *les obligations posent problème quand les taux montent ; peut-on faire mieux
avec autre chose, sans prendre trop de risque ?*

## 2. Les trois questions (au lieu de cinq hypothèses)

Toute l'analyse tient en **trois questions simples** :

1. **Rendement** — remplacer les obligations change-t-il le **rendement** à long terme ?
2. **Risque** — cela change-t-il le **risque**, surtout les grosses pertes (les baisses profondes
   et les pertes extrêmes) ?
3. **Régime** — la réponse dépend-elle de l'**environnement de taux** (la politique de la BNS) ?

> La question « vaut-il mieux remplacer *un peu* ou *tout* ? » n'est **pas** une quatrième
> hypothèse : c'est une **recommandation** que l'on tire à la fin, une fois les trois questions
> répondues.

## 3. Quelques mots à connaître (une phrase chacun)

| Mot | Ce que ça veut dire, simplement |
|---|---|
| **AP5 / VVIA** | Le profil de placement n°5 de VZ (≈50 % actions, 42 % obligations, immobilier, liquidités). |
| **Poche obligataire (42 %)** | La partie « obligations » du portefeuille : obligations suisses (16,8 %) + mondiales (25,2 %). |
| **Rendement (CAGR)** | Le gain moyen par an sur toute la période. |
| **Volatilité** | À quel point la valeur bouge : plus c'est haut, plus ça monte et descend fort. |
| **Drawdown (max)** | La pire baisse depuis un sommet : « combien on a perdu au pire moment ». |
| **Perte extrême (CVaR)** | La perte moyenne dans les **pires** mois (les 5 % de mois les plus mauvais). |
| **Sharpe** | Le rendement **rapporté au risque** : « combien de rendement par unité de risque ». Plus haut = mieux. |
| **Net de frais** | Après avoir enlevé les frais (voir étape 5). |

## 4. Les étapes de l'analyse, une par une

Chaque étape dit **ce qu'on a fait**, **pourquoi**, et **ce que ça a donné**.

### Étape 1 — Rassembler les données réelles
- **Ce qu'on a fait :** on part des vrais indices Bloomberg du portefeuille AP5 (actions suisses
  SPI/SLI/SPI Extra, actions monde MSCI, obligations suisses et mondiales, immobilier), en francs
  suisses, mois par mois, de 2008 à 2026.
- **Pourquoi :** pour que le portefeuille étudié soit **le vrai AP5**, pas une approximation
  inventée.
- **Résultat :** un tableau mensuel propre de tous les composants du portefeuille.

### Étape 2 — Reconstruire le portefeuille AP5
- **Ce qu'on a fait :** on assemble ces indices avec les poids exacts de la fiche VZ
  (*Kundendoku*, planche 5) : 25 % actions suisses, 25 % actions monde, 16,8 % obligations
  suisses, 25,2 % obligations mondiales, 5 % immobilier, 3 % liquidités.
- **Pourquoi :** c'est le portefeuille de référence auquel on comparera tous les remplacements.
- **Résultat :** une courbe de valeur de l'AP5 reconstitué, 2008–2026.

### Étape 3 — Vérifier que la reconstruction est fidèle
- **Ce qu'on a fait :** on compare notre AP5 reconstitué à la **vraie valeur du produit VZ**
  (données réelles 2019–2026).
- **Pourquoi :** pour prouver que notre reconstruction ressemble vraiment au produit réel, sinon
  toute la suite serait sur du sable.
- **Résultat :** très bonne correspondance — **corrélation 0,95**, écart de suivi ≈ 2,4 %/an. On
  a aussi vérifié que ce résultat **ne dépend pas** des réglages techniques (voir étape 6). On
  parle donc d'un **repère fidèle mais stylisé**, pas d'une copie exacte au centime près.

### Étape 4 — Choisir les remplaçants (et écarter les mauvais candidats)
- **Ce qu'on a fait :** on retient **six** actifs alternatifs qui ont tous un historique depuis
  2008 et qu'on peut réellement acheter : **or, matières premières, infrastructures, managed
  futures, obligations à haut rendement (HY), dette émergente (EM)**.
- **Pourquoi ce filtre :** on n'accepte qu'un actif *investissable, liquide, avec un prix
  observable et des frais calculables* — une exigence du directeur.
- **Écartés, avec raison :** **ILS** (pas d'historique public propre), **private equity/dette
  privée** (illiquide, valeurs « lissées », argent bloqué), **fonds hypothécaires suisses** (pas
  de série publique trouvée). On les cite pour montrer qu'ils ont été considérés puis écartés.

### Étape 5 — Enlever les frais (pour comparer honnêtement)
- **Ce qu'on a fait :** on applique à **tous** les portefeuilles les mêmes frais VZ : **1,37 %/an**
  (0,12 % produit + 1,25 % gestion), convenus avec le directeur.
- **Pourquoi :** comparer AP5 et remplacements **après frais**, comme un vrai client les vivrait,
  et à armes égales.
- **Résultat :** toutes les courbes sont « nettes de frais ».

### Étape 6 — Rééquilibrer le portefeuille comme le fait VZ
- **Ce qu'on a fait :** VZ ne rééquilibre pas à date fixe ; il surveille des **bandes** autour de
  la cible et ne rééquilibre que si un **groupe d'actifs** (catégorie) sort de sa bande. On
  reproduit ça avec une bande de **±8 %** au **niveau des catégories** (les six alternatives
  formant **une seule poche**).
- **Pourquoi le niveau « catégorie » :** la question est de remplacer la **poche** obligataire,
  pas d'inventer un système de micro-gestion actif par actif. C'est aussi ce que décrit la
  documentation VZ.
- **Vérification :** on a refait le calcul en surveillant **chaque** actif individuellement — ça
  déclenche beaucoup plus de transactions (≈ 61–96 contre ≈ 36–37) mais **donne quasiment les
  mêmes résultats**. La conclusion ne dépend donc pas de ce choix technique.

### Étape 7 — Remplacer les obligations par paliers de 10 %
- **Ce qu'on a fait :** on remplace la poche obligataire **par tranches** : 0 % (= AP5), 10 %,
  20 %, … jusqu'à 100 %, en répartissant à parts égales entre les six alternatives.
- **Pourquoi les paliers :** pour voir **une courbe** (l'effet augmente-t-il doucement ?) plutôt
  que trois points isolés — c'est plus informatif et plus honnête.
- **Résultat :** onze portefeuilles comparables, de « AP5 intact » à « obligations entièrement
  remplacées ».

### Étape 8 — Mesurer rendement ET risque
- **Ce qu'on a fait :** pour chaque palier, on calcule le rendement (CAGR), la volatilité, la pire
  baisse (drawdown), la perte extrême (CVaR) et le **Sharpe** (rendement rapporté au risque).
- **Pourquoi :** un rendement plus élevé ne vaut rien s'il coûte trop de risque ; il faut regarder
  **les deux ensemble**.
- **Résultat (le cœur de l'étude) :** plus on remplace, **plus le rendement monte** (de 3,55 % à
  4,28 %/an), **mais** la volatilité et les pertes augmentent aussi (pire baisse de −20 % à −28 %),
  et le **Sharpe ne s'améliore jamais** (≈ 0,48 stable jusqu'à ~50 %, puis il baisse).

### Étape 9 — Découper par régime de taux (BNS)
- **Ce qu'on a fait :** on coupe la période en **quatre régimes** de la BNS : R1 taux bas positifs
  (2008–14), R2 taux négatifs (2015–22), R3 hausses (2022–24), R4 assouplissement (2024–26).
- **Pourquoi :** répond à la **Question 3** et évite un seuil « taux bas » arbitraire ; on lit
  directement comment chaque régime se comporte.
- **Résultat :** le remplacement **coûte** quand les obligations sont fortes (R1) et **rapporte**
  quand elles souffrent (R2, R4). On note aussi que les obligations **mondiales** ont beaucoup
  souffert des hausses de 2022–24 (−2,9 %/an) alors que les **suisses** sont restées positives.

### Étape 10 — Tester la solidité (robustesse)
- **Ce qu'on a fait :** on vérifie que la conclusion **tient** quand on change les hypothèses :
  taille de bande (±5/8/10/15/20 %), coûts de transaction (0–50 pb), couverture de change des
  HY/EM, période (avec/sans 2008–09). On ajoute un **bootstrap** — une technique qui rejoue
  l'histoire des milliers de fois en mélangeant les mois — pour savoir si les écarts sont
  **réels** ou dus au hasard.
- **Pourquoi :** un bon résultat doit survivre à des choix raisonnables différents ; sinon il est
  fragile.
- **Résultat :** le remplacement **intégral aggrave la perte extrême dans tous les cas testés**
  (probabilité ≈ 99–100 %). Aucun niveau de remplacement n'améliore le Sharpe de façon fiable.

### Étape 11 — Regarder les crises (2020 vs 2022)
- **Ce qu'on a fait :** on compare deux crises opposées : le krach déflationniste de 2020 (COVID)
  et le choc de taux de 2022.
- **Pourquoi :** montrer que le remplacement ne supprime pas le risque — il en **change la
  nature**.
- **Résultat :** en 2020, remplacer a **nui** (les obligations protégeaient) ; en 2022, remplacer
  a **aidé** (obligations et actions baissaient ensemble). *Le remplacement change contre quelle
  crise on est protégé.*

## 5. Le résultat principal, en clair

> **Remplacer les obligations augmente le rendement, mais augmente aussi la volatilité et les
> pertes extrêmes, sans améliorer la performance ajustée au risque.**
>
> Ce n'est donc **pas** la découverte d'un « meilleur actif » que les obligations : c'est un
> **choix de budget de risque**. On ne remplace pas « les obligations », mais **une partie de ce
> qu'elles font** (le portage, un peu de diversification) — **pas** la protection en cas de crise
> ni la duration. C'est pour cela que le risque de perte extrême empire.

## 6. La recommandation

- **Éviter le remplacement intégral** : il aggrave nettement les pertes extrêmes sans gain de
  Sharpe fiable, et supprime la protection de type 2020.
- **Un remplacement partiel** est un **compromis** défendable (plus de rendement à Sharpe quasi
  constant), **pas** un optimum : les données ne désignent aucun pourcentage « idéal ».
- **Conserver la structure obligataire** (suisses + mondiales, longues + courtes).
- Le **choix des instruments** compte (un panier trié fait un peu mieux), mais c'est un constat
  *après coup*, à valider hors échantillon — ce n'est pas la recommandation.

## 7. Ce qui reste à faire (le travail de rédaction)

L'analyse empirique (les chiffres, les graphiques, les tests) est **terminée et verrouillée**. Ce
qui reste relève de la **rédaction du mémoire**, à écrire par l'étudiante :

- la **revue de littérature** ;
- le **cadre théorique** et les **références** ;
- l'introduction, la discussion et la conclusion rédigées ;
- la mise en forme finale.

## 8. Où trouver chaque chose dans le dépôt

| Vous voulez… | Fichier |
|---|---|
| Les chiffres officiels (source unique) | `analysis/results_manifest.json` |
| Le détail méthodologique complet | `docs/methodology.md` (avec le tableau « toutes les hypothèses en un coup d'œil ») |
| Le rapport complet (EN) | `reports/thesis_report.md` |
| Le résumé exécutif (FR) | `reports/resume_executif.md` |
| Les graphiques | `reports/figures/` (EN) et `reports/figures_fr/` (FR, 300 dpi) |
