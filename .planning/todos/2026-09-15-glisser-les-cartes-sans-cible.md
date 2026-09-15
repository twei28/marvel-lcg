# Glisser une carte qui ne vise rien

**Demande de l'utilisateur, 15/09/2026**, capture à l'appui (« One Way or
Another » soulevée au-dessus de « Héros et soutiens », étiquette rouge « Not
here ») : « les événements qui n'ont pas de cible, j'aimerais aussi juste
pouvoir les glisser sur le terrain de jeu ».

## La cause

`zonesDeLaSource` (`ui-app/src/board/glisser/cibles.ts`) ne connaît que les
options qui VISENT quelque chose : elle saute d'emblée celles dont la plage de
cibles est vide (`target_num_range[1] <= 0`). Une carte sans cible n'avait donc
aucune zone d'atterrissage, et le plateau répondait « Pas ici » partout. Il
fallait passer par le menu de la carte.

`optionsSansCible` existait déjà et rangeait bien ces actions à part, mais
personne ne s'en servait pour ouvrir une zone.

## Le correctif

`zonesSansCible(options, source, identite)` ouvre **les deux rangées du terrain
du joueur** (`terrain-soutien`, `terrain-combat`) dès que la carte porte une
action offerte sans cible.

⚠ **Pas la zone du méchant, ni les piles.** Y lâcher une carte veut dire « je
vise ça », et une carte sans cible ne vise justement rien : l'accepter là
laisserait croire qu'on a ciblé quelque chose.

Au lâcher : une seule action sans cible, elle part directement ; plusieurs, le
menu de la CARTE s'ouvre (pas celui de la zone, qui n'a rien à dire ici).

## Ce qui le prouve

Quatre cas dans `ui-app/src/board/glisser/cibles.test.ts`, vus rouges d'abord
(`zonesSansCible is not a function`) :

- une action sans cible ouvre les deux zones du terrain ;
- une action sans cible REFUSÉE n'en ouvre aucune ;
- une carte qui vise, elle, n'ouvre pas le terrain (témoin : on n'a pas ouvert
  les vannes pour tout le monde) ;
- une action générale (`bind_id === 0`) suit l'identité.

Batterie complète : 1574 cas verts, typage propre.

## ⚠ Ce qui n'est PAS prouvé

Le câblage de `board.tsx` (zones légales, libellé du survol, lâcher) n'est
couvert que par le typage, comme les deux autres correctifs du 15/09/2026. Le
cas de bout en bout (`npm run glisser`) détruit la partie en cours et vise le
bundle déployé : à jouer après le prochain déploiement.

## Statut

**Fait le 15/09/2026.** Non déployé, pas encore essayé à la main.

⚠ **Déployé le 15/09/2026 à 13h02** (bundle `board-CpIPLEv8.js`). Un rechargement
forcé du navigateur (Ctrl+F5) est nécessaire pour le voir.
