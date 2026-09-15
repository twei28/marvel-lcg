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

## Le correctif pressenti

Ouvrir le menu sur la liste DÉJÀ calculée (`actions`) au lieu de déléguer à
`focaliserCible`, qui la recalcule sans la source. À vérifier : le menu sait-il
recevoir une liste d'options imposée, ou faut-il lui ajouter cette entrée ?

⚠ Ne pas se contenter du vert : un cas sur `glisser-plateau.spec.ts` doit
prouver que l'attaque d'un allié n'apparaît PAS quand c'est le héros qu'on
lâche. Un cas qui vérifie seulement que l'attaque du héros est là resterait
vert avec le défaut.

## Statut

Cause identifiée le 15/09/2026, **correctif non écrit**. À faire après le
chantier de l'ouverture silencieuse.
