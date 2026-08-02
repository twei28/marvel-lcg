# Plateau jouable au doigt sur téléphone

**Date :** 2026-08-02
**Statut :** conçu, validé, non planifié
**Rapport à la roadmap :** couvre MOB-01, MOB-02, MOB-03 et le critère 5 de la phase 6 (dézoom sémantique). Ne couvre pas BOARD-11 ni BOARD-12.

---

## 1. Le problème

Le plateau actuel (`ui-app/src/board/Board.tsx`) reprend le modèle historique du jeu : une table de taille fixe, 1920x940 pixels de scène, mise à l'échelle de la fenêtre par `min(largeur/1920, hauteur/940)`. Rien ne défile, on voit tout.

Ce modèle s'effondre sur un téléphone. Sur la cible retenue, un Samsung S24 Ultra dans Chrome (environ 480x1050 pixels CSS en portrait) :

| Orientation | Échelle | Largeur d'une carte |
|---|---|---|
| Portrait 480x1050 | 0,25 | 32 px |
| Paysage 1050x480 | 0,51 | 65 px |

Aucune media query ne corrige cela : à l'intérieur de la scène, les tailles sont des constantes en pixels de scène, et `board.css` neutralise volontairement les media queries de `ScanCard.css` pour ne pas déformer la table. C'est un changement de modèle de layout, pas un ajustement CSS. La roadmap l'avait identifié comme le piège central de la phase 6.

## 2. Périmètre

**Dans le périmètre :** le plateau de jeu uniquement.

**Hors périmètre, projet distinct :** la refonte de l'écran de préparation en React pensé mobile. C'est la phase 4 de la roadmap, avec sa recherche préalable (contrat `/new?data=`, campaign logs des 4 formats). Elle fera l'objet de sa propre spec et de son propre plan. En attendant, une partie se lance depuis un PC et se joue depuis le téléphone.

**Hors périmètre, inchangé :** le mode PC. Aucune ligne de la scène à l'échelle n'est modifiée. C'est la garantie de non-régression principale.

## 3. Cadrage retenu

| Sujet | Décision |
|---|---|
| Appareil de référence | Samsung S24 Ultra, Chrome, environ 480x1050 px CSS en portrait |
| Orientation | Portrait d'abord. Le paysage fonctionne et affiche simplement plus de tuiles par rangée, il n'est pas conçu séparément |
| Modes de jeu couverts | Solo un héros, solo multi-héros, multijoueur un appareil par joueur, multijoueur PC hôte et invités au téléphone |
| Niveau de lecture d'une carte posée | Nom, coût, stats et statuts sans toucher la carte. Texte de règles et scan complet au tap |
| Geste d'inspection | Le tap ouvre le menu d'actions, qui montre la carte en grand avec son texte. Pas d'appui long |
| Modèle de layout | Vue d'état condensée qui tient toujours à l'écran, plus une couche de focus par zone |

### Pourquoi ce modèle et pas une colonne défilante

Une première proposition empilait les zones dans une colonne défilante. Elle a été écartée après examen de ce que fait le genre.

Les jeux à plateau borné (Hearthstone, Marvel Snap, Legends of Runeterra) ne défilent jamais : leur plateau a un plafond, tout tient à l'écran. Les jeux à tableau non borné, qui sont le vrai comparable de Marvel Champions, condensent sémantiquement (regroupement, empilement, compteurs à la place des objets), donnent des panneaux ou des onglets pour entrer dans une zone, et gardent le déplacement libre du plateau en dernier recours seulement.

Aucun ne fait du défilement son mode de lecture principal, et la raison est une raison de jeu : pour décider d'une action il faut voir l'état complet. Un état qu'on doit faire défiler pour le reconstituer de mémoire fait prendre de mauvaises décisions.

## 4. Architecture

Le mode mobile est un **rendu alternatif des mêmes objets**, pas une seconde application.

```
  /get_world  ──►  world.ts  ──►  zones.ts  ──►  EmplacementAffiche[]
                                                        │
                        ┌───────────────────────────────┴──────────────┐
                        ▼                                              ▼
              Board.tsx (scène à l'échelle)            PlateauMobile.tsx (vue d'état)
              INCHANGÉ                                  NOUVEAU
                        │                                              │
                        └──────────► ScanCard, interaction.ts ◄────────┘
                                     PARTAGÉS
```

