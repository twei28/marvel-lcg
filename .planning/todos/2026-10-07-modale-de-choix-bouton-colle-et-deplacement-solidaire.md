# Modale de choix : le bouton qui valide se colle au-dessus, et les deux bougent ensemble (07/10/2026)

**Statut : BACKLOG, demande de l'utilisateur. Rien n'est commencé.**

## La demande (ses mots)
« Quand on a un choix à faire dans une modale, que le bouton qui active la modale et valide le choix se colle au-dessus de la
modale, comme sur le screen, et que quand on bouge l'un ou l'autre, les deux bougent. »

## Ce que montre la capture jointe (carte « Constant Training », Cyclops)
Deux pièces séparées à l'écran :
1. **Un bandeau d'action** en haut : titre « CHOOSE THE TARGET », compteur « 0/1 required · 8 possible », et deux boutons,
   « CANCEL » et le bouton de VALIDATION nommé d'après la carte (« CONSTANT TRAINING »).
2. **Un grand panneau « OFF-TABLE TARGETS »** dessous : « Constant Training · 8 cards », avec les huit cartes candidates.
Aujourd'hui le bandeau flotte au-dessus du panneau, plus étroit et décalé, sans lien visuel avec lui.

## Comportement voulu
- Le bandeau (titre, compteur, Annuler, bouton de validation) est COLLÉ au bord supérieur du panneau : même largeur, aucun
  écart, un seul bloc visuel.
- **Déplacer l'un déplace l'autre** : on peut glisser le bandeau OU le panneau, et l'ensemble suit (une seule unité).

## Où regarder
- `ui-app/src/board/AssistantAction.tsx` (assistant de choix de cible) et `ui-app/src/board/board.css`.
- Le glisser-déposer des fenêtres existe déjà ailleurs dans le plateau : réutiliser son mécanisme plutôt que d'en écrire un autre.
- Le panneau « hors table » est aussi utilisé par d'autres choix (cartes de défausse, paquet...) : vérifier que le collage ne
  casse aucun d'eux, y compris quand il n'y a PAS de panneau de cartes (choix simple sans liste).

## Questions à trancher le jour où on le fait
- Position de départ de l'ensemble (au centre, comme aujourd'hui, ou mémorisée entre deux choix) ?
- Sur téléphone ou petit écran, le bandeau reste-t-il collé en haut, ou se range-t-il sous le panneau ?
