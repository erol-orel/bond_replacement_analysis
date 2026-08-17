# Guide global — vue d'ensemble du projet

**Mémoire VZ AP5 · « Alternatives aux obligations » · CHF, mensuel, net de frais ·
février 2008 – juin 2026**

> Ce guide donne une **vue d'ensemble** du travail : l'objectif, la méthode, les résultats
> principaux, et la carte des documents du projet. Il se lit seul, sans connaissance financière
> préalable — chaque terme technique est défini une fois. La **source unique** des chiffres est
> `analysis/results_manifest.json`.

---

## 1. Objectif et questions

**Objectif (une phrase).** Déterminer si les **42 % d'obligations** du portefeuille VZ **AP5**
peuvent être remplacés par d'autres placements, et **à quel prix en risque**, sur la période
2008–2026.

Le problème : les obligations rapportent peu depuis des années, et quand les taux **montent**
(comme en 2022), elles perdent de la valeur. On se demande donc s'il vaut mieux en remplacer une
partie par autre chose.

L'étude répond à **trois questions** :

1. **Rendement** — remplacer les obligations change-t-il le rendement à long terme ?
2. **Risque** — cela change-t-il le risque, surtout les grosses pertes (baisses profondes et
   pertes extrêmes) ?
3. **Régime** — la réponse dépend-elle de l'environnement de taux (politique de la BNS) ?

La question « partiel ou intégral ? » est traitée comme une **recommandation**, non comme une
quatrième hypothèse.

## 2. Quelques définitions utiles

| Terme | Définition courte |
|---|---|
| **Portefeuille** | Un panier de placements dans certaines proportions. |
| **Action** | Une part d'entreprise ; rapporte beaucoup mais varie fort. |
| **Obligation** | Un prêt à un État/entreprise ; verse un intérêt régulier, moins risqué. |
| **AP5 / VVIA** | Le produit VZ étudié (« profil 5 ») : ≈50 % actions, 42 % obligations, 5 % immobilier, 3 % liquidités. |
| **Rendement (CAGR)** | Le gain moyen par an. |
| **Volatilité** | À quel point la valeur bouge (haut = instable). |
| **Pire perte (drawdown)** | La plus grosse baisse depuis un sommet. |
| **Perte extrême (CVaR)** | La perte moyenne dans les 5 % de mois les pires. |
| **Sharpe** | Le rendement **rapporté au risque** ; plus il est haut, mieux c'est. |
| **Net de frais** | Après déduction des frais (1,37 %/an appliqués à tous). |

## 3. Comment lire les chiffres

Pour chaque portefeuille, on regarde toujours les mêmes mesures : rendement, volatilité, pire
perte, perte extrême, et surtout le **Sharpe**. Le Sharpe est le chiffre décisif : deux
portefeuilles peuvent rapporter autant, mais celui au **Sharpe le plus élevé** y parvient avec
**moins de risque**. Gagner plus en prenant beaucoup plus de risque n'est donc pas « mieux » — le
Sharpe corrige exactement pour cela.

## 4. Le travail réalisé, étape par étape

| Étape | Ce qui a été fait | Pourquoi |
|---|---|---|
| 1. Données | Récupérer les vrais indices Bloomberg du portefeuille, en CHF, mensuels, 2008–2026 | Travailler sur le vrai portefeuille |
| 2. Reconstruction | Assembler l'AP5 avec les poids exacts de la fiche VZ | Créer la référence |
| 3. Validation | Comparer au vrai produit VZ (corrélation 0,95, tracking error 2,4 %) | Prouver que la copie est fidèle |
| 4. Candidats | Retenir 6 alternatives investissables ; écarter les autres avec raisons | Liste défendable |
| 5. Frais | Appliquer 1,37 %/an à tous les portefeuilles | Comparaison honnête, après frais |
| 6. Rééquilibrage | Imiter le rééquilibrage par bandes de VZ (±8 %, par catégorie) | Reproduire le vrai fonctionnement |
| 7. Paliers | Remplacer les obligations par doses de 10 % (0 → 100 %) | Voir une courbe, pas des points isolés |
| 8. Mesures | Rendement + risque pour chaque palier | Juger le compromis |
| 9. Régimes | Découper en 4 régimes de taux BNS | Répondre à la question 3 |
| 10. Robustesse | Refaire en changeant les hypothèses + bootstrap (3 000 rejeux) | Vérifier la solidité |
| 11. Crises | Comparer 2020 (COVID) et 2022 (choc de taux) | Montrer la nature du risque |