Ce qui est réutilisé sans modification : `zones.ts` (découpage en emplacements), `card-model.ts`, `interaction.ts` (le tap existe déjà, il n'y a aucun glisser-déposer dans le plateau), `world.ts` et son `isVisibleFor`, `SelecteurCibles`, `MenuActionsCarte`, `HistoriquePartie`.

Ce qui est nouveau :

- `PlateauMobile.tsx` : le niveau 1, la vue d'état.
- `TuileCondensee.tsx` : une entité réduite à sa vignette, son nom court et ses compteurs.
- `ZoneFocus.tsx` : le niveau 2, une zone ouverte en feuille par-dessus.
- `mobile.css` : les styles des deux niveaux.
- `useModeMobile.ts` : la bascule.

## 5. Les deux niveaux

### Niveau 1, la vue d'état

Elle tient toujours à l'écran, en entier, sans jamais défiler. Ce n'est pas le plateau en petit : c'est l'état de la partie en objets condensés. Une amélioration attachée à un héros n'est pas une carte, c'est une pastille sous sa tuile. Une pile est un chiffre.

```
┌────────────────────────────┐
│ T3 · Phase joueur    ⚙ ↺ ≡ │  52 px
├────────────────────────────┤
│ VILAIN                     │
│ ┌────┐ Rhino  II           │
│ │art │ ♥12/22  ⚔3 ▣2       │ 140 px
│ └────┘ sbires: [Ga][Ga]    │
├────────────────────────────┤
│ COMPLOTS                   │
│ Breakin' & Takin'  ▲4/12   │ 110 px
│ [Secondaire 2/6][Sec. 0/4] │
├────────────────────────────┤
│ RENCONTRE   deck 24 · déf 7│  64 px
├────────────────────────────┤
│ SPIDER-MAN (toi)    ♥8/10  │
│ ⚡3 · alliés [Th♥3][Ms♥2]  │ 200 px
│ améliorations ●●● soutiens●│
│ ── autres joueurs ──       │
│ Capitaine ♥9/12 ⚡2     ▸  │  44 px
├────────────────────────────┤
│ ▲ MAIN 6   [][][][][][]    │  76 px
└────────────────────────────┘
```

Les bandes correspondent aux `CleEmplacement` existants de `zones.ts`. Les hauteurs indiquées sont des valeurs de repos : elles se contractent selon la règle de condensation ci-dessous.

### Niveau 2, la zone en focus

Un tap sur une bande l'ouvre en feuille par-dessus le niveau 1. Les cartes y font 149 px de large (206 px de haut), soit trois par rangée à 480 px : nom, coût et stats sont lisibles sans zoom, et chaque carte dépasse largement les 44 px de cible tactile. Les zones denses passent à quatre par rangée, en 110 px.

Un tap sur une tuile précise du niveau 1 court-circuite le focus et ouvre directement `MenuActionsCarte` pour cette carte, avec la carte en grand dedans.

### La règle de condensation

**Le niveau 1 ne défile jamais, il condense davantage.** C'est ce qui remplace le zoom optique, et c'est la règle qui rend le modèle tenable quand la partie s'étale. Par ordre d'application :

1. Les tuiles d'une bande rétrécissent jusqu'à leur taille plancher (64 px de haut).
2. Au-delà, elles se groupent : cinq alliés deviennent deux tuiles et un « +3 » touchable qui ouvre la zone en focus.
3. Un seul joueur est déplié à la fois. Les autres sont des bandeaux de 44 px.

Une bande qui n'a rien à montrer n'est pas dessinée, comme aujourd'hui dans `zones.ts`.

### Le ciblage court-circuite les deux niveaux

Quand le moteur demande une cible, on n'envoie pas le joueur la chercher dans les bandes. Le `SelecteurCibles` existant s'ouvre avec les cibles valides, d'où qu'elles viennent sur la table, et le niveau 1 se contente de marquer d'un compteur les bandes concernées. La barre d'action reste visible tant que le moteur attend une réponse : elle ne se replie jamais.

## 6. Gestes

Un seul geste principal, le tap.

| Geste | Effet |
|---|---|
| Tap sur une bande | Ouvre la zone en focus |
| Tap sur une tuile | Ouvre le menu d'actions de cette carte, carte en grand dedans |
| Tap ou glissement sur la poignée du tiroir | Déplie ou replie la main |
| Glissement vers le bas sur une feuille | La ferme |
| Retour Android | Ferme la feuille du dessus, une couche à la fois |

Aucun appui long, aucun glisser-déposer, aucun survol requis. Les quatre usages restants de `onMouseEnter` (`MenuActionsCarte.tsx:594` et `:674`, `SelecteurCibles.tsx:39`, `DemandeCentrale.tsx:189`) reçoivent leur équivalent au tap.

Contraintes tactiles : toute cible fait au moins 44x44 px, une tuile condensée au moins 64 px de haut, le tiroir de main a une poignée de 32 px. Les `env(safe-area-inset-*)` protègent le tiroir et la barre d'action de la barre gestuelle Android.

Deux non-décisions assumées : pas de double tap, il entre en conflit avec le zoom du navigateur ; et le zoom du navigateur n'est jamais désactivé, même si le plateau n'en a plus besoin.

Les couches empilées (focus, menu d'actions, sélecteur) sont gérées par `history.pushState`, une entrée par couche, pour que le retour d'Android ferme la bonne.

## 7. Plusieurs joueurs

Un seul joueur est déplié à la fois : par défaut celui dont c'est le tour, sinon celui qu'on a touché. Les autres sont des bandeaux de 44 px portant points de vie, ressources, taille de main et statuts, dépliables au tap.

En solo multi-héros, le passage de tour déplie automatiquement le héros actif. En multijoueur réseau, rien ne change côté information cachée : `isVisibleFor` filtre déjà ce que chaque siège a le droit de voir, et le rendu mobile consomme le même descripteur filtré.

## 8. La bascule

`useModeMobile.ts` évalue `(max-width: 900px) or (pointer: coarse)` en JavaScript, via `matchMedia`, et non en CSS : le choix du composant de rendu est une décision React, pas une question de feuille de style.

Un réglage à trois états dans le panneau ⚙ (auto, mobile forcé, PC forcé) permet de tester le mode mobile depuis un PC et de repasser en mode PC sur une tablette. Il est mémorisé dans `localStorage`, sur le modèle de la clé `ui` de la bascule `?ui=old`.

## 9. Filet et vérification

Le filet existant s'étend, il n'est pas remplacé :

- Un gabarit S24 Ultra dans `ui-check` : 480x1050, `deviceScaleFactor: 3`, `hasTouch: true`, `pointer: coarse`.
- Les 34 fixtures `get_world` de `public/js/fixtures/` rejouées dans le rendu mobile, chacune vérifiée sans débordement du niveau 1.
- Les références PC existantes restent vertes : le mode PC n'est pas modifié.

Les fixtures ne couvrent pas `zone-victoire`, `deck-rencontre-vide` ni `stade-3` (les cinq parties d'origine se sont soldées par une défaite). Si le plateau mobile a besoin de ces cas, ils sont à capturer avec `~/marvel-work/tools/run_dump.sh` avant la vérification finale.

## 10. Definition of done

1. Une partie solo complète se joue depuis le téléphone, sans jamais zoomer ni faire défiler le niveau 1.
2. Les 34 fixtures se rendent en mode mobile sans débordement du niveau 1.
3. Toute cible tactile mesure au moins 44 px, vérifié automatiquement sur les fixtures.
4. L'autoplay reste à zéro traceback.
5. `?ui=old` fonctionne toujours et les références PC restent vertes.
6. Le lancement de la partie se fait depuis un PC : la préparation est le projet suivant.

## 11. Pièges connus de ce codebase à respecter

Repris de `.planning/STATE.md`, ils s'appliquent à ce chantier :

- Tout passage vers le jeu se fait par `bash ui-app/deployer.sh`, jamais par une recopie de `dist/` à la main.
- Le routage du serveur est une liste blanche stricte par extension : le build ne peut produire que `.html`, `.js` et `.css`. Tout asset importé est inliné (`assetsInlineLimit: () => true`).
- `Fusion/marvel-lcg-src` est un codebase de distribution périmé, servi par `JOUER-EN-MULTI.bat` avec une partie possiblement en cours. Le codebase de travail est `~/marvel-work/fusion/marvel-lcg-src`. Ne jamais écrire dans `Fusion/`.
- Node est le binaire Windows : il ne lit pas les chemins WSL, et npm exécute ses scripts via `cmd.exe` (un script npm doit rester une commande unique).
- Le runtime `public/js/marvel/` n'est ni lu ni modifié. Le nouveau code est une fonction pure de `get_world`.

## 12. Ce que ce projet ne fait pas

- Il ne refait pas l'écran de préparation. Projet distinct.
- Il ne conçoit pas de disposition paysage dédiée. Le paysage fonctionne par reflux, il n'est pas optimisé.
- Il ne touche pas au mode PC.
- Il n'ajoute pas de manifeste PWA ni d'installation sur l'écran d'accueil.
- Il ne traite pas la galerie de cartes, le deck builder ni le replay, différés en v1.x.
