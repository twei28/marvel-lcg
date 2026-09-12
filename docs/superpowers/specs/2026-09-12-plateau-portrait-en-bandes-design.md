# Le plateau portrait en bandes, avec la main et les piles derrière des encoches

**Décidé avec l'utilisateur le 12/09/2026**, en dix-neuf questions une à une,
après son premier vrai test du plateau portrait sur téléphone (livré le 11/09,
`2026-09-11-plateau-portrait-telephone-design.md`) : « je vois plein de
problèmes ».

Ce qu'il a dit, en substance : la main n'a pas à être visible tout le temps,
on devrait la sortir d'un swipe depuis une petite encoche à droite ; pareil
pour le deck et la défausse, derrière une encoche à gauche, parce qu'on ne va
presque jamais les voir ; et une fois ces deux choses rangées, le plateau a
la place d'avoir de vraies zones comme sur PC, avec la manigance principale et
les annexes dans la même zone, chaque zone étant une bande en paysage qu'on
fait glisser du doigt pour voir tout ce qu'elle contient.

## Les décisions

| Sujet | Décision |
|---|---|
| Main cachée | Une **encoche** collée au bord droit, avec le **nombre de cartes**. Swipe vers la gauche ou tap : la main s'ouvre. |
| Main ouverte | **La rangée actuelle, en bas** (`MainPortrait`), par-dessus le plateau. Se referme d'un tap en dehors, d'un swipe vers la droite, du Retour Android. |
| Main automatique | **Elle s'ouvre seule** dès qu'une question du moteur porte sur une carte en main (paiement, défausse, choix), et se range une fois la réponse donnée. |
| Encoche gauche | **Toutes les piles** : deck et défausse du joueur, deck et défausse de rencontre, set némésis, cartes écartées (victoire, retirées, mises de côté), deck spécial et réserve s'il y en a. |
| Tiroir gauche ouvert | **Un panneau latéral, une pile par ligne** : dos ou dernière carte, nom, compte. Un tap sur une pile consultable l'étale (modale « cartes regardées » du PC). |
| Zones | **4 bandes**, de haut en bas : **Méchant**, **Manigances**, **Engagés**, **Mon héros**. |
| Bande Méchant | Le méchant **épinglé à gauche** (fixe pendant le défilement) avec ses attachements ; environnements et cartes de scénario **à sa droite**. |
| Bande Manigances | La principale **épinglée à gauche** avec sa jauge ; les annexes à sa droite. |
| Bande Engagés | Les sbires engagés et leurs attachements. |
| Bande Mon héros | L'identité **épinglée à gauche** ; alliés, soutiens, améliorations à sa droite. |
| Défilement | Chaque bande **défile horizontalement** du doigt. **Le plateau défile verticalement** quand les 4 bandes dépassent la hauteur. Le bandeau reste fixe en haut. |
| Taille des cartes | **Lisibles : trois par largeur d'écran** (environ 150 px sur 480). |
| Attachements | **Glissés sous la porteuse**, comme sur PC (`.plateau-unite`). |
| Chiffres | **Une pastille par valeur sur la carte** : PV, menace, statuts. C'est ce que `ScanCard` dessine déjà ; on cesse de les retirer. |
| Bande vide | Elle **garde sa hauteur et affiche un texte** (« Aucun ennemi engagé »). |
| Tap / appui long | **Tap = ouvrir en grand** (`CarteOuverte`), **appui long = agir** (action directe du moteur, sinon le menu d'actions de la carte). Inchangé. |
| Questions | **Feuille en bas, comme aujourd'hui** (`DemandeCentrale`), cibles allumées dans les bandes. |
| Coop | **Des onglets sur la bande Mon héros**, un héros à la fois. Les trois autres bandes sont communes. |
| Cadre | **Bandeau en haut seulement.** La barre du bas disparaît. Options, Historique, Sauver, Salon, Journal, Musique, Langue, Quitter passent dans un menu **« … »** du bandeau, en feuille basse. |
| Fin du tour | **Dans le bandeau, à droite** : le bouton d'action principal (Fin du tour, et sa variante suggérée « ✓ »). |
| Paysage | **Même design, bandes plus larges** (cinq cartes par largeur). L'écran « Remets ton téléphone droit » disparaît. |
| Livraison | **Tout d'un coup**, testé par l'utilisateur à la fin. Le plateau PC ne change pas. |

## Ce qu'on retire

- `EcranPaysage` : le paysage reçoit le même plateau.
- `BarreBas` en portrait : plus de barre en bas. Le composant reste tant que
  `PlateauMedaillons` l'emploie.
- `CarteAvecChiffres`, `CompteursPortrait`, `BarreMenace` en portrait : les
  chiffres sont sur la carte (pastilles de `ScanCard`), la jauge de menace est
  celle de la carte. `BarreMenace` reste disponible mais n'est plus montée.
- L'ancien modèle **`?medaillons`** (`PlateauMedaillons`, `MainEventail`,
  `TiroirPiles` actuel, `RangeeMedaillons`, `Medaillon`, `ZoneFocus`,
  `bandes.ts`, `couches.ts`, `joueurs.ts`) : **retiré du dépôt**. Il était
  gardé « jusqu'à décider de son sort sur pièce » (spec du 11/09) ; le sort
  est décidé. Deux mécanismes d'historique (`couches.ts` et
  `retour-android.ts`) coexistaient, un seul reste. Le CSS de `CarteOuverte`
  et de `.pm-barre` (dans `medaillon.css`) déménage dans `portrait.css`.