## 5. Les trois façons de remplacer (le cœur des résultats)

**Approche A — une seule alternative à la fois.** On remplace toutes les obligations par un seul
placement. Résultat : **seul l'or**, isolé, fait mieux que l'AP5 (Sharpe 0,60 contre 0,48). Le
haut rendement et la dette émergente font pareil que l'AP5 mais avec de plus grosses chutes. Les
matières premières et les managed futures ont **perdu de l'argent**.

**Approche B — un mélange.** Mettre 42 % sur un seul actif est dangereux. On mélange donc. Mais un
mélange **équipondéré** (parts égales) donne un Sharpe de **0,46** — *moins bien que l'AP5*, car il
inclut les deux perdants. Un mélange **trié** (haut rendement 35 %, dette émergente 30 %, or 20 %,
infrastructures 15 %), qui écarte les perdants, remonte à **0,52**.

**Approche C — allocation optimisée.** Un optimiseur libre de tout choisir **garde la plupart des
obligations** et n'ajoute qu'un peu d'or. Il ne remplace jamais tout.

> Trois méthodes différentes disent la même chose : garder les obligations, ajouter au plus un
> peu d'or.

## 6. La conclusion

> **Remplacer les obligations augmente le rendement, mais augmente aussi la volatilité et les
> pertes extrêmes, sans amélioration fiable du rendement ajusté au risque.**

Ce n'est donc pas la découverte d'un actif « meilleur » que les obligations : c'est un **choix de
budget de risque**. Concrètement :

- **Ne pas remplacer les obligations en totalité** : cela aggrave les grosses pertes sans meilleur
  Sharpe, et retire la protection de type 2020.
- **Le seul ajout utile** historiquement est **un peu d'or, à côté des obligations** — et encore,
  c'est un pari concentré sur une période favorable à l'or, à stresser avant tout usage.
- **Conserver la structure obligataire** (suisses + mondiales, longues + courtes) : elles ne sont
  pas redondantes.

## 7. Les documents du projet (carte de lecture)

| Document | Contenu |
|---|---|
| **Thèse (version principale)** `reports/these_principale_FR.md` | L'analyse complète : structure, candidats un par un, tableaux, figures, recommandation. |
| **Résultats complets** `reports/resultats_complets_FR.md` | **Tous** les tableaux chiffrés (tracking error, par actif, par palier, régimes, optimisations, robustesse, crises), chacun relié à sa source. |
| **Ce guide global** `reports/guide_global_FR.md` | La vue d'ensemble et la carte de lecture. |
| **Traçabilité du code** `reports/tracabilite_code_FR.md` | Où se trouve chaque calcul dans le code Python (fichier : lignes). |
| **Résumé exécutif** `reports/resume_executif_FR.md` | La version courte des messages clés. |
| Méthodologie détaillée | `docs/methodology.md` |
| Figures | `reports/figures_fr/` (dont T1–T4) |
| Chiffres officiels (source unique) | `analysis/results_manifest.json` |

## 8. Pour aller plus loin (travail de rédaction restant)

L'analyse empirique (données, calculs, graphiques, tests statistiques) est **terminée et
reproductible**. Restent à rédiger, pour transformer ce socle en mémoire complet :

- la **revue de littérature** (décomposition du rôle des obligations, duration, alternatives) ;
- le **cadre théorique** et les **références** ;
- l'**introduction**, la **discussion** et la **conclusion** rédigées ;
- la **mise en forme** finale.

Les chiffres et figures nécessaires à ces chapitres existent déjà dans les documents ci-dessus.

## 9. Questions fréquentes

- **Pourquoi commencer en 2008 ?** L'une des alternatives (la dette émergente) débute en février
  2008 ; pour comparer tous les portefeuilles sur exactement la même période, on part de là.
- **Pourquoi des proxys (ETF/indices) et pas les fonds VZ eux-mêmes ?** Il faut un historique long,
  public et net de frais ; les ETF/indices le fournissent, ce qui est indiqué explicitement.
- **L'or à 0,60, pourquoi ne pas tout mettre en or ?** C'est un seul actif, très volatil, sans
  aucun revenu, et le résultat vient d'une période favorable à l'or. Concentrer 42 % du
  portefeuille sur un seul pari serait imprudent.
- **Le résultat est-il robuste ?** Oui pour le point central (« le remplacement intégral aggrave
  les pertes extrêmes ») : il survit à toutes les variations testées. Le petit avantage d'un
  remplacement partiel, lui, dépend des hypothèses — ce qui est indiqué honnêtement.
