# Le parcours solo au téléphone, en paysage

**Date :** 2026-09-07
**Statut :** conçu, validé par l'utilisateur en séance, à planifier
**Remplace :** `2026-08-02-plateau-mobile-design.md` pour le plateau (portrait
et médaillons abandonnés). Ce qui y est dit du modèle de layout PC reste vrai.
**Rapport à la roadmap :** MOB-01 à MOB-03 (phase 6, revue), et la partie
mobile de la phase 4 (assistant), traitée sans réécriture React.

---

## 1. Le problème

Le site se joue depuis un PC. Le plateau a reçu en août un rendu mobile en
portrait, fait de médaillons ronds et d'une zone focus. L'utilisateur, après
usage, ne veut plus de ce modèle : le terrain est grand, les médaillons perdent
trop, et un téléphone tenu en paysage donne assez de largeur pour montrer de
vraies cartes.

L'assistant de préparation (`Fusion/marvel-lcg-src/public/prepare.html`,
`js/prepare/app.js`, 3100 lignes de JS vanille) n'a jamais été pensé pour le
doigt : cinq media queries, aucune cible tactile, un survol pour ouvrir la
scène d'un héros. Il faut donc encore un PC pour lancer une partie.

Le but du chantier : **une partie solo, à un ou deux héros, préparée et jouée
de bout en bout depuis un téléphone tenu en paysage.**

## 2. Périmètre

**Dans le périmètre :**

- le plateau de jeu (`ui-app/src/board/mobile/`), redessiné en paysage ;
- l'assistant de préparation, adapté en place au doigt ;
- l'accueil de l'assistant (« Comment veux-tu jouer ? ») et la bulle qui
  conseille le paysage ;
- le retour au menu depuis le plateau et l'écran de fin de partie ;
- solo un héros et solo deux héros (hot-seat sur un seul appareil).

**Hors périmètre, chantier suivant :** multijoueur au téléphone (un appareil
par joueur), deck-builder, salon, rejoindre, campagne, galerie, pages
secondaires (cards, deck, replay, report).

