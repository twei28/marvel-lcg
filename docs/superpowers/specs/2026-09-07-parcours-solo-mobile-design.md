# Le parcours solo au téléphone, en portrait

**Date :** 2026-09-07, révisée le soir même après le premier terrain
**Statut :** conçu, validé par l'utilisateur en séance (version 2), à planifier
**Remplace :** la version 1 de cette spec (paysage obligatoire, deux rangées),
retirée après le premier essai sur le téléphone, et
`2026-08-02-plateau-mobile-design.md` (portrait à médaillons). Ce que ces deux
textes disent du modèle de layout PC reste vrai.
**Rapport à la roadmap :** MOB-01 à MOB-03 (phase 6, revue), et la partie
mobile de la phase 4 (assistant), traitée sans réécriture React.

---

## 0. Historique, pour ne pas refaire les mêmes essais

| Quand | Modèle | Pourquoi abandonné |
|---|---|---|
| Août 2026 | Portrait, médaillons ronds et zone focus | Le terrain est grand, les médaillons perdent trop : l'utilisateur veut voir de vraies cartes |
| 07/09/2026, journée | Paysage obligatoire, deux rangées de vraies cartes mesurées à la hauteur de la rangée | Sur le téléphone, dès que la barre du navigateur est visible, la rangée n'a plus la hauteur d'une carte au plancher et la carte est coupée. La hauteur est la ressource rare en paysage ; en portrait elle abonde |

Ce que la journée du 07/09 a produit reste utile à 70 % : la carte posée avec
ses états en pastilles, les piles épinglées, la rangée qui défile avec son
voile « +N », le compte des cartes hors champ, le plein écran au premier
geste, la pile de couches. Seule la composition change.

## 1. Le problème

Le site se joue depuis un PC. L'utilisateur veut préparer et jouer une partie
solo depuis son téléphone, tenu en portrait comme n'importe quelle
application. Trois choses manquent :

- un plateau en portrait qui montre de **vraies cartes entières**, jamais
  rognées ;
- des **menus pensés pour le doigt** : le menu d'actions d'une carte, le
  choix d'une cible ou d'une carte hors table, les questions du moteur, les
  panneaux Options, Historique, Sauvegardes, la fin de partie. Aujourd'hui
  tout cela est partagé avec le PC et posé pour une souris ;
- un **assistant de préparation** (mode, héros, deck, méchant) utilisable au
  doigt sur 480 px de large.

Le but du chantier : **une partie solo, à un ou deux héros, préparée et jouée
de bout en bout depuis un téléphone tenu en portrait, sur
narwhalchampions.com.**

## 2. Périmètre

**Dans le périmètre :**

- le plateau de jeu (`ui-app/src/board/mobile/`), redessiné en portrait ;
- tout ce qui s'ouvre par-dessus le plateau (§5) ;
- l'assistant de préparation, adapté en place au doigt (§6) ;
- le retour au menu depuis le plateau et l'écran de fin de partie ;
- solo un héros et solo deux héros (hot-seat sur un seul appareil).

**Hors périmètre, chantier suivant :** multijoueur au téléphone (un appareil
par joueur), deck-builder, salon, rejoindre, campagne, galerie, pages
secondaires (cards, deck, replay, report).

