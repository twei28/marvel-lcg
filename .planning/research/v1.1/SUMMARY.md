# Project Research Summary

**Project:** Marvel Champions LCG (projet custom)
**Domain:** jeu de cartes coopératif en navigateur, plateau React (PC) rendu tactile sur tablette, téléphone (plateau et menus) repensé
**Researched:** 13/10/2026
**Confidence:** MOYENNE à HAUTE sur les mécanismes de plateforme et les points d'intégration (lus dans le code et dans les données de compatibilité officielles) ; MOYENNE sur les comportements fins d'un vrai iPad et d'un vrai iPhone, non vérifiables sans l'appareil ; MOYENNE sur le panorama concurrentiel (plusieurs revues, pas de capture ouverte directement)

## Executive Summary

Ce jalon n'ajoute aucune dépendance : tout ce qu'il faut existe déjà dans la plateforme web (Pointer Events, `scroll-snap`, `dvh`, `env()`, container queries) ou a déjà été écrit à la main dans le dépôt (appui long, glisser, feuille basse, Wake Lock, vibrations, installation). Le travail consiste à brancher un **détecteur du dernier geste** (doigt contre souris, séparé de la disposition par largeur qui existe déjà), à corriger des trous de plateforme bien identifiés, et à décider une fois pour toutes l'orientation de la partie sur téléphone. Les quatre recherches convergent sur un même diagnostic : la tablette n'est pas une troisième mise en page, c'est le plateau PC existant avec un axe de saisie en plus ; et le défaut qui bloque tout ("un toucher ouvre l'aperçu et il ne se referme plus") a une cause unique, précisément localisée dans le code.

L'approche recommandée tient en quatre mouvements : d'abord un détecteur de saisie partagé (`data-saisie` sur `<html>`) et un projet Playwright tactile/WebKit, avant toute autre modification ; ensuite la tablette (aperçu refermable, cibles 44 px, infobulles) qui profite gratuitement au téléphone couché ; puis la décision d'orientation du téléphone, appuyée sur des mesures et non sur l'intuition ; enfin la refonte du plateau et des menus téléphone dans la structure que cette décision dicte. Le risque principal n'est pas technique mais de méthode : refaire une troisième disposition, mélanger saisie et disposition dans le même axe, ou toucher `viewport-fit=cover` sans l'audit complet des marges qui va avec, feraient regagner exactement les défauts que la refonte d'octobre vient de corriger.

