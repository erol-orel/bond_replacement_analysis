# Guide pas à pas — tout expliquer, très simplement

**Mémoire HEC Lausanne · « Alternatives aux obligations » · mandat VZ AP5 · CHF, mensuel, net de
frais · février 2008 – juin 2026**

> À quoi sert ce document. Il explique **absolument tout** ce qui a été fait, **une étape à la
> fois**, dans un langage très simple — comme si on l'expliquait à quelqu'un qui n'a jamais fait
> de finance. Chaque mot compliqué est expliqué. Chaque décision est justifiée. L'objectif est que
> tu puisses tout comprendre et tout réexpliquer à quelqu'un d'autre.

---

## PARTIE 0 — Le vocabulaire de base (à lire en premier)

Avant de parler de l'étude, voici les mots essentiels, avec des images simples.

- **Un portefeuille**, c'est un panier de placements. On met dedans différents « ingrédients »
  (actions, obligations, or…) dans certaines proportions.
- **Une action**, c'est une part d'entreprise. Ça rapporte beaucoup sur le long terme mais ça
  monte et descend fort (risqué).
- **Une obligation**, c'est un **prêt**. Tu prêtes de l'argent à un État ou une entreprise, et en
  échange on te verse un petit intérêt régulier, puis on te rend ton argent à la fin. C'est
  **moins risqué** que les actions, mais ça rapporte peu.
- **VZ AP5**, c'est le portefeuille étudié : un produit réel de la société suisse VZ, « profil 5 »
  (assez dynamique). Il contient à peu près **50 % d'actions, 42 % d'obligations, 5 %
  d'immobilier, 3 % de liquidités**.
- **Les « 42 % obligations »**, c'est le gros bloc de prêts du portefeuille. C'est **lui** que la
  thèse veut peut-être remplacer.
- **Le rendement**, c'est ce que ça rapporte, en général exprimé en **% par an**.
- **Le risque**, c'est à quel point ça bouge et à quel point on peut perdre. On le mesure de
  plusieurs façons (voir Partie 3).
- **« Net de frais »**, ça veut dire *après avoir enlevé les frais* (la banque prend une
  commission ; on la retire pour être réaliste).

**Le problème de départ, en une phrase.** Les obligations rapportent très peu depuis des années
(taux d'intérêt bas), et quand les taux **remontent** (comme en 2022), elles **perdent** de la
valeur. Donc on se demande : *peut-on remplacer une partie de ces obligations par autre chose de
mieux ?* C'est toute la thèse.

## PARTIE 1 — L'objectif et les trois questions

**L'objectif, en une phrase.** Savoir si l'on peut remplacer les **42 % d'obligations** du
portefeuille AP5 par d'autres placements, **et à quel prix en risque**, sur la période 2008–2026.

On répond à **trois questions simples** :

1. **Rendement** — remplacer les obligations, est-ce que ça **rapporte plus** ?
2. **Risque** — est-ce que ça **augmente le risque**, surtout les grosses pertes ?
3. **Régime** — est-ce que la réponse **change selon l'époque** (taux qui montent ou qui
   descendent) ?

C'est tout. Trois questions. On ne cherche pas *le* pourcentage magique ; on cherche à comprendre
le **compromis** entre rendement et risque.

## PARTIE 2 — Les « ingrédients » de remplacement testés

On teste **six** placements alternatifs qui existent vraiment, qu'on peut acheter, et qui ont un
historique depuis 2008 :

| Alternative | En une phrase |
|---|---|
| **Or** | Métal précieux, valeur refuge en cas de crise. Ne verse aucun intérêt. |
| **Haut rendement (HY)** | Obligations d'entreprises plus risquées, qui paient plus d'intérêt. |
| **Dette émergente (EM)** | Obligations de pays en développement, plus d'intérêt, plus de risque. |
| **Infrastructures** | Actions d'entreprises d'autoroutes, d'énergie, etc. Verse des revenus. |
| **Managed futures** | Fonds « suiveurs de tendance » automatiques. Censés aider en crise. |
| **Matières premières** | Pétrole, métaux, blé… Censé protéger contre l'inflation. |

