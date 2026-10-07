# Mode manuel : le panneau d'aide ne doit pas cacher l'agrandissement de la carte (07/10/2026)

**Statut : BACKLOG, demande de l'utilisateur. Rien n'est commencé.**

## Le défaut (ses mots)
« En manuel, quand on ouvre l'aide, la zone d'agrandissement de la carte doit se mettre à côté du panneau d'aide, car là le
panneau cache l'agrandissement de la carte. »

## Comportement voulu
Quand le panneau d'aide du mode manuel est ouvert, l'aperçu agrandi de la carte (celui qu'on obtient au survol) ne doit plus être
recouvert : il se place À CÔTÉ du panneau d'aide (à sa gauche, dans l'espace resté libre), pas dessous.

## Où regarder
- `ui-app/src/board/manuel/VoletAideManuel.css` : le panneau est en `position: fixed; right: 0; width: min(380px, 92vw);`
  avec `z-index: 610` (et 605 / 612 pour sa languette), donc il passe AU-DESSUS de l'aperçu de la carte.
- L'aperçu agrandi : `ui-app/src/board/apercu-survol.ts` et le composant qui le dessine (chercher dans `board.css` /
  `Board.tsx`) ; il faut qu'il connaisse la largeur occupée par le panneau d'aide quand celui-ci est ouvert.

## À vérifier quand on le fait
- Petit écran / téléphone (la feuille du panneau passe à `min(380px, 92vw)` puis une media-query à 760 px) : là, pas de place à côté.
  Que fait l'aperçu : se range au-dessus du panneau, ou le panneau se replie pendant le survol ?
- L'aperçu doit revenir à sa place d'origine quand l'aide se referme.
