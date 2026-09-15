# Le glisser-déposer perd sa source quand il y a plusieurs actions

**Constat de l'utilisateur, 15/09/2026** : « quand je drag n drop mon perso sur
le méchant, il me propose deux attack, l'une d'elle c'est l'attaque avec un
allié, pourquoi ? ce n'est pas l'allié que j'ai drag n drop ».

## La cause, lue dans le code (pas mesurée en jeu)

`board.tsx`, `onDepot` (vers la ligne 2167) calcule d'abord les actions de la
SOURCE, correctement filtrées :

```js
const actions = optionsDuDepot(optionsCourantes, sourceId, cible.carteId, idIdentiteGlisser)
if (actions[0] && actions.length === 1) { ...joue l'action... }
if (actions.length > 1) {
  // Plusieurs actions visent cette carte : on ouvre le menu de
  // ciblage, celui-la meme qu'un clic sur la cible aurait ouvert.
  interaction.focaliserCible(cible.carteId)
}
```

⚠ **Le repli jette la liste filtrée.** `focaliserCible` ouvre le menu de la
CIBLE, et ce menu liste par construction toutes les actions qui peuvent viser
cette carte, quelle que soit la carte qui les porte (`interaction.ts:132` :
« le panneau central liste alors les actions disponibles qui peuvent viser
CETTE carte »). L'attaque de l'allié en fait partie.

Dès que la source a DEUX actions contre la cible, le geste perd donc sa source.
Avec une seule action, rien ne se voit : elle part directement.

## Le correctif, écrit le 15/09/2026

`focaliserCible(id, source?)` retient désormais la carte LÂCHÉE, et le menu de
cible se restreint à ses actions quand elle est connue. Sans source (un clic
direct sur la cible), rien ne change : le menu liste tout ce qui peut la viser,
c'est son rôle.

La règle « les actions de cette source » n'est pas réécrite : le menu appelle
`optionsDeLaSource` (`glisser/cibles.ts`), la MÊME fonction que le
glisser-déposer. Deux définitions auraient divergé, et le menu aurait rouvert la
porte qu'on ferme ici.

Quitter le focus d'une cible oublie la source : les cinq remises à zéro de
`cibleFocus` remettent aussi `sourceDepot` à `undefined`.

### Ce qui le prouve

Trois cas dans `ui-app/src/board/interaction.test.ts`, vus ROUGES d'abord
(« expected [1, 2] to equal [1] ») :

- lâcher le héros ne montre QUE l'action du héros, pas celle de l'allié ;
- une action générale (`bind_id === 0`) suit bien le héros, puisqu'elle est
  rattachée à son identité ;
- un clic direct sur la cible montre toujours les deux : le comportement du
  clic ne bouge pas.

Batterie complète du plateau : 1567 cas verts, 137 fichiers. Typage propre.

### ⚠ Ce qui n'est PAS prouvé

Le câblage de `board.tsx` (le dépôt qui PASSE sa source au menu) n'est couvert
que par le typage. Le cas de bout en bout existe (`ui-check/tests/glisser-plateau.spec.ts`,
`npm run glisser`) mais il **crée une nouvelle partie sur le serveur de jeu et
détruit celle en cours**, et il testerait le bundle déployé, c'est-à-dire
l'ancien code. À lancer après le prochain déploiement, pas avant.

## Statut

Cause identifiée et **correctif écrit le 15/09/2026**, vérifié par trois cas
unitaires vus rouges d'abord. Non déployé, et le bout-en-bout reste à jouer.

⚠ **Déployé le 15/09/2026 à 13h02** (bundle `board-CpIPLEv8.js`). Un rechargement
forcé du navigateur (Ctrl+F5) est nécessaire pour le voir.