**Hors périmètre, inchangé :** le plateau PC (`Board.tsx` et la scène à
l'échelle). Aucune ligne n'y est modifiée. Le moteur Python n'est pas touché.

## 3. Décisions de cadrage

| Sujet | Décision |
|---|---|
| Appareil de référence | Samsung S24 Ultra, Chrome. En paysage : environ 1050 x 480 px CSS en plein écran, 1050 x 430 avec la barre du navigateur |
| Orientation du plateau | **Paysage obligatoire.** En portrait, un écran « Tourne ton téléphone » couvre le plateau. La partie continue dessous |
| Orientation de l'assistant | Les deux sens fonctionnent. Une bulle conseille le paysage à l'accueil, fermable et mémorisée |
| Plein écran | Le premier tap sur le plateau demande `requestFullscreen()` puis `screen.orientation.lock('landscape')`. Un refus n'est pas une erreur : l'écran portrait reste le filet |
| Cartes posées | De **vraies cartes** (`ScanCard`), jamais des médaillons ni des tuiles |
| Modèle de layout | Deux rangées horizontales de cartes, main en éventail, barre basse. Une rangée qui déborde défile horizontalement |
| Assistant | Adapté en place : une feuille de style mobile, deux changements ciblés dans le rendu JS. Aucune réécriture React |
| Tablette | Même rendu que le téléphone (le pointeur grossier suffit à `REQUETE_MOBILE`), avec des cartes plafonnées à 150 px |

## 4. Le plateau en paysage

### 4.1 Composition

Quatre bandes, de haut en bas, dans une hauteur de 480 px (430 avec la barre
du navigateur) :

```
┌──────────────────────────────────────────────────────────────┐
│ Méchant │ Manig. principale │ Manig. │ Sbire │ Sbire │ ▸ │ 🂠 12 │  rangée ennemie
│ [▓▓▓]   │ [▓▓▓▓▓▓]          │ [▓▓]   │ [▓▓]  │ [▓▓]  │   │ 🂠  4 │  ~170 px
├──────────────────────────────────────────────────────────────┤
│ Héros   │ Allié │ Allié │ Soutien │ Amélio. │ ▸           │ 🂠 28 │  rangée héros
│ [▓▓▓]   │ [▓▓]  │ [▓▓]  │ [▓▓]    │ [▓▓]    │             │ 🂠  6 │  ~170 px
├──────────────────────────────────────────────────────────────┤
│   ╲[c]╱ ╲[c]╱ ╲[c]╱ ╲[c]╱ ╲[c]╱        main en éventail       │  ~90 px visibles
│  Annuler · Sauver · Options · Historique     [onglets héros]  │  barre basse 48 px
└──────────────────────────────────────────────────────────────┘
```

**Rangée ennemie**, dans l'ordre de lecture : méchant (`rencontre`),
manigance principale (`complot-principal`, format paysage, donc plus large à
hauteur égale), manigances secondaires (`complots-secondaires`), sbires
engagés et environnement (`terrain-combat`). À l'extrémité droite, épinglées
hors du défilement : les piles de rencontre (`piles-rencontre`), deck et
défausse, en dos de carte réduit avec leur compte.

**Rangée héros**, dans l'ordre : identité, alliés, soutiens, améliorations
(`terrain-soutien`), puis `deck-special`, `reserve`, `nemesis` quand ils
existent. Les améliorations et états attachés se glissent derrière leur
porteur, comme sur PC. À droite, épinglées : `piles-joueur` et `annexes`.

⚠ Ruling du 07/09/2026 (revue finale) : `annexes` porte aussi des cartes
posées (preuves, règles, ressources) ; seules ses piles sont épinglées, ses
cartes rejoignent la zone défilante de la rangée héros.

**Main** : `MainEventail` repris tel quel, mêmes gestes (appui pour ouvrir,
appui court pour agrandir, appui maintenu sur la grande carte pour jouer).

**Barre basse** : `BarreBas` reprise telle quelle, avec sa transformation
quand le moteur pose une question.

### 4.2 Taille des cartes

La largeur d'une carte se calcule depuis la hauteur disponible, en CSS :

```
--hauteur-rangee : (100dvh - 48px barre - 90px main - 2 x 14px étiquettes) / 2
--card-w         : clamp(84px, var(--hauteur-rangee) * 63 / 88, 150px)
```

Soit environ 110 px en plein écran, 95 px avec la barre du navigateur, 150 px
sur tablette. À ces tailles, `ScanCard` pose déjà le nom, le coût et les bulles
de stats ; le texte de règles n'est pas lisible, et c'est accepté : il se lit
dans la carte ouverte. `ScanCard` reçoit `--card-w` par la classe de la
rangée, comme `board.css` le fait déjà pour la scène PC (`board.css:893`).

La manigance principale reste en format paysage : même hauteur, largeur
88/63 fois plus grande.

⚠ Ruling du 07/09/2026 (tâche 12) : une carte posée ne se dimensionne plus
depuis une estimation en hauteur d'écran. Elle se dimensionne depuis la
hauteur RÉELLE de sa rangée, en unités de container query
(`.rangee-cartes-fenetre { container-type: size }`,
`--card-w: clamp(84px, (100cqh - 18px) * 63/88, 150px)`, 18 px étant la
jauge PV/menace qui déborde sous le cadre). La formule `100dvh - 166px` de
cette section est conservée seulement pour la main (`--pp-card-w`) et comme
estimation de conception dans `taille-carte.ts`
(`HAUTEUR_JAUGE = 18`). Raison : une estimation en `dvh` doit deviner la
hauteur de la barre du bas, et la page de fixtures la gonfle à 88 px à
cause de son bandeau « Saved state ». Mesurer la rangée fait tenir les
cartes quelle que soit la hauteur que prennent la barre, la zone de sécurité
ou une bannière.

### 4.3 Défilement d'une rangée

Une rangée qui ne tient pas défile horizontalement avec `scroll-snap` carte
par carte. Un voile dégradé au bord droit signale qu'il y a une suite, et un
compte « +N » sur ce voile dit combien de cartes sont hors champ. Les piles
épinglées à droite ne défilent pas.

Pendant un ciblage ou un paiement, ce qui n'est pas visable s'éteint (règle
actuelle, classes `est-en-ciblage` et `est-en-paiement`), et chaque rangée se
recale sur sa première cible visible (`scrollIntoView`).

### 4.4 États et attachements

Sonné, coriace et désorienté sont des cartes attachées par le moteur. Sur une
carte de 100 px, une carte glissée derrière ne se lit pas. Ils deviennent des
pastilles lettrées au coin supérieur droit de la carte (T, S, C, avec la
couleur et le libellé de la table `ETATS` du médaillon actuel, qui est
déplacée dans un module partagé). Les améliorations restent des cartes
glissées derrière le porteur, décalées de 12 px, tap possible sur la partie
visible.

### 4.5 Deux héros

En solo à deux héros, `terrain-soutien` porte les groupes des deux joueurs
(`proprietaires`, voir `joueurs.ts`). La rangée héros montre les deux groupes
séparés par un trait vertical, le héros actif en premier
(`ordreDAffichage`). La main affichée est celle du joueur actif ; les onglets
de la barre basse, déjà rendus par la page dans `outils`, changent de joueur.
Le badge « Actif » de `heroActifId` est posé sur l'identité concernée.

### 4.6 Ouvrir une carte, agir

Le tap sur une carte posée ouvre `CarteOuverte` (carte en grand, texte
lisible, actions). Le menu d'actions de la page (`MenuActionsCarte`) et le
sélecteur de cibles hors table continuent d'être inscrits dans la pile de
couches (`couches.ts`) pour que le Retour d'Android ferme la couche du sommet
et non la partie.

### 4.7 Phase du méchant

Le cartouche du déroulé détaillé (`DeroulePhase`) se pose à la place de la
main pendant la phase du méchant : la main n'est pas jouable à ce moment, et
la hauteur ne permet pas les deux. Il garde ses boutons Précédent, Suivant et
« la règle », en cibles de 44 px. Quand le moteur pose une question pendant la
phase (défense, ordre des sbires), la barre basse se transforme comme
aujourd'hui.

### 4.8 Plein écran et portrait

Un module `plein-ecran.ts` expose deux fonctions pures testables (faut-il
demander le plein écran, faut-il afficher l'écran portrait) et un hook qui
les branche : premier `pointerdown` sur le plateau en mode mobile,
`requestFullscreen()` sur `document.documentElement`, puis
`screen.orientation.lock('landscape')` dans le `then`. Toute exception est
avalée : le filet est l'écran portrait.

`EcranPortrait.tsx` : un voile plein écran, une icône de téléphone qui tourne
en CSS, le texte « Tourne ton téléphone : le plateau se joue en paysage. » Il
est monté par `PlateauMobile` quand `useOrientation()` rend `portrait`. Il ne
démonte pas le plateau (aucun état perdu, la connexion au moteur continue).

### 4.9 Ce qui disparaît, et quand

Supprimés **après** la partie terrain validée (§7), dans un commit séparé :
`Medaillon.tsx`, `RangeeMedaillons.tsx`, `TiroirPiles.tsx`, `ZoneFocus.tsx`,
`medaillon.css`, la branche portrait de `PlateauMobile.tsx` et les
affirmations portrait de `plateau-mobile.spec.ts`. Le projet Playwright `s24`
(480 x 1050) est conservé : il sert à vérifier l'écran portrait (§7.1).
`bandes.ts` est remplacé par `rangees.ts` (§5.1).

Conservés : `MainEventail`, `BarreBas`, `CarteOuverte`, `useAppuiLong`,
`couches.ts`, `joueurs.ts`, `useModeMobile`, `useOrientation`.

⚠ Ruling du 07/09/2026 (tâche 12) : le filet `plateau-mobile.spec.ts` de
l'ancien rendu est rouge depuis `a1de7adb` (`.tiroir-languette` 18 x 56 px),
antérieur à ce chantier ; laissé tel quel jusqu'à la suppression.

⚠ Ruling du 07/09/2026 (revue finale) : `PlateauPaysage` dépend de
`medaillon.css` pour la main, la barre, le bouton Payer et la carte ouverte.
Le sous-projet 3 DÉCOUPE `medaillon.css` (ces règles migrent dans
`paysage.css`) et ne le supprime qu'ensuite.

## 5. Architecture du plateau

Le mode mobile reste un **rendu alternatif des mêmes objets** : `zones.ts`
découpe, `board.tsx` choisit `PlateauMobile` ou `Board` selon
`useModeMobile()`, les deux acceptent les mêmes `BoardProps`. Rien de cela ne
change.

### 5.1 Nouveaux modules

| Fichier | Rôle | Testé par |
|---|---|---|
| `mobile/rangees.ts` | Table pure : les 12 `CleEmplacement` rangés en deux rangées (`ennemie`, `heros`) plus `main`, et pour chaque rangée ses emplacements défilants et ses emplacements épinglés. Le test vérifie qu'aucun emplacement de `zones.ts` n'est orphelin, comme `bandes.test.ts` aujourd'hui | vitest |
| `mobile/taille-carte.ts` | La formule du §4.2 en fonction pure (hauteur de fenêtre, hauteur des bandes fixes) pour la tester ; le CSS la reproduit | vitest |
| `mobile/plein-ecran.ts` | Règles pures du §4.8 et hook | vitest |
| `mobile/etats.ts` | La table `ETATS` sortie du médaillon | vitest existant déplacé |
| `mobile/RangeeCartes.tsx` | Une rangée : étiquette, zone défilante de `ScanCard`, voile « +N », piles épinglées | vitest (rendu, compte « +N ») |
| `mobile/PilesEpinglees.tsx` | Deck et défausse en dos réduit avec compte, tap ouvre la pile (reprend `pileRegardee`) | vitest |
| `mobile/EcranPortrait.tsx` | Le voile du §4.8 | Playwright |
| `mobile/PlateauMobile.tsx` | Réécrit : compose les deux rangées, la main, la barre, le cartouche, les couches | `PlateauMobile.test.tsx` réécrit |
| `mobile/mobile.css` | Réécrit pour les rangées, garde main et barre | Playwright |

### 5.2 Ce qui est partagé avec le PC, sans modification

`ScanCard`, `card-model.ts`, `zones.ts`, `interaction.ts`, `world.ts`,
`SelecteurCibles`, `MenuActionsCarte`, `HistoriquePartie`, `DeroulePhase`.

### 5.3 Erreurs et cas limites

- **Rangée vide** (aucun sbire, aucun allié) : l'étiquette reste, la zone
  montre un emplacement vide en pointillé, la hauteur ne bouge pas.
- **Plus de 12 cartes dans une rangée** : le défilement absorbe tout, le
  « +N » compte juste. Aucune condensation.
- **Écran plus bas que 360 px** (barre du navigateur plus clavier) : la
  largeur de carte touche son plancher de 84 px et la main passe à 60 px
  visibles. En dessous, on accepte un débordement vertical de la main seule.
- **Plein écran refusé** ou verrouillage impossible (iOS Safari) : rien ne
  casse, l'écran portrait fait le travail à chaque rotation.
- **Rotation en pleine question du moteur** : la question reste dans la barre
  basse, l'écran portrait la couvre, elle est toujours là au retour.

## 6. L'assistant et l'accueil

### 6.1 La bulle « passe en paysage »

Dans `accueilView()`, sur `(pointer: coarse)` et en portrait, une bulle sous
« Comment veux-tu jouer ? » : « Le plateau se joue en paysage. Tu peux
préparer ta partie dans les deux sens. » Un bouton Fermer. Clé
`localStorage` `bulle-paysage-fermee`. Jamais réaffichée après fermeture.

Au lancement, si le téléphone est en portrait, le bouton final porte une ligne
« Pense à tourner ton téléphone » au-dessus de « Lancer ». Il ne bloque pas.

### 6.2 La feuille mobile

`public/css/prepare/prepare-mobile.css`, chargée après `prepare.css` dans
`prepare.html`, avec son cache-buster. Tout y est sous
`@media (max-width: 700px), (pointer: coarse)`. Elle ne redéfinit que ce qui
change sur téléphone ; les media queries existantes de `prepare.css` restent.

| Étape | Ce que la feuille change |
|---|---|
| Barre d'étapes | `.progress` réduite au titre en haut ; une barre fixe en bas (`.nav-mobile`) avec Précédent, le nom de l'étape, Suivant ; boutons de 48 px de haut. `.stage` reçoit un `padding-bottom` de 80 px |
| Accueil | `.acc-modes` en une colonne, `.acc-nombre` à 44 px, `.acc-titre h1` à 44 px |
| Équipe | `.hero-grid` sur deux colonnes (existe déjà sous 560 px, étendu au pointeur grossier), `.tb-scene` masquée, `.search` pleine largeur, `.slots` en grille de deux |
| Decks | même gabarit « arsenal » que l'Équipe : `.tb-scene` masquée, `.tb-droite` pleine largeur, la liste des decks (`.tb-roster-deck`, déjà une grille) sur deux colonnes, `.tb-arsenal-outils` en boutons pleine largeur, bouton « Voir les cartes » qui ouvre la feuille défilante existante (`ouvrirCartesHeros`) |
| Méchant | `.scn-grid` sur deux colonnes, `.faceoff` en colonne, `.fo-vs` centré, les puces modulaires (`.mod-chip`) à 44 px de haut et en flux pleine largeur |
| Final | `.layout` en une colonne, `.recap` devient le corps de l'étape, bouton Lancer dans la barre fixe du bas, raison de blocage juste au-dessus |
| Paysage sur téléphone | grilles sur trois colonnes, barre d'étapes toujours en bas |

### 6.3 Les deux changements dans `app.js`

1. **La fiche du héros au tap.** Aujourd'hui `herosSurvole` alimente
   `rendreScene(h)` au survol. Sur pointeur grossier, le tap sur une tuile de
   héros ouvre une fiche repliée sous la grille (portrait, bio par `pliBio`,
   bouton « Choisir ce héros », bouton « Voir ses cartes »). Le second tap sur
   la même tuile, ou le bouton, l'assigne au siège (`assignHero`).
2. **Le récapitulatif replié.** Sur les étapes Équipe, Decks et Méchant, la
   colonne `.recap` se replie en un bouton « Ton équipe » dans la barre du bas,
   qui l'ouvre en feuille par-dessus. À l'étape Final elle est le corps.

Aucune autre logique ne bouge : `state`, `goto`, `stepComplete`, `launch`
restent tels quels.

### 6.4 Bouts du parcours

- **Retour au menu depuis le plateau** : le bouton existe dans les options ;
  il doit rester à 44 px dans la barre basse et sortir du plein écran
  (`document.exitFullscreen()`) avant de naviguer.
- **Fin de partie** (`fin-partie.ts` et son écran) : vérifiée en 1050 x 480,
  boutons à 44 px, aucun débordement.

## 7. Preuves

### 7.1 Automatiques

- **vitest** (`ui-app`) : les modules purs du §5.1, plus `PlateauMobile.test.tsx`
  réécrit (deux rangées présentes, piles épinglées, deux héros séparés, écran
  portrait monté quand l'orientation est portrait).
- **Playwright** (`ui-check`) : un projet `s24-paysage` (1050 x 480,
  `hasTouch`, `isMobile`) joué sur les 34 états enregistrés de
  `fixtures.html`, avec trois affirmations : aucun débordement vertical de
  `.plateau-mobile`, chaque `.scan-card` posée mesure au moins 84 px de large,
  chaque cible tactile au moins 44 px dans les deux axes. Un second projet
  `s24-portrait-plateau` (480 x 1050) vérifie sur trois états que
  `.ecran-portrait` couvre la fenêtre. Le test `plateau-mobile.spec.ts` actuel
  est remplacé, pas cumulé.
- **Captures** : l'assistant est déjà capturé sur le gabarit `mobile`
  (390 x 844) par `npm run captures`. Les références sont refaites une fois le
  design validé à l'écran, en une passe, avec `captures:valider`.

### 7.2 Terrain

Le critère de fin du chantier : une partie solo complète, un héros puis deux
héros, depuis le S24 Ultra par le tunnel, de l'accueil de l'assistant au bilan
de fin de partie, sans toucher un PC. Les médaillons ne sont supprimés qu'après
cette partie.

## 8. Livraison

Inchangée. `bash ui-app/deployer.sh` pour le plateau ; cache-busters de
`prepare.html` recalculés par le build pour la feuille mobile. Aucun fichier du
moteur Python touché, ce que `test_cards` et la batterie complète confirment
sans rien avoir à prouver de nouveau.

## 9. Découpage en sous-projets

Chacun reçoit son plan d'implémentation, dans cet ordre :

1. **Plateau paysage** : §4, §5, §7.1 côté plateau. Il décide si le pari des
   vraies cartes tient sur l'écran, et on le saura dès les premières captures
   Playwright.
2. **Assistant au doigt** : §6.1 à §6.3, captures de l'assistant.
3. **Bouts du parcours et terrain** : §6.4, partie terrain du §7.2,
   suppression des médaillons (§4.9).
