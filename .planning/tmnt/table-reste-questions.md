# Questions ouvertes : T15, T16, T17 (mode « Sur la table », 19/10/2026)

## Q1. Refuser de défendre contre un sbire Rapide fige la partie (constaté, existait avant)

Vu : Assassin Badoon (16117) mis en jeu pendant le tour, Spider-Man héros. On clique « Ne pas défendre ». Le moteur pose
alors une seconde question (`WhenUnitBeingAttack`, `show_cancel` vrai) dont la seule option (Sens d'Araignée, `Play`) est
listée dans `refus_json` avec la raison « update legal targets », et `options_json` est VIDE. `lireDemande` (ask.ts) rend
`undefined` quand il n'y a aucune option : le plateau croit que le moteur n'attend rien, et la partie reste figée
(« En attente de Spider-Man »). Reproduit dans l'ancien affichage aussi. Défendre avec Spider-Man ne fige pas.

Options :
1. `lireDemande` garde une demande sans option quand `show_cancel` est vrai (le panneau montre alors « Passer »).
   Touche une logique partagée par tous les modes.
2. Côté moteur : ne pas proposer Sens d'Araignée contre un sbire (la carte dit « quand le MÉCHANT initie une attaque »).
3. Ne rien faire pour l'instant.

Recommandation : 2 (c'est une règle du jeu mal posée), puis 1 en filet. Je n'y ai pas touché (hors périmètre).

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