- `ui-check/tests/plateau-paysage.spec.ts` : mort depuis la suppression du
  plateau paysage, supprimé.

## Architecture

### Les composants (`ui-app/src/board/mobile/`)

- **`PlateauPortrait.tsx`** (réécrit) : `<main class="plateau-portrait">` en
  colonne : `BandeauPortrait` fixe, `.portrait-table` qui défile
  verticalement et contient les 4 `Bande`, puis les couches : `EncocheMain` +
  `MainPortrait` en feuille, `TiroirPiles`, `CarteOuverte`, `PileRegardee`.
  Il ne décore plus lui-même : il passe `interactifs`/`effets` aux `Unite`,
  qui appellent `avecInteraction` (seule copie autorisée, `Board.tsx`).
- **`Bande.tsx`** (nouveau) : `{ cle, titre, epinglee?: UniteAffichee,
  unites: UniteAffichee[], texteVide, onglets?: ReactNode, ... }`. Rend
  `<section class="bande bande-<cle>">` avec un titre, un rail
  `.bande-rail` (`overflow-x: auto`, `scroll-snap-type: x proximity`), la
  carte épinglée en `position: sticky; left: 0` puis les autres. Chaque carte
  passe par **`Unite` de `Board.tsx`, exporté** : attachements glissés sous
  la porteuse, statuts, piles, stades, pastilles. Un tap sur une carte ouvre
  `CarteOuverte` (via `onCardClick` détourné : `Unite` reçoit
  `ouvrirCarte`), l'appui long agit (`useAppuiLong` dans une enveloppe
  `CarteBande`, une par carte).
- **`bandes-portrait.ts`** (remplace `blocs-portrait.ts`) : fonction pure
  `repartirEnBandes(plateau): BandesPortrait` →
  `{ vilain, manigances, engages, heros, main, piles }`.
  - `vilain.epinglee` = première unité de `rencontre` ; `vilain.unites` =
    autres unités de `rencontre` + cartes de `terrain-combat` de
    `kind === 'environment'`.
  - `manigances.epinglee` = `complot-principal[0]` ; `unites` =
    `complots-secondaires`.
  - `engages.unites` = `terrain-combat` sauf `ally` et `environment`.
  - `heros.epinglee` = l'identité (`kind === 'hero'` ou `'alter-ego'` dans
    `terrain-soutien`) ; `unites` = le reste de `terrain-soutien` + alliés de
    `terrain-combat` + `deck-special` et `reserve` **sans leurs piles**.
  - `piles` = `piles-joueur`, `piles-rencontre`, `nemesis`, `annexes`, et les
    unités à `pileContenu` de `deck-special`/`reserve`, chacune
    `{ cle, titre, unite, compte }`. Repérage par `unite.cle`
    (`joueur-deck`, `joueur-defausse`, `rencontre-encounter-deck`,
    `rencontre-encounter-discard`, `nemesis-set`, `annexes-*`), jamais par
    nom.
  - `main` = `main`.
- **`EncocheMain.tsx`** (nouveau) : `<button class="encoche encoche-main"
  data-tactile="main">` au bord droit, 48×72 px minimum, avec le nombre. Tap
  ou swipe vers la gauche (`pointerdown` puis `pointermove` de 24 px)
  déclenche `onOuvrir`. `EncochePiles` est le même composant au bord gauche
  (`encoche-piles`, `data-tactile="tiroir"`), sans nombre, icône « ≡ ».
- **`MainPortrait.tsx`** (adapté) : devient une feuille `.main-feuille`
  (voile `.main-feuille-voile`, `role="dialog"`), même rangée qu'aujourd'hui.
  Prop `ouverte`, `onFermer`. Swipe vers la droite sur la feuille = fermer.
