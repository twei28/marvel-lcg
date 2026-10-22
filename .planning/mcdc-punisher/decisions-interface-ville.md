# Interface « La Ville » (PU-8) : decisions de l'utilisateur

Le 22/10/2026, l'utilisateur remplace le plan « A + B » (mini-carte permanente + fenetre « La Ville ») par un **onglet lateral « Ville »**, a cote des onglets Journal et Aide existants. Exemple HTML : artefact « La Ville ne dort jamais » (maquette de principe, hors onglet).

| # | Question | Decision |
|---|---|---|
| 1 | Ouverture du panneau | **Panneau lateral PAR-DESSUS la table** (comme un tiroir) ; la table garde sa taille |
| 2 | Onglet ferme | **Mini-carte 3×3 en miniature** dans l'onglet (9 cases, pions, toujours visible sur le cote) |
| 3 | Territoire d'un autre joueur | **La carte montre les 3 rangees, la mienne en surbrillance** ; un clic sur le pion d'un coequipier affiche sa rangee et ses sbires en lecture seule, sans changer ma table |
| 4 | Declenchement du deplacement | **Les deux** : clic sur une case verte puis choix du cout (epuiser un personnage / 1 ressource), ET l'Action habituelle de la carte The City reste disponible |
| 5 | Detail d'un lieu | **Survol = carte agrandie** (comme les autres cartes du plateau) ; le clic reste reserve au deplacement |
| 6 | Infos sur chaque case | **Les quatre** : pions des joueurs, pastille de sbire attache, compteurs de piste poses sur le lieu, indicateur « capacite deja utilisee ce round » (limite commune a tous) |
| 7 | Position de la carte agrandie (volet ouvert) | **A GAUCHE du volet, collee a lui**, pour ne pas masquer la zone de jeu (pas a l'endroit habituel). Hauteur **fixe, centree verticalement** (ne bouge pas d'un lieu a l'autre) |
| 8 | Assemblee (multi-tables) : comment les groupes se retrouvent | **Un code d'assemblee partage** : la 1re table qui lance Kingsfall epique cree l'assemblee, recoit un code court ; les autres tables l'entrent en creant leur partie ; la 1re table = organisatrice (Longue vie et Le Roi vivent chez elle) |
