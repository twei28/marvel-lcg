# Les animations sont molles

**Constat de l'utilisateur, 14/09/2026** : « au niveau animation, on est très
mauvais. Je ne sais pas si c'est parce que toi tu n'y arrives pas ou si c'est
parce que c'est la manière dont c'est codé qui ne le permet pas, mais je trouve
ça très très un peu mou. »

## La réponse à sa question : c'est un choix, pas une limite

Le système existe et fonctionne (`ui-app/src/board/CoucheAnimations.tsx`, 228
lignes) : il diffe les positions d'un rendu à l'autre et fait voler une image
fantôme du départ à l'arrivée. Rien n'empêche de mieux faire.

Ce qui manque tient en cinq points mesurés, pas en une impression.

### 1. ⚠ LA DURÉE EST FIXE, ET C'EST LA CAUSE PRINCIPALE

`const DUREE = 250` : 250 ms **quelle que soit la distance**. Une carte qui
traverse l'écran met exactement le même temps qu'une carte qui bouge de trois
centimètres. Rien ne pèse, rien ne prend son élan.

C'est le point à corriger en premier : une durée qui suit la distance rend le
mouvement crédible avant même qu'on touche à la courbe.

### 2. La courbe a été volontairement privée de nerf

`transition: transform 250ms cubic-bezier(0.22, 0.75, 0.3, 1)`, avec ce
commentaire dans `board.css` : « Décélération douce SANS dépassement : le
"clac"/rebond précédent rendait l'arrivée groupée de plusieurs cartes fouillis.
Arrêt net et propre. »

⚠ Le rebond a donc été retiré pour régler un AUTRE problème : plusieurs cartes
qui atterrissent en même temps. La bonne correction n'est pas de le remettre
tel quel, mais de le rendre au coup UNIQUE et de le retirer aux arrivées
groupées.

### 3. Le vol est plat

Une seule `translate` + `scale`. Aucune rotation, aucune bascule, aucun
changement d'échelle en cours de route. Une vraie carte lancée tourne un peu.

### 4. La carte ne décolle jamais

`box-shadow` constante pendant tout le vol. Une ombre qui s'écarte et se
diffuse au décollage, puis se resserre à l'atterrissage, suffit à donner la
hauteur.

### 5. Au-delà de dix cartes, plus rien

`const MAX_VOLS = 10`, et c'est justifié (« 40 cartes qui volent en même temps »
= une resynchronisation, pas un coup). Mais la coupure est brutale : rien
n'anime au lieu d'animer autrement (une pile qui glisse d'un bloc, par exemple).

## Lien avec la phase du méchant sur la table

Cette fiche est un PRÉREQUIS de
`2026-09-14-phase-du-mechant-sur-la-table.md` : l'utilisateur y demande « un
entre-deux qui fasse plus jeu de cartes, où on voit vraiment les cartes
bouger ». Des cartes molles y ruineraient tout l'effet recherché.

## Statut

Constaté et analysé le 14/09/2026, **non commencé**. Ordre conseillé : la
durée (1), puis l'ombre (4), puis la courbe (2) ; la rotation (3) et les
grands lots (5) ensuite.
