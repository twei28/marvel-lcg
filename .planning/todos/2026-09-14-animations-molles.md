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

### 6. La défausse n'est pas visée, c'est le deck qui l'est

**Demande de l'utilisateur, 14/09/2026** : « il faut que le point de départ soit
son vrai point de départ sur la table de jeu, et le point d'arrivée le vrai
point d'arrivée ».

Les cartes, elles, sont bien visées : `boiteDe(el)` lit la position réelle de
chaque `.scan-card[data-card-id]`. Les PILES ne le sont pas :

```js
const defausseJoueur = ancre('zone-piles-joueur', 1) ?? deckJoueur
const defausseRencontre = ancre('zone-piles-rencontre', 1) ?? deckRencontre
```

`ancre(zone, 1)` = la DEUXIÈME carte de la zone des piles. ⚠ Quand la défausse
est vide, elle n'est pas dessinée : il n'y a pas de deuxième carte, et le repli
`?? deckJoueur` envoie la carte voler **vers le deck**. Une carte défaussée part
donc se poser sur la pioche, ce qui est le contraire de ce qui se passe.

Même chose en sens inverse pour une carte qui revient de la défausse.

À corriger en visant les ZONES elles-mêmes (leur boîte) plutôt qu'une carte
dedans, pour que le point existe même quand la pile est vide.

## Lien avec la phase du méchant sur la table

Cette fiche est un PRÉREQUIS de
`2026-09-14-phase-du-mechant-sur-la-table.md` : l'utilisateur y demande « un
entre-deux qui fasse plus jeu de cartes, où on voit vraiment les cartes
bouger ». Des cartes molles y ruineraient tout l'effet recherché.

## Statut

⚠ **L'en-tête de cette fiche disait « non commencé » alors que cinq causes sur
six étaient corrigées.** Corrigé le 15/09/2026 en relisant le code, pas la
fiche.

Fait, et **derrière la garde d'essai** (`board/essais.ts`, réservée à un
compte) pour les quatre premières :

- (1) la durée suit la distance : `dureeDe()`, racine carrée, 130 à 400 ms ;
- (2) le « clac » rendu au coup UNIQUE et refusé aux arrivées groupées ;
- (3) l'inclinaison dans le sens du départ, bornée à 3 degrés ;
- (4) l'ombre qui s'écarte au décollage et se resserre à l'approche,
  plus le tressaillement de la pile qui reçoit ;
- (6) la place de la défausse DÉDUITE quand elle est vide, donc une carte
  défaussée ne vole plus vers la pioche. Hors garde d'essai, pour tout le
  monde.

Commits : `ebe3f172`, `4366749f`, `edfc211e`.

Reste (5) : au-delà de `MAX_VOLS = 10`, rien ne s'anime au lieu d'animer
autrement. Non commencé.

⚠ La garde d'essai est du code TEMPORAIRE : le jour où l'utilisateur valide le
poids et le geste à l'usage, le drapeau et ses deux branches disparaissent.

## Point 5 traité le 20/10/2026

Au-delà de `MAX_VOLS`, chaque groupe (pioche, mise en jeu, défausse) vole en UNE pile fantôme avec le nombre de cartes en pastille (`regrouper`, `CoucheAnimations.tsx`). Preuve : `ui-check/tests/animations-vol-groupe.spec.ts` (12 cartes piochées dans une vraie partie, 1 fantôme).

## CORRECTION du 21/10/2026 : la garde d'essai des animations n'existe plus dans le code

Cette fiche (ci-dessus) dit encore « derrière la garde d'essai » pour les points (1) à (4), et que
le point (5) attend la validation du geste. **Faux aujourd'hui** : relu dans `CoucheAnimations.tsx`,
aucune des cinq animations n'est conditionnée par `essaisOuverts()` ou tout autre drapeau — la classe
`est-essai` posée sur la racine du composant est un nom resté dans le code mais ne correspond à AUCUN
sélecteur CSS (vérifié : `grep -rn "est-essai" styles/`, zéro résultat). Les cinq points sont donc
déjà live pour tout le monde, sans garde, depuis une date non retrouvée dans l'historique.

Ce qui reste réellement réservé par `board/essais.ts` (`essaisOuverts()`) aujourd'hui : l'Épuré est
déjà ouvert à tous (`epurePourTous = true`, `affichage.ts`) ; seule la **couleur du halo/des marques**
(héros + méchant) reste derrière la garde — voir `2026-09-14-revoir-les-couleurs-du-halo.md` (item 30,
retiré du backlog le 21/10/2026, couleurs encore fausses pour certains héros, pas de passe de
validation prévue). Décision de l'utilisateur le 21/10/2026 : garder cette garde en place pour cette
raison. Item 7 du backlog clos.