On a aussi **considéré puis écarté** d'autres candidats, avec des raisons claires : les
**convertibles** (trop proches des actions), les **CLO** (pas de données propres), les **ILS /
obligations catastrophe** et le **private credit** (pas assez liquides, pas de bon historique).
On le dit dans la thèse pour montrer qu'on ne les a pas oubliés — on les a exclus **exprès**.

## PARTIE 3 — Comment on mesure (les chiffres à connaître)

Pour chaque portefeuille, on regarde toujours les mêmes choses. Voici ce que chaque mot veut dire,
très simplement :

- **Rendement (CAGR)** — le gain **moyen par an**. Exemple : 4 % veut dire qu'en moyenne le
  portefeuille a grandi de 4 % chaque année.
- **Volatilité** — à quel point ça **bouge**. Élevée = ça monte et descend fort (stressant).
- **Pire perte (drawdown)** — la **plus grosse chute** depuis un sommet. Exemple : −28 % veut dire
  qu'au pire moment, on avait perdu 28 % depuis le point haut.
- **Perte extrême (CVaR)** — dans les **pires mois** (les 5 % les plus mauvais), combien on perd en
  moyenne. C'est le « risque de catastrophe ».
- **Sharpe** — le chiffre le plus important : le **rendement rapporté au risque**. Il répond à :
  *« pour le risque que je prends, est-ce que je suis bien payé ? »* **Plus il est haut, mieux
  c'est.** Deux portefeuilles peuvent rapporter pareil, mais celui avec le Sharpe le plus élevé le
  fait avec **moins de risque** — c'est le meilleur.

> Astuce pour Erta : si tu ne devais retenir qu'un seul chiffre, ce serait le **Sharpe**. Gagner
> plus en prenant beaucoup plus de risque, ce n'est pas « mieux » — le Sharpe corrige justement
> pour ça.

## PARTIE 4 — Les étapes de l'analyse, une par une

Chaque étape dit : **ce qu'on a fait**, **pourquoi**, **ce que ça a donné**.

### Étape 1 — Rassembler les vraies données
- **Fait :** on récupère les vrais indices Bloomberg de chaque ingrédient du portefeuille AP5, en
  francs suisses, mois par mois, de 2008 à 2026.
- **Pourquoi :** pour travailler sur le **vrai** portefeuille, pas une version inventée.
- **Résultat :** un grand tableau mensuel, propre, de tous les ingrédients.

### Étape 2 — Reconstruire le portefeuille AP5
- **Fait :** on assemble ces ingrédients avec les poids exacts de la fiche officielle VZ (25 %
  actions suisses, 25 % actions monde, 16,8 % + 25,2 % obligations, 5 % immobilier, 3 % cash).
- **Pourquoi :** c'est le portefeuille de **référence** ; tout sera comparé à lui.
- **Résultat :** la courbe de valeur de l'AP5 « reconstitué », 2008–2026.

### Étape 3 — Vérifier que notre reconstruction est fidèle
- **Fait :** on compare notre AP5 reconstitué au **vrai produit VZ** (dont on a les vraies valeurs
  2019–2026).
- **Pourquoi :** si notre copie ne ressemblait pas à l'original, toute la suite serait fausse. Il
  faut le **prouver**.
- **Résultat :** très bonne ressemblance (**corrélation 0,95** — proche de 1 = quasi identique). On
  a même vérifié que ce résultat tient quel que soit le réglage technique. On parle donc d'un
  **repère fidèle mais stylisé**, pas d'une copie au centime près (honnête).

### Étape 4 — Choisir les remplaçants (et écarter les mauvais)
- **Fait :** on retient les **six** alternatives de la Partie 2, et on écarte les autres avec des
  raisons.
- **Pourquoi :** on n'accepte qu'un placement *qu'on peut vraiment acheter, revendre vite, et dont
  on peut calculer le rendement après frais*.
- **Résultat :** une liste honnête et défendable de candidats.

### Étape 5 — Enlever les frais (pour comparer juste)
- **Fait :** on retire à **tous** les portefeuilles les mêmes frais VZ : **1,37 % par an**.
- **Pourquoi :** comparer ce qu'un vrai client toucherait *après frais*, et à armes égales.
- **Résultat :** toutes les courbes sont « nettes de frais ».

