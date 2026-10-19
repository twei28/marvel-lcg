# Questions ouvertes : T15, T16, T17 (mode « Sur la table », 19/10/2026)

## Q1. Refuser de défendre contre un sbire Rapide fige la partie : RÉSOLU (19/10/2026)

Cause réelle (pas Sens d'Araignée, dont le « refus » n'est que la liste des cartes injouables de la main) : la question
« Qui défend ? » est posée PAR un geste manuel (`Puzzle.PutIntoPlay`), donc depuis l'intérieur du `DoGetInput` de la
question précédente. Le joueur figurait deux fois dans `asking_players` ; sa réponse n'en retirait qu'une, et `{}`
(« Ne pas défendre ») est la valeur lue comme « pas d'entrée » : le moteur dormait pour toujours. Corrigé dans
`DeviceManager.DoGetInput` (le joueur sort de `asking_players` avant de drainer le geste). Aucune règle changée.
Test : `tools/test_mode_manuel.py question_posee_par_un_geste` (rouge avant, vert après).

## Q2. Une seule étape par statut dans le toast quand deux statuts tombent dans le même rendu

Le toast sait dire « Hulk reçoit les statuts Sonné et Désorienté » quand les deux arrivent dans le même rendu du moteur.
Quand les deux cartes sont posées par deux commandes séparées, on voit deux toasts à la suite (le second remplace le premier).
Options : 1. laisser ; 2. empiler les toasts d'une même carte ; 3. allonger la durée quand plusieurs se suivent.
Recommandation : 1.

## Q3. La flèche attaquant → défenseur pour un sbire Rapide

Pendant la phase du méchant, une flèche rouge relie l'attaquant à sa cible. Hors phase, le bandeau porte la phrase, le nombre
et le calcul, mais pas la flèche ni la lecture des cartes de boost (le calcul dit « + Boost n »).
Options : 1. laisser ainsi ; 2. tracer la flèche seulement ; 3. rejouer aussi la lecture des boosts hors phase.
Recommandation : 2 (petit), 3 plus tard si tu veux les mêmes cartes lues au centre.

## Q4. L'allié vaincu est déjà dans la pile de défausse pendant l'étape du coup

Pendant l'étape « Klaw attaque Hulk », la table montre déjà Hulk dans la défausse (le monde est à jour). L'étape « Hulk est vaincu »
le lit puis l'y renvoie. Pour que Hulk reste en jeu jusqu'à son étape, il faudrait caler la table de l'étape du coup sur le
monde d'avant la défausse.
Options : 1. laisser ; 2. caler la table (risque sur les instantanés de la phase).
Recommandation : 1 pour l'instant.
