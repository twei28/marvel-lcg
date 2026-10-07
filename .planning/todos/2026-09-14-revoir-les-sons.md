# Revoir les sons

> **Mise à jour du 07/10/2026 (audit du backlog)** : Statut « non commité » PÉRIMÉ : `b175b2ef` (07/10) a intégré les sons CC0, le volume réglable et le survol. RESTE : demander à l'utilisateur quels déclencheurs tombent mal. Déploiement des sons non vérifié.

**Demande de l'utilisateur, 14/09/2026**, dans la foulée des animations : « et
après il faudra revoir les sons aussi ».

Aucune précision donnée à ce stade : à cadrer avec lui avant de toucher quoi
que ce soit. La demande est notée pour ne pas se perdre, pas pour être devinée.

## Ce qu'il faudra lui demander

- Ce qui le gêne : les sons eux-mêmes (trop plats, mal choisis), leur
  DÉCLENCHEMENT (au mauvais moment, absents sur certains coups), ou leur
  mélange (trop fort, trop de sons en même temps) ?
- S'il veut des sons LIÉS AU MOUVEMENT des cartes, ce qui rejoint directement
  `2026-09-14-animations-molles.md` : un vol sans son paraît toujours mou, quel
  que soit le soin mis à la courbe.

## Ce qui existe déjà

`docs/reference/SONS-DECLENCHEURS.md` décrit les sons et leurs déclencheurs, et
le réglage « Sons » (onglet « Image et son ») les coupe. À relire avant d'en
parler avec lui : la fiche dira ce qui est déjà couvert et ce qui ne l'est pas.

## Statut

**Cadré le 15/09/2026**, cinq questions posées une à une. La spec fait foi :
`docs/superpowers/specs/2026-09-15-refonte-des-sons-design.md`, qui porte la
LISTE DE COURSES des 21 sons (ce que chacun doit évoquer, sa durée, sa
fréquence).

Décisions : l'utilisateur fournira les fichiers à partir de cette liste ; les
sons de MOUVEMENT seront joués par le plateau, là où la carte vole, et non par
le moteur ; le volume et les déclencheurs peuvent être traités avant les
fichiers.

⚠ Reste à lui faire nommer QUELS déclencheurs tombent au mauvais moment. Il dit
que certains arrivent mal, on ne sait pas lesquels. Ne rien déplacer avant.

## 07/10/2026 : intégré (non commité, non déployé)

Page d'écoute en quatre versions (Kenney rejeté : « génériques, moches,
8 bits » ; Sonniss bloqué par Cloudflare ; retenu : Freesound CC0). Choix et
intégration détaillés dans la spec, section « Statut au 07/10/2026 ».
Sources : `Fusion/marvel-lcg-src/assets/sounds/SOURCES.md`.
