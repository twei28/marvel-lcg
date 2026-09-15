# La barre « Vue » était tombée dans le bouton « Partie »

**Constat de l'utilisateur, 15/09/2026**, en partie à plusieurs : « j'ai plus le
bouton dans le header pour choisir de voir tous les héros ou que celui que je
sélectionne ».

## Ce que c'était

Pas une disparition : un **déménagement non voulu**, hérité de la refonte des
réglages en fenêtre à onglets (14/09/2026).

⚠ **La décision écrite disait le contraire.** `2026-09-14-reglages-fenetre-a-onglets.md`,
tableau des décisions : « Un bouton "Partie" séparé dans la barre : historique,
log, journal, sauvegardes, quitter. **La Vue reste dans la barre** (elle change
à chaque tour en multijoueur). » L'implémentation l'avait pourtant rangée à
l'intérieur de `<PopoverPartie>`, donc derrière deux clics.

Vérifié avant de conclure : le bundle déployé contient bien `bh-vue`
(`board-gXRhbhhj.js`), le contrôle n'avait pas été supprimé.

## Le correctif

Le bloc est remonté dans la barre, juste avant le bouton « Partie », avec le
commentaire qui rappelle la décision pour que la prochaine refonte ne le
reprenne pas.

Il reste conditionné à **plus d'un joueur** : en solo il n'y a qu'une vue
possible, un bouton n'y proposerait rien.

## ⚠ Ce qui n'est PAS prouvé

Aucun cas automatique ne couvre la barre du haut : `board.tsx` n'est pas monté
en vitest (1576 cas verts, mais aucun ne regarde cet en-tête). La preuve est
visuelle, à faire à deux joueurs après déploiement.

C'est le trou qui a laissé passer le défaut, et il vaut pour tous les boutons
de cette barre : **à envisager, une spec `ui-check` qui compte les boutons du
header sur une partie à deux.**

## Statut

**Corrigé le 15/09/2026.** Non déployé, preuve visuelle à faire.
