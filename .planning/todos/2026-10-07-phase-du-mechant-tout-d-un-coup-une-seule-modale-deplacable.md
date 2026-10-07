# Phase du méchant « tout d'un coup » : revoir les modales, une seule fenêtre claire et déplaçable (07/10/2026)

**Statut : BACKLOG, demande de l'utilisateur (questions posées une à une). Rien n'est commencé.**

## Le problème constaté (capture du 07/10/2026, Cyclops attaqué par Klaw)
En mode « tout d'un coup », les choix de défense sont des BULLES ÉPARPILLÉES sur la table, chacune posée près d'une carte :
« Defend with Cyclops (DEF 2) », « Ask Cyclops → Iceman », « Defend with Dust », et en bas « Don't defend (ATK 2 - 1 Frostbite -
1 Frostbite + 2 boost cards) ». Le message « Cyclops is being attacked by Klaw / You can react » flotte en haut, loin de l'attaquant.
Constats sur la capture : « Ask Cyclops → Iceman » se pose SUR l'allié Dust, « Defend with Cyclops » tombe près du héros, on ne
voit pas d'un coup d'œil l'ensemble des choix, et les cartes dessous sont cachées.

## Ce que dit l'utilisateur
« C'est surtout la dispersion qui est problématique : il faudrait faire une modale plus claire et bougeable. »
Parmi les causes proposées, il a retenu : **les bulles sont dispersées et cachent les cartes** (pas un problème de vocabulaire ni
de quantité d'écrans).

## Décisions (questions une à une)
1. **Forme : UNE fenêtre avec tous les choix en liste.** Un seul panneau DÉPLAÇABLE : en haut le rappel de l'attaque (« Klaw attaque
   Cyclops, ATK 2 »), puis une liste de boutons (« Défendre avec Cyclops (DEF 2) », « Défendre avec Dust », « Demander à Iceman »,
   « Ne pas défendre »). Les cartes concernées s'allument sur la table quand on survole un bouton.
2. **Portée : TOUS les choix de la phase du méchant**, pas seulement la défense : défendre, réagir à une carte (« You can react »),
   choisir une cible, une interruption. Un seul style, un seul endroit, déplaçable.

## Où regarder
- `ui-app/src/board/DemandeCentrale.tsx`, `board.tsx` (les bulles posées près des cartes), `board/ligne-attaque.ts`,
  `board/sous-cadre.ts`, `board/deroule-textes.ts` (textes), et la famille de la phase du méchant (`CartouchePhase.tsx`, `DeroulePhase.tsx`).
- Lien avec la fiche voisine du 07/10 : « la modale de choix, le bouton de validation collé au-dessus, et les deux bougent ensemble »
  (`2026-10-07-modale-de-choix-bouton-colle-et-deplacement-solidaire.md`) : même mécanisme de déplacement solidaire à partager.
- Le glisser-déposer des fenêtres existe déjà ailleurs dans le plateau : le réutiliser.

## Questions encore ouvertes
- Que devient le texte long du bouton « Ne pas défendre (ATK 2 - 1 Frostbite - 1 Frostbite + 2 boost cartes) » : détail replié, ou
  ligne dédiée « Dégâts prévus » dans le rappel ?
- Position de départ de la fenêtre (centrée, ou près de l'attaquant), et mémorisée d'un choix à l'autre ?
- Plusieurs héros : une fenêtre par héros attaqué, ou une seule qui change de titre ?
- Les modes « étape par étape » et « résumé » de la phase du méchant gardent-ils leurs fenêtres actuelles ?