**Hors périmètre, inchangé :** le plateau PC (`Board.tsx` et la scène à
l'échelle) et le rendu PC de chaque panneau. Le moteur Python n'est pas
touché.

## 3. Décisions de cadrage

| Sujet | Décision |
|---|---|
| Appareil de référence | Samsung S24 Ultra, Chrome. En portrait : 480 px de large, 1050 px de haut en plein écran, environ 950 avec la barre du navigateur |
| Orientation du plateau | **Portrait obligatoire.** En paysage, un écran « Tourne ton téléphone » couvre le plateau. La partie continue dessous |
| Orientation de l'assistant | Portrait, sans conseil ni bulle : le téléphone est déjà dans le bon sens |
| Plein écran | Le premier tap sur le plateau demande `requestFullscreen()`. Aucun verrouillage d'orientation. Un refus n'est pas une erreur |
| Cartes posées | De **vraies cartes** (`ScanCard`), entières, jamais rognées |
| Modèle de layout | Quatre rangées horizontales de cartes, main en éventail, barre basse. Une rangée qui déborde défile horizontalement ; si l'écran est trop court, la colonne des rangées défile verticalement, on ne coupe jamais une carte |
| Menus | Un seul motif, la feuille basse (§5), pilotée par CSS sous une classe posée sur `body`, sans réécrire les composants |
| Assistant | Adapté en place : une feuille de style mobile, deux changements ciblés dans le rendu JS. Aucune réécriture React |
| Un seul rendu mobile | Les médaillons et le plateau paysage sont supprimés dans ce chantier, pas après |
| Tablette | Même rendu que le téléphone (le pointeur grossier suffit à `REQUETE_MOBILE`), cartes plafonnées à 130 px, donc plus de cartes par rangée |

## 4. Le plateau en portrait

### 4.1 Composition

Six bandes, de haut en bas, dans 480 px de large :

```
┌──────────────────────────────┐
│ MÉCHANT · MANIGANCES      🂠 🂠 │  rangée 1, ~185 px
│ [▓▓▓] [▓▓▓▓▓▓] [▓▓▓] ▸ +2     │
│  12PV    3/7                 │
├──────────────────────────────┤
│ SBIRES · ENVIRONNEMENT        │  rangée 2
│ [▓▓▓] [▓▓▓]                  │
├──────────────────────────────┤
│ HÉROS · ALLIÉS                │  rangée 3
│ [▓▓▓] [▓▓▓] [▓▓▓]            │
├──────────────────────────────┤
│ SOUTIENS · AMÉLIORATIONS  🂠 🂠 │  rangée 4
│ [▓▓▓] [▓▓▓] [▓▓▓] [▓▓▓]      │
├──────────────────────────────┤
│  ╲[c]╱ ╲[c]╱ ╲[c]╱ ╲[c]╱      │  main en éventail, ~120 px visibles
│ Annuler · Sauver · Options …  │  barre basse, 48 px
└──────────────────────────────┘
```

Chaque rangée a son étiquette, sa zone qui défile horizontalement et, à
droite hors du défilement, ses piles épinglées :

| Rangée | Emplacements défilants (`zones.ts`) | Épinglés |
|---|---|---|
| 1. Méchant et manigances | `rencontre`, `complot-principal` (format paysage), `complots-secondaires` | `piles-rencontre` |
| 2. Sbires et environnement | `terrain-combat` | aucun |
| 3. Héros et alliés | l'identité et les alliés de `terrain-soutien`, un groupe par joueur, l'actif en premier | aucun |
| 4. Soutiens et améliorations | les soutiens et améliorations de `terrain-soutien`, puis `deck-special`, `reserve`, `nemesis`, puis les cartes posées d'`annexes` (preuves, règles, ressources) | `piles-joueur`, les piles d'`annexes` |

`terrain-soutien` est donc éclaté sur deux rangées, par type de carte :
`hero`, `alter-ego` et `ally` en rangée 3, tout le reste en rangée 4. Le
découpage vit dans une table pure (`rangees.ts`, réécrite), dont le test
vérifie qu'aucun des 12 emplacements n'est orphelin et qu'aucune carte de
`terrain-soutien` n'est perdue ni doublée.

**Main** : `MainEventail` repris tel quel, mêmes gestes (appui pour ouvrir,
appui court pour agrandir, appui maintenu sur la grande carte pour jouer),
avec des cartes de la même largeur que les cartes posées.

**Barre basse** : `BarreBas` reprise telle quelle, avec sa transformation
quand le moteur pose une question.

### 4.2 Taille des cartes

La largeur d'une carte vient de la **largeur** de l'écran, plus de la hauteur :

```
--pp-card-w : clamp(96px, (100vw - 16px marges - 3 x 8px écarts) / 4, 130px)
```

Soit 110 px sur 480 px de large, quatre cartes entières par rangée. La
hauteur d'une rangée découle de la carte : étiquette 14 px, carte
`--pp-card-w × 176 / 127`, jauge PV/menace 18 px qui déborde sous le cadre,
soit environ 185 px. Les quatre rangées font 740 px, la main 120, la barre
48 : 908 px, sous les 950 disponibles avec la barre du navigateur.

Sur un écran plus court (clavier ouvert, vieux téléphone), la colonne des
rangées (`.pp-rangees`) défile verticalement (`overflow-y: auto`). Aucune
carte n'est jamais rognée : c'est l'affirmation que le filet Playwright
mesure par rangée (§7.1).

La manigance principale reste en format paysage : même hauteur, largeur
`176 / 127` fois plus grande. `taille-carte.ts` est réécrit pour cette
formule (largeur de fenêtre en entrée), avec ses tests.

### 4.3 Défilement d'une rangée

Inchangé depuis la version 1, déjà livré : `scroll-snap` carte par carte,
voile « +N » au bord droit, cliquable, qui avance d'une largeur visible, piles
épinglées hors du défilement dans une colonne plafonnée à 30 % de la largeur.
Pendant un ciblage ou un paiement, ce qui n'est pas visable s'éteint et
chaque rangée se recale sur sa première cible (clé formée des ids des cartes
ciblables).

### 4.4 États et attachements

Inchangé, déjà livré : sonné, coriace et désorienté en pastilles lettrées au
coin de la carte (`etats.ts`) ; les améliorations glissées derrière le
porteur, décalées de 14 px vers la droite. ⚠ La bande visible d'une
amélioration glissée fait 14 px, sous le plancher tactile : la carte ouverte
(§4.6) montre désormais les attachées de son porteur, pour qu'un doigt puisse
les lire.

### 4.5 Deux héros

`terrain-soutien` porte les groupes des deux joueurs (`proprietaires`, voir
`joueurs.ts`). La rangée 3 montre un groupe par héros, séparés par un trait,
le héros actif en premier (`ordreDAffichage`), souligné ; la rangée 4 suit le
même ordre. La main affichée est celle du joueur actif ; les onglets de la
barre basse, rendus par la page dans `outils`, changent de joueur. Le badge
« Actif » suit `heroActifId`.

### 4.6 Ouvrir une carte, agir

Le tap sur une carte posée ouvre `CarteOuverte` : la carte en grand, son
texte lisible, ses attachées en vignettes dessous (nouveau), et le bouton
d'action quand le moteur en propose une. La carte ouverte et la pile regardée
s'inscrivent dans la pile de couches (`couches.ts`) : le Retour d'Android
ferme ce qui est ouvert, jamais la partie. C'est le geste le plus fréquent
du modèle, il ne peut pas rester hors de la pile.

### 4.7 Phase du méchant

Le cartouche du déroulé détaillé (`DeroulePhase`) se pose au-dessus de la
main, pleine largeur, au plus 45 % de la hauteur de l'écran, son texte
défilant dedans, ses boutons Précédent, Suivant et « la règle » en cibles de
48 px. Son ancrage suit la vraie hauteur de la barre (`--pp-barre-h` posée sur
`body` par un `ResizeObserver` sur la piste des rangées, déjà livré).

### 4.8 Plein écran et paysage

`plein-ecran.ts` (déjà livré) perd le verrouillage d'orientation : premier
`pointerdown`, `requestFullscreen()`, et rien d'autre. `EcranPortrait.tsx`
devient `EcranOrientation.tsx` et s'affiche quand `useOrientation()` rend
`paysage`, avec le texte « Tourne ton téléphone : le plateau se joue en
portrait. » Il ne démonte pas le plateau.

### 4.9 Ce qui disparaît, dans ce chantier

Supprimés au sous-projet 1, dans un commit dédié, sans attendre le terrain :
`PlateauMedaillons.tsx` et son test, `Medaillon.tsx`, `RangeeMedaillons.tsx`,
`TiroirPiles.tsx`, `ZoneFocus.tsx`, `bandes.ts`, `paiement-identite-mobile.test.tsx`
(remplacé par le test de paiement de `PlateauPortrait`), `PlateauPaysage.tsx`
et son test, `plateau-mobile.spec.ts`, le projet Playwright `s24-paysage`,
l'aiguillage `?medaillons` de `PlateauMobile.tsx`.

`medaillon.css` est **découpé** : les règles de la main, de la barre, du
bouton Payer et de la carte ouverte migrent dans la feuille du plateau
(`portrait.css`, renommage de `paysage.css`), le reste est supprimé.
`mobile.css` est réduit aux classes `.focus-*` de la pile regardée, ou
fusionné.

Conservés : `MainEventail`, `BarreBas`, `CarteOuverte`, `useAppuiLong`,
`couches.ts`, `joueurs.ts`, `useModeMobile`, `useOrientation`, `etats.ts`,
`hors-champ.ts`, `plein-ecran.ts`, `CartePosee`, `PilesEpinglees`,
`RangeeCartes`.

## 5. Les menus par-dessus le plateau

### 5.1 Le motif : la feuille basse

Sur le téléphone, tout panneau qui s'ouvre au-dessus de la table est une
**feuille basse** : elle monte depuis le bas de l'écran, pleine largeur, avec
une poignée, un titre et un bouton Fermer de 44 px ; le plateau reste
visible derrière, assombri. Une feuille « haute » monte jusqu'en haut quand
son contenu défile (sélecteur de cartes, historique).

Chaque feuille ouverte s'inscrit dans la pile de couches (`couches.ts`) : le
Retour d'Android ferme la feuille du sommet. `useCouchesBoard` est étendu
aux panneaux de la page (options, historique, sauvegardes, journal).

### 5.2 Déclinaison par menu

| Menu | Composant | Sur le téléphone |
|---|---|---|
| Actions d'une carte | `MenuActionsCarte` | Feuille basse : la carte en vignette à gauche (84 px), les actions en boutons pleine largeur de 48 px à droite, la raison d'un refus sous le bouton grisé. En ciblage (`mode-cibles`), la feuille se réduit à une bande « Choisis une cible · Annuler » et le plateau s'éteint sauf les cibles |
| Carte hors table | `SelecteurCibles` | Feuille haute : titre de l'action, cartes sur trois colonnes de 140 px, défilement vertical, tap pour choisir |
| Questions du moteur | `DemandeCentrale` | Feuille basse : texte, carte en cause en vignette, réponses en boutons de 48 px. La barre du bas continue de se transformer |
| Cibles depuis le menu | `ModaleCiblesMenu` | Feuille haute, même grille que le sélecteur |
| Cartes regardées | `ModaleCartesRegardees` | Feuille haute, grille de trois colonnes |
| Options | `PanneauOptions` | Feuille haute, sections empilées, réglages en lignes de 48 px |
| Historique, Journal du héros | `HistoriquePartie`, `JournalHeros` | Feuille haute, liste qui défile |
| Sauvegardes, Salon, Récompenses | `PanneauSalon`, `PanneauRecompenses` | Feuille haute |
| Fin de partie | `EcranFinPartie` | Plein écran vertical, boutons empilés de 48 px |
| Splash de tour, bandeau de phase | `SplashTour`, `BandeauPhase` | Inchangés, déjà pleine largeur |

### 5.3 Comment, sans toucher au PC

Le plateau portrait pose `mode-plateau-portrait` sur `body` (comme le paysage
posait `mode-plateau-paysage`). Une feuille `menus-mobile.css` ne s'applique
que sous cette classe : elle repositionne les panneaux existants en feuilles
(`position: fixed; left: 0; right: 0; bottom: 0`), redimensionne boutons et
grilles, cache ce qui n'a pas de sens au doigt (aperçu latéral au survol).
Le rendu PC ne voit rien.

Trois changements JS, pas plus :

1. `usePlacement` rend un placement « feuille » quand `body` porte la classe
   (pas de calcul de contournement des cartes) ;
2. `useCouchesBoard` reçoit les panneaux de la page ouverts (options,
   historique, sauvegardes, journal, cartes regardées) et les empile ;
3. `SelecteurCibles` et les deux modales reçoivent une prop `colonnes` ou une
   classe pour la grille de trois colonnes.

Les composants ne sont pas réécrits. Si l'un d'eux résiste au CSS (structure
DOM impossible à replier en feuille), il gagne une variante mobile de son
seul rendu, jamais de sa logique.

### 5.4 Cas limites

- **Deux feuilles à la fois** (une question du moteur pendant un menu
  d'actions) : la question passe devant, le menu attend derrière, comme sur
  PC où le menu se cache pendant un ciblage.
- **Clavier virtuel** (champ de texte dans un panneau) : la feuille haute
  défile, le champ reste visible.
- **Feuille plus haute que l'écran** : jamais, son contenu défile et sa
  hauteur est plafonnée à 92 % de l'écran.

## 6. L'assistant

### 6.1 La feuille mobile

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

### 6.2 Les deux changements dans `app.js`

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

### 6.3 Bouts du parcours

- **Retour au menu depuis le plateau** : le bouton existe dans les options ;
  il reste à 44 px et sort du plein écran (`document.exitFullscreen()`)
  avant de naviguer.
- **Fin de partie** : voir §5.2.

## 7. Preuves

### 7.1 Automatiques

- **vitest** (`ui-app`) : `rangees.ts` réécrit (12 emplacements, éclatement
  de `terrain-soutien` par type sans perte ni doublon), `taille-carte.ts`
  réécrit (largeur de fenêtre en entrée), `PlateauPortrait.test.tsx` (quatre
  rangées, piles épinglées, deux héros, paiement par une identité posée,
  écran paysage monté en paysage, carte ouverte et pile regardée dans la
  pile de couches), `couches` étendu aux panneaux.
- **Playwright** (`ui-check`) : le projet `s24` (480 x 1050, `hasTouch`,
  `isMobile`) joue les 34 états enregistrés avec les affirmations du
  paysage transposées : aucun débordement par `.rangee-cartes-defilement`,
  chaque carte posée d'au moins 96 px de large, chaque `[data-tactile]` d'au
  moins 44 px, voile « +N » mesuré, aucune erreur console. Un second test
  en 1050 x 480 vérifie sur trois états que l'écran « Tourne ton téléphone »
  couvre la fenêtre. Un troisième volet, `menus-mobile.spec.ts`, ouvre sur un
  état enregistré le menu d'actions d'une carte, une question du moteur et
  le sélecteur, et mesure que chaque bouton fait 44 px et que la feuille
  tient dans l'écran.
- **Captures** : l'assistant est capturé sur le gabarit `mobile` (390 x 844)
  par `npm run captures`. Les références sont refaites une fois le design
  validé à l'écran, avec `captures:valider`.

### 7.2 Terrain

Le critère de fin du chantier : une partie solo complète, un héros puis deux
héros, depuis le S24 Ultra sur narwhalchampions.com, de l'accueil de
l'assistant au bilan de fin de partie, sans toucher un PC.

## 8. Livraison

Deux étapes, à ne pas confondre (leçon du 07/09) :

1. `bash ui-app/deployer.sh` construit le bundle et le dépose dans
   `Fusion/marvel-lcg-src` (installation locale, port 2345 et tunnel) ;
2. `deploiement/deployer.ps1 -Code` (PowerShell, lançable depuis WSL) envoie
   ce dossier sur le serveur public et **redémarre le service**, ce qui coupe
   les parties en cours. Chaque sous-projet se termine par cette étape, pour
   que l'utilisateur voie le résultat sur son téléphone.

Aucun fichier du moteur Python touché.

## 9. Découpage en sous-projets

Chacun reçoit son plan d'implémentation, dans cet ordre, et se termine par
un déploiement public :

1. **Plateau portrait** : §4 en entier, suppression des médaillons et du
   paysage, découpe de `medaillon.css`, filet Playwright portrait (§7.1
   deux premiers points).
2. **Menus mobiles** : §5, filet `menus-mobile.spec.ts`.
3. **Assistant au doigt** : §6, captures.
4. **Terrain et bouts du parcours** : §6.3, §7.2, retours consignés.