- **`TiroirPiles.tsx`** (réécrit) : `{ piles, ouvert, onFermer, onOuvrirPile
  }`. Voile `.tiroir-voile` + `<aside class="tiroir">`, une `<button
  class="tiroir-pile">` par ligne (48 px), désactivée si rien à consulter.
- **`BandeauPortrait.tsx`** (étendu) : `{ monde, quiAgit, menu?: ReactNode,
  actionPrincipale?: { libelle, suggere?, agir } }`. Trois segments à gauche,
  puis `.portrait-menu-bouton` (« … », `data-tactile="menu"`) qui ouvre une
  feuille `.portrait-menu` contenant `menu` (= `actionsPartie` du PC, rendu
  en liste verticale par CSS, `.bh-etat` masqué), puis le bouton
  `.portrait-action` à droite.
- **`PlateauMobile.tsx`** : plus d'`EcranPaysage`, plus de `?medaillons`.
  Toujours `body.mode-plateau-portrait`, `useRetourAndroid`, plein écran.
- **`retour-android.ts`** : `FERMABLES` gagne `.main-feuille-voile`,
  `.tiroir-voile`, `.portrait-menu-voile`, `.plateau-regardees-voile` (déjà),
  `.menu-actions-carte`.

### La page (`ui-app/src/board.tsx`)

- Nouvelle prop de `BoardProps` : `actionPrincipale?: { libelle: string;
  suggere?: boolean; agir: () => void }`, remplie quand
  `afficherFinTourSimple` (`{ libelle: t('Fin du tour'), suggere:
  finDeTourSuggeree, agir: interaction.annuler }`). Le bouton flottant
  `.bouton-fin-tour` n'est plus rendu quand `modePlateau === 'mobile'`.
- `mainVisibleForcee` reste passé ; le portrait ne s'en sert pas (trop
  large). Le signal exact est local : **une question porte sur la main si une
  clé de `props.interactifs` est l'id d'une unité de `bandes.main`** avec un
  rôle `cible`, `ressource` ou `porteur`.
- `Unite` et `PileRegardee` sont exportés de `Board.tsx`.

### Le CSS (`portrait.css`, réécrit ; `menus-mobile.css`, ajusté)

- `.plateau-portrait { position: fixed; inset: 0; display: grid;
  grid-template-rows: auto 1fr }` ; `.portrait-table { overflow-y: auto;
  overscroll-behavior: contain }`.
- `.bande-rail { display: flex; gap: 8px; overflow-x: auto; padding: 6px 12px;
  scroll-snap-type: x proximity }` ; `.bande-epinglee { position: sticky;
  left: 0; z-index: 2; background: var(--fond) }`.
- `--card-w: clamp(140px, calc((100vw - 48px) / 3), 200px)` en portrait,
  `calc((100vw - 64px) / 5)` en paysage (`@media (orientation: landscape)`).
- `body.mode-plateau-portrait { --feuille-bas: 0px }` : les feuilles de
  `menus-mobile.css` descendent jusqu'au bord, la barre n'existe plus.
- Les règles anti-loupe (`transform: none`, `--inspect-scale: 1`) couvrent
  `.bande`, `.main-feuille`, `.tiroir`.
- Les pièges de couches restent (`@layer` cassé en production : `base` bat
  `composants` et `utilitaires`) : les surcharges de `board.css` gardent
  `!important`, celles de `ScanCard.css` vivent en `utilitaires`.

## Vérification

- **vitest** : `bandes-portrait.test.ts` (répartition, épinglées,
  environnement chez le méchant, piles repérées par clé) ;
  `PlateauPortrait.test.tsx` réécrit (4 bandes, textes vides, onglets coop
  sur la bande héros, main fermée par défaut, main ouverte par un tap sur
  l'encoche et par une question sur la main, tiroir, tap = ouvrir, appui long
  = agir) ; `BandeauPortrait.test.tsx` (menu, action principale) ;
  `retour-android.test.ts` (nouveaux fermables). Les tests de l'ancien modèle
  et de la barre du bas sont supprimés.
- **Playwright** `plateau-mobile.spec.ts` réécrit, projet `s24` (480×1050,
  tactile) sur les fixtures : `.plateau-portrait` visible, aucun débordement
  horizontal de la page, chaque carte des bandes ≥ 140 px de large, chaque
  `[data-tactile]` ≥ 44×44, la main fermée au départ (`.main-feuille`
  absente), un tap sur `.encoche-main` l'ouvre, un tap sur `.encoche-piles`
  ouvre le tiroir, zéro erreur console. `menus-mobile.spec.ts` adapté : les
  boutons sont dans le menu « … » du bandeau, les feuilles touchent le bas.
- **Sur le téléphone**, par l'utilisateur, à la fin.