### Étape 6 — Rééquilibrer comme le fait VZ
- **Fait :** VZ ne rééquilibre pas à date fixe ; il **surveille des marges** autour de la cible et
  ne rééquilibre que si un **groupe** d'actifs sort de sa marge (±8 %). On reproduit ça.
- **Pourquoi :** on veut imiter le **vrai** fonctionnement du produit, pas un rééquilibrage
  artificiel.
- **Résultat + vérification :** on a aussi testé en surveillant **chaque** actif un par un — ça
  déclenche beaucoup plus d'opérations mais **change à peine les résultats**. Donc notre choix ne
  fausse rien.

### Étape 7 — Remplacer les obligations par doses de 10 %
- **Fait :** on remplace les obligations **par tranches** : 0 % (= AP5), 10 %, 20 %… jusqu'à 100 %.
- **Pourquoi :** pour voir une **courbe** (l'effet augmente-t-il doucement ?), pas seulement
  quelques points isolés.
- **Résultat :** onze portefeuilles comparables.

### Étape 8 — Mesurer rendement ET risque
- **Fait :** pour chaque dose, on calcule rendement, volatilité, pire perte, perte extrême, Sharpe.
- **Pourquoi :** un rendement plus élevé ne vaut rien s'il coûte trop de risque. On regarde **les
  deux ensemble**.
- **Résultat (le cœur) :** plus on remplace, **plus le rendement monte** (3,55 % → 4,28 %), **mais
  le risque aussi** (pire perte −20 % → −28 %), et le **Sharpe ne s'améliore jamais**.

### Étape 9 — Regarder chaque époque (régime de taux)
- **Fait :** on découpe 2008–2026 en **quatre périodes** selon la politique de la BNS.
- **Pourquoi :** répond à la Question 3 ; évite un seuil « taux bas » arbitraire.
- **Résultat :** remplacer **coûte** quand les obligations sont fortes, et **rapporte** quand elles
  souffrent. C'est un **pari sur l'époque**.

### Étape 10 — Vérifier la solidité (robustesse)
- **Fait :** on refait tout en changeant les hypothèses (marges, frais, couverture, période), et on
  utilise un **bootstrap** — une technique qui **rejoue l'histoire des milliers de fois** en
  mélangeant les mois, pour voir si un résultat est **vrai** ou dû à la chance.
- **Pourquoi :** un bon résultat doit **survivre** à des choix différents.
- **Résultat :** le remplacement total **aggrave la perte extrême dans presque 100 % des cas**, et
  **aucune** dose n'améliore le Sharpe de façon fiable.

### Étape 11 — Regarder les crises (2020 contre 2022)
- **Fait :** on compare deux crises opposées.
- **Pourquoi :** montrer que le remplacement ne supprime pas le risque, il en **change la nature**.
- **Résultat :** en **2020** (COVID), remplacer a **nui** (les obligations protégeaient) ; en
  **2022** (choc de taux), remplacer a **aidé** (obligations et actions baissaient ensemble).

## PARTIE 5 — Les trois façons de remplacer (le cœur des résultats)

C'est la partie la plus importante à réexpliquer. Trois approches, de la plus simple à la plus
avancée.

### Approche A — une seule alternative à la fois
On remplace **toutes** les obligations par **un seul** ingrédient, et on compare (**figure T1**).
Résultat clair : **seul l'or**, tout seul, fait mieux que l'AP5 (Sharpe 0,60 contre 0,48). Le haut
rendement et la dette émergente font pareil que l'AP5 mais avec de plus grosses chutes. Les
matières premières et les managed futures ont carrément **perdu de l'argent**.

> À retenir : parmi six alternatives, **une seule** (l'or) est meilleure toute seule. Ce n'est pas
> évident au départ — d'où l'intérêt de tester une par une.

### Approche B — un mélange (et pourquoi ce mélange)
Mettre 42 % dans un seul actif, c'est dangereux (tous les œufs dans le même panier). Donc on
mélange. Mais **quel** mélange ?
- **Mélange équipondéré** (parts égales des six) : Sharpe **0,46** — *moins bien que l'AP5* !
  Pourquoi ? Parce qu'il inclut les deux perdants (matières premières, managed futures).
- **Mélange trié** (on garde les bons, on jette les perdants : haut rendement 35 %, dette émergente
  30 %, or 20 %, infrastructures 15 %) : Sharpe **0,52** — mieux que l'AP5.

> La leçon : un mélange « bête » (tout à parts égales) est **moins bon** que de garder les
> obligations. Il faut **choisir** les ingrédients — et ce choix est justifié par l'Approche A.
> Attention honnête : ce mélange trié est choisi *après avoir vu les résultats*, donc c'est une
> **illustration**, pas une promesse.

### Approche C — laisser un ordinateur optimiser
On laisse un **optimiseur** (un programme) choisir les meilleurs poids possibles, en regardant tout
l'historique. Résultat frappant : même **libre de tout enlever**, il **garde la plupart des
obligations** et ajoute seulement **un peu d'or**. Il ne remplace **jamais** tout.

> Trois méthodes différentes (une par une, mélange, optimiseur) disent **la même chose** : garder
> les obligations, ajouter au plus un peu d'or.

## PARTIE 6 — La conclusion, en langage simple

> **Remplacer les obligations fait gagner un peu plus, mais fait aussi risquer beaucoup plus — sans
> être mieux payé pour ce risque.**

Autrement dit : on ne trouve **pas** un placement « meilleur que les obligations ». On **change le
niveau de risque** du portefeuille. C'est un choix, pas une amélioration gratuite.

Ce qu'on peut réellement dire :
- **Ne pas tout remplacer** : ça aggrave les grosses pertes sans meilleur Sharpe.
- **Le seul ajout utile** historiquement, c'est **un peu d'or, à côté des obligations** (pas à leur
  place) — et encore, c'est un pari concentré sur une période où l'or a bien marché.
- **Garder les obligations** (suisses + mondiales, longues + courtes) : elles se comportent
  différemment selon les époques et se complètent.

## PARTIE 7 — Les questions qu'Erta pourrait poser (et les réponses)

- *« Pourquoi 2008 et pas avant ? »* — Parce que l'un des ingrédients (la dette émergente) commence
  en février 2008. Pour comparer tous les portefeuilles sur **exactement la même période**, on part
  de là.
- *« Pourquoi des proxys (ETF) et pas les vrais fonds VZ ? »* — Parce qu'il faut un historique long,
  public et net de frais. Les ETF/indices le fournissent ; on le dit clairement.
- *« L'or à 0,60, pourquoi ne pas tout mettre en or ? »* — Parce que c'est **un seul actif**, très
  volatil, sans aucun revenu, et le beau résultat vient d'une période **favorable** à l'or. Mettre
  42 % du portefeuille sur un seul pari, c'est imprudent.
- *« Le résultat est-il sûr ? »* — Le côté « le remplacement total aggrave les grosses pertes » est
  **très solide** (survit à tous les tests). Le petit avantage d'un remplacement partiel, lui,
  **dépend des hypothèses** — on est honnête là-dessus.
- *« Est-ce que la thèse est finie ? »* — L'**analyse** (chiffres, graphiques, tests) est finie. Il
  reste à **écrire** le mémoire : revue de littérature, cadre théorique, références, introduction,
  discussion, conclusion. Ça, c'est le travail de rédaction de l'étudiante.

## PARTIE 8 — Où se trouve chaque chose

| Tu veux… | Fichier |
|---|---|
| La version principale de la thèse (FR) | `reports/these_principale_FR.md` |
| Ce guide simple | `reports/guide_pas_a_pas.md` |
| Les chiffres officiels (source unique) | `analysis/results_manifest.json` |
| Le détail méthodologique complet | `docs/methodology.md` |
| **Où se trouve chaque calcul dans le code (lignes exactes)** | `reports/tracabilite_code_FR.md` |
| Les graphiques | `reports/figures_fr/` (dont T1–T4, les nouveaux) |