Les risques à mitiger, par ordre de gravité : le survol souris qui se déclenche au toucher (iOS rejoue des événements souris après un doigt) ; les impossibilités définitives sur iPhone (pas de vibration, pas de verrou d'orientation, pas de plein écran) qui obligent à concevoir pour les deux orientations et à masquer les réglages sans effet plutôt qu'à les afficher ; et l'absence de tout filet de test tactile aujourd'hui (le gabarit tablette de Playwright tourne sans `hasTouch`). Trois points restent à trancher par l'utilisateur avant de coder, détaillés plus bas : l'orientation du téléphone, menu burger contre barre basse, et le sort de quelques cas limites (iPad mini portrait, Split View, téléphone couché 667×375).

## Key Findings

### Recommended Stack

Aucune nouvelle dépendance. Les quatre recherches recommandent unanimement de rester sur les briques maison existantes (Pointer Events, hooks `useAppuiLong`/`useGlisser`, `scroll-snap` CSS) plutôt que d'introduire une bibliothèque de gestes : `@use-gesture/react` n'a pas été publiée depuis mars 2024, `vaul` est déclaré non maintenu par son auteur, et `@base-ui/react` (Drawer) ne vaudrait le coup que si les pages de menus migraient en React — ce qui n'est pas prévu pour ce jalon.

**Core technologies :**
- `PointerEvent.pointerType` — source de vérité unique pour distinguer doigt et souris ; les media queries `(hover)`/`(pointer)` sont piégées sur iPad avec trackpad.
- CSS `scroll-snap-type`/`scroll-snap-stop` — glissement latéral (carte agrandie, livre de campagne) sans JS, inertie native.
- `env(safe-area-inset-*)` + `viewport-fit=cover` — zones sûres, actuellement inertes sur le plateau car la balise viewport manque.
- Playwright, projet WebKit + `hasTouch` à créer — seul filet capable d'attraper les écarts Pointer Events/CSS WebKit avant un vrai iPad.
- `navigator.wakeLock`, déjà branché — à garder tel quel, sans NoSleep.js ni vidéo en boucle.

### Expected Features

**Must have (déjà largement fait, à consolider) :**
- Lire une carte sans la jouer partout, agrandissement entier quelle que soit l'orientation, feuilleter la main en glissant, voir l'autre face — fait depuis la refonte d'octobre et les correctifs Raven.
- Aucune carte superposée captant le doigt d'une autre ("une ligne par famille") — fait, à garantir par un test de non-chevauchement des boîtes tactiles.
- Jouer = toucher puis bouton ou glisser, jamais un seul toucher (séparer lire et agir, piège n°1 de tous les concurrents portés) — fait côté téléphone, à vérifier sur tablette.
- Annuler 5 s — déjà au-dessus de l'état de l'art concurrent.
- Tablette : aperçu sans survol fermable, détection du dernier geste, cibles 44 px, `touch-action: manipulation`.

**Should have (différenciateurs) :**
- Paysage téléphone dérivé des mêmes bandes (deux colonnes) à la place du plateau PC réduit — supprime la source des deux derniers retours de Raven.
- Indicateurs de hors-champ (pastille sur une bande/onglet quand une cible ou une question s'y trouve) — personne ne le fait bien chez les concurrents.
- Vue d'ensemble compacte des héros en coop à 3-4 joueurs.
- Mots-clés expliqués dans l'agrandissement.

**Defer (v1.x / v2+) :**
- Barre basse de navigation (si l'arbitrage burger/barre la retient).
- Glisser vers une zone de dépôt pour les actions fréquentes.
- Mode outil au doigt (branche `mode-manuel`, T3).

### Architecture Approach

Le constat central, partagé par STACK, ARCHITECTURE et PITFALLS : il n'existe aujourd'hui aucune notion de "mode de saisie" partagée — une demi-douzaine de détections locales et incohérentes (`(pointer: coarse)` à trois endroits différents, `pointerType` lu au cas par cas). La recommandation est de créer deux axes strictement indépendants : la **disposition** (largeur, déjà centralisée dans `useModeMobile.ts`, inchangée) et la **saisie** (doigt/souris, nouveau, posé une fois sur `<html>` par un script de tête `saisie.js` partagé entre le plateau React et les pages JS non compilées). La tablette devient alors "`Board` + `data-saisie=doigt`", jamais une troisième mise en page.

**Composants majeurs :**
1. `saisie.js` (nouveau, `public/js/`) — seul propriétaire de `data-saisie`, lu par le CSS et par `useSaisie()` côté React.
2. `Board.tsx` (modifié) — garde sur `survol`, aperçu posé et refermé au doigt, croix 44 px.
3. `CoucheInfobulles` (nouveau) — un seul écouteur délégué pour l'appui long, plutôt que d'envelopper 55 sites `title`.
4. État au-dessus de l'aiguillage (`RenduPartie`) — ce qui doit survivre à une rotation (question en cours) remonte plus haut dans `board.tsx`.

### Critical Pitfalls

1. **Le survol souris se déclenche au toucher, l'aperçu reste collé** — `Board.tsx` ouvre l'aperçu sur `onMouseOver` (lignes 1423/1620) ; Safari iOS rejoue des événements souris de compatibilité après un toucher, sans jamais envoyer le `mouseleave` qui fermerait. Cause exacte du bug "un toucher ouvre aperçu + menu et l'aperçu ne se ferme plus" constatée sur iPad. Correction : `onPointerOver` filtré sur `pointerType === 'mouse'`.
2. **Fermer une couche au `pointerdown` fait traverser le toucher jusqu'à la carte du dessous** — fermer sur `click`, jamais sur `pointerdown`, sous peine de clic fantôme sur une carte jouable.
3. **La rotation laisse des mesures périmées** — au moins sept composants écoutent chacun `window.resize` ; iOS fournit des dimensions fausses pendant la rotation. Cause probable (hypothèse, confiance MOYENNE) du retour Raven "Fin du tour posée sur la main après plusieurs rotations". Il faut une source de géométrie unique, pas sept écouteurs indépendants.
4. **`viewport-fit=cover` absent du plateau** — sans lui, tous les `env(safe-area-inset-*)` déjà posés 11 fois dans le CSS sont inertes ; l'ajouter sans audit complet des marges fait passer des boutons sous l'encoche en paysage.
5. **Trois impossibilités iOS à assumer, pas à contourner** — pas de vibration, pas de verrou d'orientation, pas de plein écran sur iPhone. Afficher un réglage qui ne fait rien sur l'appareil réel des joueurs (Raven est sur iPhone) est le retour n°5 déjà constaté : il faut masquer, pas promettre.

## Convergences entre les quatre recherches

Les quatre fiches, écrites indépendamment, tombent sur les mêmes conclusions — un signal de confiance fort :

- **Cause unique et précisément localisée du bug d'aperçu iPad** : les quatre fiches citent `Board.tsx` lignes 1423 et 1620, `onMouseOver`, et le même mécanisme (événements souris de compatibilité après un toucher, aggravé par l'heuristique WebKit de "changement de contenu" qui peut en plus avaler le clic suivant). Correction identique recommandée partout : `onPointerOver` filtré sur `pointerType`.
- **`data-saisie` sur `<html>`** : STACK et ARCHITECTURE proposent indépendamment le même mécanisme (attribut unique, propriétaire unique `saisie.js`, lu par CSS et React), avec le même argument : une media query seule ne peut pas trancher sur iPad avec trackpad.
- **`viewport-fit=cover` manquant** : STACK et PITFALLS identifient toutes les deux l'absence de cette directive dans `ui-app/board.html` comme la raison pour laquelle les `env(safe-area-inset-*)` déjà écrits ne servent à rien, et toutes les deux préviennent qu'il faut l'ajouter avec un audit des marges, pas seul.
- **Un projet Playwright tactile/WebKit à créer avant toute modification** : les quatre fiches constatent que `playwright.config.ts` ne simule aucune tablette tactile (`hasTouch` absent du gabarit `tablette`) et placent la création de ce filet en tête de l'ordre de construction, avant le premier changement de `Board.tsx`.
- **La tablette n'est pas une troisième disposition** : FEATURES, ARCHITECTURE et PITFALLS le disent dans les mêmes termes, en citant la même décision du 12/10.

## Contradictions et tensions à arbitrer

Ces points ne se résolvent pas par plus de recherche : ils demandent une décision de l'utilisateur.

1. **Orientation du téléphone.** FEATURES recommande explicitement "portrait d'abord, paysage dérivé des mêmes bandes en deux colonnes" (avec des mesures de confirmation détaillées : densité, nombre de touchers par tour, part réelle des parties jouées couché). ARCHITECTURE, plus prudente, décrit l'option "les deux" comme "la plus probable vu l'existant" mais propose de **garder exactement les deux rendus actuels** (debout = `PlateauPortrait`, couché = `Board` tactile), sans trancher elle-même si le paysage doit devenir des bandes à deux colonnes ou rester le plateau PC réduit. Les deux fiches s'accordent sur le fait qu'un verrou portrait dur est impossible sur iPhone et donc que le paysage doit rester jouable quoi qu'il arrive — mais pas sur la mise en page à lui donner. **À trancher avant de toucher au plateau téléphone** (c'est explicitement l'étape 4 de l'ordre de construction recommandé).
2. **Menu burger contre barre basse.** FEATURES signale que la décision du 09/10 (en-tête burger) est remise en question par les études d'ergonomie mobile (NN/g : la navigation cachée réduit la découverte ; Material 3 : 3-5 destinations = barre basse), mais précise elle-même que cet argument n'est appuyé que par des études génériques, pas par l'observation d'un jeu de cartes comparable. Priorité P2 "à arbitrer" dans la matrice.
3. **Réglages impossibles sur iPhone.** Toutes les fiches constatent que vibration, verrou d'orientation et plein écran n'existeront jamais sur iPhone par API. Ce n'est pas une contradiction entre les recherches, mais une tension produit à trancher : masquer purement et simplement ces réglages sur iPhone (recommandation unanime) versus les garder affichés "pour cohérence visuelle avec Android" — à ne pas faire, selon les quatre fiches, mais à confirmer explicitement puisque c'est un changement visible de l'interface des réglages.
4. **Cas limites non tranchés** : l'iPad mini en portrait (744 px de large, tombe sous le seuil de 768 px et reçoit aujourd'hui le plateau téléphone — voulu ou pas, aucune fiche ne le dit), le Split View/Slide Over iPad (fenêtre de 320 à 700 px), et le téléphone couché à 667×375 (garde-t-il les bandes ou bascule-t-il au plateau PC réduit à l'échelle minimale). ARCHITECTURE propose une solution technique immédiate pour ce dernier cas (ajouter `and (orientation: portrait)` au média query de disposition) mais la qualifie elle-même de "changement d'une ligne au comportement large, à décider avec captures".

## Implications for Roadmap

Numérotation à la suite de la roadmap existante (dernière phase livrée : Phase 7).

### Phase 8 : Fondations tactiles (saisie + filet de test)
**Rationale :** toutes les recherches placent ce lot en préalable bloquant ; sans détecteur de saisie partagé ni projet Playwright tactile, aucune autre phase ne peut être vérifiée.
**Delivers :** `saisie.js` + `saisie.ts` (détecteur du dernier geste, réglage auto/toujours/jamais), projet Playwright `tablette-doigt` (`hasTouch`, `isMobile`), tests Vitest de la fonction pure de décision.
**Uses :** Pointer Events, `useSyncExternalStore` (React 19, natif).
**Avoids :** piège n°4 (iPad mal classé, se déclare Mac), piège n°5 (bascule qui fait sauter la mise en page sous le doigt), piège "tester sans `hasTouch`".

### Phase 9 : Tablette T1 — aperçu refermable
**Rationale :** c'est le seul point strictement bloquant pour l'usage tactile du plateau PC ; corrige la cause unique du bug constaté par Raven.
**Delivers :** `onPointerOver` filtré sur `Board.tsx` (lignes 1423/1620), aperçu posé au toucher avec le menu, fermeture au toucher ailleurs (sur `click`, pas `pointerdown`) et par une croix, `touch-action: manipulation`, `-webkit-touch-callout: none`.
**Addresses :** feature table-stakes C "Aucun survol nécessaire" et "Aperçu et menu ensemble au premier toucher".
**Avoids :** pièges 1, 2, 9, 10 (survol collant, fermeture traversante, double déclenchement, zoom au double toucher).

### Phase 10 : Tablette T2 — 44 px et infobulles
**Rationale :** dépend de T1 (la détection et l'aperçu doivent être posés) ; complète le mode tablette sans toucher à l'orientation.
**Delivers :** barre du haut et compteurs à 44 px (compensés de l'échelle de scène), `CoucheInfobulles` (appui long délégué), raison "injouable" affichée explicitement au toucher.
**Addresses :** feature table-stakes C restante.
**Avoids :** piège 6 (44 px dans une scène réduite par `transform: scale`), piège 8 (appui long qui réveille le système iOS), piège 12 (régressions PC via le code tactile partagé — à vérifier par comparaison au pixel à chaque lot).

### Phase 11 : Décision d'orientation du téléphone
**Rationale :** toutes les fiches l'exigent avant de toucher au plateau téléphone ; c'est une décision produit appuyée sur des mesures, pas un développement.
**Delivers :** mesures Playwright (cartes visibles par orientation, touchers par tour type, défilements par tour), éventuellement un compteur anonyme d'orientation réelle en partie, décision écrite dans PROJECT.md (portrait seul / paysage dérivé des bandes / plateau PC réduit couché), sort tranché pour l'iPad mini portrait, Split View et le cas 667×375.
**Uses :** le filet Playwright de la Phase 8.
**Avoids :** piège 15 (deux orientations doublent la surface de défauts si la décision n'est pas explicite sur ce que devient l'orientation secondaire).

### Phase 12 : Refonte téléphone — menus
**Rationale :** indépendante du plateau (fichiers disjoints), peut avancer en parallèle des phases 9-10 une fois la Phase 8 posée (balise `saisie.js`).
**Delivers :** salon invité au format assistant (seule page de menus non faite), clavier qui ne cache pas le bouton d'envoi, arbitrage burger/barre basse tranché et appliqué.
**Addresses :** feature table-stakes B, arbitrage noté dans les contradictions ci-dessus.
**Avoids :** piège 13 (clavier virtuel qui cache le bouton), piège 14 (réglages sans effet affichés).

### Phase 13 : Refonte téléphone — plateau
**Rationale :** dépend de la décision de la Phase 11 ; c'est elle qui dicte la structure (deux colonnes dérivées des bandes, ou plateau PC réduit conservé).
**Delivers :** `PlateauPortrait`/paysage mis en cohérence avec la décision, indicateurs de hors-champ (cibles, questions), zone réservée du bouton d'action par orientation, test de rotation répétée (6 rotations, aucun élément fixe sur la main), `viewport-fit=cover` + audit complet des marges.
**Addresses :** différenciateurs FEATURES (paysage dérivé des bandes, indicateurs hors-champ).
**Avoids :** piège 3 (rotation et mesures périmées — source de géométrie unique à construire), piège 7 (hauteur Safari et zones sûres), piège 11 (défilement élastique).

### Phase Ordering Rationale

- L'ordre reproduit celui proposé par ARCHITECTURE, qui est le seul document des quatre à raisonner explicitement en dépendances de fichiers et d'état : fondations (8) avant tout changement visible, tablette T1 (9) avant T2 (10) parce que T2 réutilise l'aperçu posé par T1, orientation (11) avant plateau téléphone (13) parce qu'elle fixe la structure de ce qui sera codé.
- Les menus (12) sont volontairement détachés du plateau téléphone (13) : les quatre recherches constatent qu'ils touchent des fichiers disjoints (pages JS non compilées contre `ui-app/src/board/`), seule la balise `<script src="saisie.js">` les relie.
- Une contrainte externe non négociable, signalée par ARCHITECTURE et reprise ici : vérifier que la refonte de la phase du méchant (mêmes fichiers `Board.tsx`/`board.css`) est bien close avant d'entamer la Phase 9, et vérifier `git stash list` (deux sessions ont déjà travaillé sur le même arbre).

### Research Flags

Needs research pendant la planification détaillée :
- **Phase 11 (orientation) :** les contradictions entre FEATURES et ARCHITECTURE ne sont pas résolues par la recherche ; prévoir une mesure réelle (Playwright + éventuellement compteur anonyme) avant d'écrire le plan.
- **Phase 13 (plateau téléphone) :** dépend directement de l'issue de la Phase 11 ; si le verdict est "paysage dérivé des bandes", le détail de la mise en page à deux colonnes n'a pas été maquetté et mériterait une recherche courte sur place.
- **Phase 12, arbitrage burger/barre basse :** appuyé sur des études génériques (NN/g, Material 3), pas sur un jeu de cartes comparable ; si l'arbitrage est serré, un test utilisateur léger vaudrait mieux qu'une recherche supplémentaire.

Phases avec patterns bien documentés (recherche-phase non nécessaire) :
- **Phase 8 et 9 :** le point d'intégration est lu dans le code à la ligne près (`Board.tsx` 1423/1620) et la correction (Pointer Events filtrés) est un pattern web standard, documenté par MDN et confirmé par les quatre recherches.
- **Phase 10 :** HIG Apple (44 px) et `touch-action` sont des patterns stables, sans ambiguïté relevée.

## Confidence Assessment

| Area | Confidence | Notes |
|------|------------|-------|
| Stack | HAUTE | support navigateur appuyé sur MDN browser-compat-data (08/10/2026), caniuse, blogs WebKit officiels ; MOYENNE sur les comportements fins sur appareil réel (iPad+trackpad, haptique iOS) |
| Features | MOYENNE | bonne sur les contraintes navigateur (HAUTE, données officielles) et sur Marvel Snap (déclaration publique de Ben Brode) ; BASSE sur Gwent et Sentinels (revues inaccessibles, 403) ; aucune capture de concurrent ouverte directement cette session |
| Architecture | HAUTE | points d'intégration tous lus dans le code existant ; MOYENNE pour la détection iPad+trackpad (une source WebKit/GitHub) ; BASSE pour tout ce qui touche un vrai iPad, jamais essayé |
| Pitfalls | MOYENNE | mécanismes WebKit bien documentés (Apple, blogs WebKit officiels) ; plusieurs causes rattachées au code (rotation, piège 3) restent des hypothèses non reproduites en émulation |

**Overall confidence:** MOYENNE. Les mécanismes de plateforme et les points d'intégration dans le code sont solides (HAUTE) ; ce qui manque structurellement à toutes les fiches, et qu'aucune quantité de recherche supplémentaire ne peut combler, est la vérification sur un vrai iPad et un vrai iPhone — explicitement reportée à la phase T3/plus tard par trois des quatre fiches.

### Gaps to Address

- **Aucun test sur appareil réel** : toutes les fiches le signalent. Prévoir, à la fin des phases 9-10 et 13, une courte liste de contrôle sur l'iPhone de Raven et un iPad (déjà rédigée dans PITFALLS.md, section "Ça a l'air fini mais ça ne l'est pas").
- **Ambiguïté sur `beforeinstallprompt` et un service worker à gestionnaire `fetch` vide** (STACK, confiance BASSE) : à vérifier sur un vrai Android avant de toucher `sw-plateau.js`, hors du périmètre strict de ce jalon si l'installation n'est pas retouchée.
- **Décision explicite manquante pour l'iPad mini portrait (744 px) et le Split View/Slide Over** : aucune fiche ne tranche s'il s'agit d'un comportement voulu ou d'un oubli du seuil de 768 px. À trancher en Phase 11, avec captures.
- **Panorama concurrentiel partiellement invérifié** (Gwent, Sentinels, gestes précis de Snap) : si l'arbitrage d'orientation ou de navigation reste serré après les mesures internes, revenir chercher des captures directes plutôt que des résumés de revues.

## Sources

### Primary (HIGH confidence)
- MDN browser-compat-data 8.1.5 (instantané du 08/10/2026) — support `PointerEvent`, `WakeLock`, `Navigator.vibrate`, `ScreenOrientation.lock`, `touch-action`, unités `dvh`/`svh`, `env()`, container queries, manifeste web
- caniuse — Vibration, Wake Lock, ScreenOrientation.lock, beforeinstallprompt, Fullscreen
- WebKit blog officiel — "Designing Websites for iPhone X" (`viewport-fit`), "More Responsive Tapping on iOS" (`touch-action`), "New WebKit Features in Safari 15.4" (`dvh`/`svh`/`lvh`), "WebKit Features for Safari 27.0"
- Apple Safari Web Content Guide — séquence d'événements souris au toucher
- Code lu directement : `Board.tsx`, `useModeMobile.ts`, `telephone.ts`, `useAppuiLong.ts`, `CarteOuverte.tsx`, `apercu-survol.ts`, `board.css`, `portrait.css`, `ui-app/board.html`, `ui-check/playwright.config.ts`, `web_server.py`, `vite.config.ts`
- DragnCards (code source et issues GitHub) — mode outil tactile, bogues de dépôt connus

### Secondary (MEDIUM confidence)
- Out of Games (Ben Brode sur l'orientation de Marvel Snap)
- Revues concordantes (Hearthstone, Magic Arena, Legends of Runeterra, Slay the Spire, Balatro mobile)
- Forums Apple / Sentry — iPad se déclarant Mac, `maxTouchPoints`
- WebKit bugs 170595 (rotation), 297779 (iOS 26, clavier) — comportements observés mais non reproduits cette session
- NN/g (navigation cachée), Material 3 (barre de navigation), Steven Hoober (prise en main)

### Tertiary (LOW confidence)
- Gwent et Sentinels of the Multiverse sur mobile — revues inaccessibles (403), résumés de recherche contradictoires
- Astuce `<input type="switch">` pour l'haptique iOS — sources communautaires uniquement, contournée par Apple en 26.5
- Densité portrait/paysage téléphone — calcul indicatif à remplacer par mesure Playwright réelle (Phase 11)

---
*Research completed: 13/10/2026*
*Ready for roadmap: yes*
