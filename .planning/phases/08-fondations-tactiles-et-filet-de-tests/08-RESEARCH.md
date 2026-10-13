# Phase 8 : Fondations tactiles et filet de tests - Recherche

**Recherché le :** 13/10/2026
**Domaine :** détection doigt / souris partagée entre plateau React et pages JS non compilées, choix du plateau (écrans limites), mesures d'écran jointes aux signalements, projets Playwright tactiles (Chromium + WebKit)
**Confiance :** HAUTE sur les points d'intégration (lus dans le code, lignes citées) et sur le comportement de l'émulation Playwright (mesuré le 13/10 sur ce poste) ; MOYENNE sur le comportement d'un vrai iPad (non vérifiable sans l'appareil) et sur les largeurs Split View des iPad récents (calculées à partir d'une mesure publiée sur iPad Air 2)

## Résumé

La phase n'ajoute aucune dépendance et ne change rien de visible au plateau, hormis deux lignes de réglage, un bouton dans les en-têtes de menus et une question posée une fois sur écran limite. Le cœur est un **script de tête classique `public/js/saisie.js`**, seul propriétaire de deux attributs posés sur `<html>` : `data-appareil` (`pc` | `tactile`, calculé une fois) et `data-saisie` (`doigt` | `souris`, suit le dernier geste). Il est chargé sans `defer` par `ui-app/board.html` et par les pages de menus, exactement comme `public/js/ui-version.js` aujourd'hui. Côté React, un petit module `ui-app/src/board/saisie.ts` lit ces attributs et écrit les réglages ; la forme du plateau reste décidée par `useModeMobile.ts`, qui apprend le réglage « Plateau » et la préférence d'écran limite.

Trois constats mesurés changent le plan par rapport à la recherche du jalon : (1) **`boutons-bd.test.ts` est VERT aujourd'hui** (290 fichiers, 3315 tests, tous verts le 13/10 à 10 h 28, arbre de travail tel quel) : la règle « déjà rouge » de la feuille de route est périmée, la base doit être relevée à nouveau au premier plan ; (2) **en WebKit émulé sous Windows, `navigator.maxTouchPoints` vaut 0 et `navigator.platform` vaut `Win32`**, même avec `hasTouch` : sans surcharge par `addInitScript`, le cas « iPad qui se déclare Mac » n'est pas testable, et une détection fondée sur `maxTouchPoints` seul classerait l'iPad émulé en PC ; (3) **la page du plateau sur fixture (`/app/board.html?etat=`) n'a ni bouton Réglages ni panneau de signalement** : « ouvrir Réglages sur fixture » (décision verrouillée) est impossible sans toucher `board.tsx`, voir Questions ouvertes.

**Recommandation principale :** poser d'abord la base des suites dans un fichier de la phase, puis `saisie.js` (classification d'appareil + bascule après le geste + mesures d'écran exposées), puis le branchement React (réglages, `useModeMobile`, rapport), puis les pages (bouton, question d'arrivée, mesures), et terminer par les trois projets Playwright `tablette-doigt` (Chromium), `ipad` et `ipad-mini` (WebKit) lancés par une seule commande `npm run tactile`.

## Standard Stack

### Cœur (rien à installer)
| Brique | Version | Rôle | Pourquoi |
|---|---|---|---|
| `PointerEvent.pointerType` | plateforme | Seule source de vérité du dernier geste (`touch`, `pen`, `mouse`) | Mesuré : un toucher émet `pointerdown:touch`, `pointerup:touch`, puis des événements souris de compatibilité qui NE sont PAS des PointerEvent |
| `matchMedia('(pointer: fine)')` + `navigator.platform` / `maxTouchPoints` | plateforme | Classer l'appareil (`pc` / `tactile`) une seule fois, avant tout geste | Seul moyen de garder « PC à écran tactile = souris » tout en faisant basculer l'iPad qui se déclare Mac |
| React 19.2 `useSyncExternalStore` | ^19.2.8 (installé) | `useSaisie()` côté plateau, abonné à l'attribut | Natif, aucune dépendance |
| `@playwright/test` | 1.62.0 épinglé (installé) | Projets tactiles Chromium + WebKit | WebKit révision 2336 (WebKit 26.5) DÉJÀ installé dans `C:\Users\arnau\AppData\Local\ms-playwright\webkit-2336` : aucun `playwright install` à faire |
| Vitest | ^3.2.7 (installé) | Fonctions pures côté TS, et test qui charge `saisie.js` dans jsdom | Précédent : `halo-heros-accord.test.ts` importe un module de `Fusion/.../public/js/` |
| `node --test` | Node 25.3 (Windows) | Modules JS purs des pages | Précédent : `Fusion/marvel-lcg-src/tools/tests-lanceur/*.test.mjs` (22 fichiers, 187 tests) |

### Alternatives écartées
| Au lieu de | On pourrait | Pourquoi non |
|---|---|---|
| Script classique `saisie.js` dans `<head>` | `<script type="module">` | Différé : l'attribut arriverait après le premier rendu des pages à HTML statique ; les phases 9 et 10 poseront du CSS dessus (barre à 44 px), un éclair serait visible |
| `pointerType` | `(hover: hover)` / `(pointer: coarse)` pour décider à chaque geste | Ne bascule pas à l'usage (iPad + trackpad), décision 4 du jalon |
| `pointerType` de l'événement `click` | | **Mesuré : en WebKit, le `click` qui suit un toucher porte `pointerType: "mouse"`** (Chromium : `"touch"`). L'écouter ferait rebasculer en souris à chaque toucher |
| Nouveau champ `mesures` dans `/post_rapport_bug` | Bloc texte en tête du champ `journal` existant | Le moteur filtre les champs par liste blanche (`server_get.py` l. 2116 à 2133) : un nouveau champ serait jeté, et `server_get.py` est déjà modifié par une autre session |

**Installation :** aucune.

## Architecture Patterns

### Structure des fichiers
```
Fusion/marvel-lcg-src/public/js/
├── ui-version.js          # existant : modèle exact (classique, sans defer, dans <head>)
└── saisie.js              # NOUVEAU : seul propriétaire de html[data-appareil] et html[data-saisie],
                           #           expose window.marvelSaisie (décisions pures + mesures())
Fusion/marvel-lcg-src/public/js/prepare/
├── saisie-reglages.js     # NOUVEAU (module) : bouton d'en-tête + fenêtre des deux choix + question d'arrivée
└── (affichage.js)         # modèle à copier, SANS /save_preferences ni synchroniserAffichage
Fusion/marvel-lcg-src/tools/tests-lanceur/
└── saisie.test.mjs        # NOUVEAU si on garde les décisions testables sous node (voir Code Examples)
ui-app/src/board/
├── saisie.ts              # NOUVEAU : clés, lire/écrire réglages, useSaisie(), modePlateauEffectif() pur
├── saisie.test.ts         # NOUVEAU : table de cas + accord avec saisie.js chargé dans jsdom
├── QuestionEcranLimite.tsx# NOUVEAU : la même question à l'entrée du plateau (PagePartie seulement)
├── mobile/useModeMobile.ts# MODIFIÉ : réglage Plateau + préférence écran limite
├── FenetreReglages.tsx    # MODIFIÉ : deux lignes dans l'onglet Apparence, ligne « Table complète » retirée de l'onglet Avancé
├── rapport-bug.ts / RapportBug.tsx # MODIFIÉS : bloc MESURES D'ÉCRAN en tête
└── dico-en.ts             # MODIFIÉ : libellés anglais
ui-app/board.html          # MODIFIÉ : <script src="/public/js/saisie.js?v=1"> à côté de ui-version.js
ui-check/
├── playwright.config.ts   # MODIFIÉ : projets tablette-doigt, ipad, ipad-mini (testMatch restreint)
├── global-setup.ts        # MODIFIÉ : question d'écran limite déjà répondue
├── tests/tactile.spec.ts  # NOUVEAU
└── package.json           # MODIFIÉ : script "tactile" (une seule commande, compatible cmd.exe)
```

### Pattern 1 : deux attributs, un seul propriétaire, posés avant tout style
**Quoi :** `saisie.js` calcule `data-appareil` une fois au chargement, pose `data-saisie` initial (réglage, sinon selon l'appareil), puis suit les gestes. Tout le reste LIT : React (`useSaisie`, `useModeMobile`), les pages (lecture directe de l'attribut), le CSS des phases suivantes.
**Où le charger :** dans `<head>`, sans `defer`, juste après `ui-version.js` :
- `ui-app/board.html` l. 6 (Vite laisse passer un script classique à chemin absolu, précédent `ui-version.js` et `messages.js?v=1` dans `dist/board.html`) ;
- toutes les pages du jeu qui chargent déjà `teinte-page.js` (inventaire mesuré) : `prepare.html`, `galerie.html`, `campagne.html`, `deck-builder.html`, `salon.html`, `cards.html`, `deck.html`, `replay.html`, `rejoindre.html`, `achievements.html`, `palettes-heros.html`. **Hors liste** : `marvel.html` (ancien plateau), `scene.html` (fichier de transition), `authenticate`, `clean_cache`, `credits`, `sandbox`, `puzzle_editor`, `releve-images`, `report`, `fixtures.html`, `main.html`.
- Déclarer chaque `saisie\.js\?v=` dans `deployer.sh` (règle STATE : toute nouvelle référence `?v=` y est déclarée), y compris `$P/app/board.html`.

### Pattern 2 : classer l'appareil, puis décider (fonctions pures)
```
classerAppareil({ platform, maxTouchPoints, pointeurFin, pointeurGrossier }):
  iPadQuiSeDitMac = platform === 'MacIntel' && maxTouchPoints > 1   -> 'tactile' (toujours, même avec trackpad)
  sinon pointeurFin (pointeur PRINCIPAL fin)                         -> 'pc'
  sinon pointeurGrossier || maxTouchPoints > 0                       -> 'tactile'
  sinon                                                              -> 'pc'

saisieInitiale(reglage, appareil):
  'toujours' -> 'doigt' ; 'jamais' -> 'souris' ; 'auto' -> appareil === 'tactile' ? 'doigt' : 'souris'

saisieApresGeste(reglage, appareil, pointerType):
  reglage !== 'auto'  -> valeur fixe du réglage
  appareil === 'pc'   -> 'souris'          (PC à écran tactile : les touchers ne basculent pas)
  pointerType 'mouse' -> 'souris' ; 'touch' | 'pen' -> 'doigt'
```
Mesures qui fondent ce choix (sonde Playwright du 13/10, ce poste) :

| Contexte émulé | maxTouchPoints | platform | pointer: coarse | Classe obtenue |
|---|---|---|---|---|
| WebKit 820x1180 `hasTouch` | **0** | **Win32** | oui | tactile (par `coarse`) |
| WebKit + `addInitScript` (5, `MacIntel`) | 5 | MacIntel | oui | tactile (par iPad-Mac) |
| WebKit sans tactile | 0 | Win32 | non (fine) | pc |
| Chromium 1180x820 `hasTouch` | **1** | Win32 | oui | tactile |
| Chromium PC | 0 | Win32 | non (fine) | pc |

Conséquences : `maxTouchPoints > 1` SEUL raterait les deux émulations ; le critère « pointeur principal fin » est ce qui garde un portable Windows tactile en souris (son pointeur principal est le pavé tactile) ; l'exception `MacIntel && maxTouchPoints > 1` est ce qui garde l'iPad tactile même s'il rapportait `(pointer: fine)` avec un trackpad (comportement réel non vérifié, confiance BASSE, d'où l'exception explicite). La lecture de `navigator.platform` est une exception assumée à « aucune lecture d'agent utilisateur » (piège 4 du jalon) : elle sert uniquement à repérer l'iPad, à documenter dans le code.

### Pattern 3 : la bascule s'applique APRÈS le geste
- Écouter en capture sur `document` : `pointerdown` (mémorise le type candidat et « geste en cours »), `pointerup` / `pointercancel` (fin du geste), `pointermove` de type `mouse` sans bouton enfoncé (trackpad au repos).
- À la fin d'un geste, appliquer au premier de : l'événement `click` suivant (en capture, puis `setTimeout(0)` pour laisser les gestionnaires du clic s'exécuter d'abord), ou un délai de garde d'environ 400 ms (glisser, appui long : pas de clic). Raison : sur iOS réel, le clic synthétique est ciblé APRÈS `touchend` ; changer la mise en page entre les deux peut le faire tomber à côté (piège 5 du jalon).
- Hystérésis : ignorer un `pointermove` souris dans les ~500 ms qui suivent un `pointerup` tactile (assurance peu coûteuse, l'émulation n'en produit pas).
- **Ne jamais** décider sur `click`, `mouse*` ni `touch*`.
- Conséquence pour les phases 9 et suivantes : un gestionnaire qui doit savoir si LE geste en cours est un doigt lit `evenement.pointerType`, pas l'attribut (qui ne bascule qu'après).

### Pattern 4 : forme du plateau = largeur + réglage + préférence d'écran limite
Recommandation (latitude laissée par CONTEXT) : **deux clés distinctes**.
- `mc_plateau_v1` : `auto` | `telephone` | `tablette` (la ligne « Plateau » des réglages).
- `mc_ecran_limite_v1` : `telephone` | `tablette` (la réponse à la question, consultée seulement en Automatique ET en zone limite).

```
modePlateauEffectif({ reglage, preference, etroit, limite, appareil, forceAdresse }):
  forceAdresse (?mobile)                 -> 'mobile'
  appareil === 'pc' && !etroit           -> 'pc'      (garantie anti-enfermement CONSERVÉE, voir Pièges)
  reglage === 'telephone'                -> 'mobile'
  reglage === 'tablette'                 -> 'pc'
  !etroit                                -> 'pc'
  appareil === 'tactile' && limite && preference -> preference === 'tablette' ? 'pc' : 'mobile'
  sinon                                  -> 'mobile'  (comportement d'aujourd'hui)
```
Pourquoi deux clés : un iPad mini qui a répondu « Téléphone » debout retrouve le plateau tablette couché (1133 px, hors zone limite) ; un iPad qui passe d'écran partagé à plein écran suit la largeur sans jamais être redemandé ; la question n'écrase jamais un choix explicite. « Changer d'avis dans les Réglages » = choisir Téléphone ou Tablette dans la ligne Plateau (forcé partout). Afficher sous la ligne, en Automatique et en zone limite : « Sur cet écran : tablette (ton choix à l'arrivée) ».

Migration : à la première lecture de `mc_plateau_v1` absente, `mode-plateau === 'pc'` donne `tablette`, toute autre valeur donne `auto`. Retirer la ligne « Table complète comme sur PC » de l'onglet Avancé (`FenetreReglages.tsx` l. 661 à 674) : deux réglages contradictoires sinon. Tests à mettre à jour : `FenetreReglages.test.tsx` l. 66, 68, 139 à 144, 206 à 217 ; `useModeMobile.test.ts` (bloc `modeEffectif`).

Effet immédiat : `useModeMobile` garde son état React (`useState`) et s'abonne en plus à un événement `marvel:plateau` (émis par l'écriture du réglage, côté React comme côté pages) et à `storage`. Le changement d'aiguillage `RenduPartie` (`board.tsx` l. 4222) est le même que celui d'une rotation qui franchit 768 px : l'état de partie, au-dessus de l'aiguillage, survit (ARCHITECTURE du jalon, Pattern 4).

### Pattern 5 : écran limite, bornes chiffrées
`REQUETE_LIMITE = '(min-width: 500px) and (max-width: 767px) and (min-height: 500px)'`, ET `data-appareil="tactile"`. Équivaut à « largeur entre 500 et 767, côté court d'au moins 500 ».

| Appareil (points CSS) | Largeur x hauteur | Résultat | Source |
|---|---|---|---|
| iPhone SE / mini, debout | 375 x 667/812 | téléphone d'office | HAUTE |
| iPhone 14 à 16 Pro Max, debout | 390 à 440 | téléphone d'office | HAUTE |
| Gabarit `s24` du harnais (S24 Ultra de l'utilisateur) | 480 x 1050 | téléphone d'office (d'où 500 et non 480) | `playwright.config.ts` l. 29 |
| iPhone SE couché | 667 x 375 | hors zone (hauteur 375) : bandes, comme aujourd'hui | HAUTE |
| iPhone couché | 812 à 956 x 375 à 440 | plateau PC réduit, comme aujourd'hui | HAUTE |
| iPad mini debout | 744 x 1133 | **ZONE LIMITE** | CONTEXT |
| iPad mini couché | 1133 x 744 | tablette d'office | |
| iPad 10/11, Air 11 debout | 820 x 1180 | tablette d'office | CONTEXT |
| iPad 1024 couché en Split View 1/2 | 507 x 768 | ZONE LIMITE | mesure publiée iPad Air 2 (useyourloaf) |
| iPad 1024 couché, 2/3 | 694 x 768 | ZONE LIMITE | idem |
| iPad 768 debout, Split View | 438 x 1024 | téléphone d'office | idem |
| iPad 1180 couché, 1/2 (calculé) | ~585 x 820 | ZONE LIMITE | MOYENNE (calcul (L-10)/2) |
| iPad Pro 13 couché, 1/2 (calculé) | ~683 x 1032 | ZONE LIMITE | MOYENNE |
| Slide Over / 1/3 | 320 à 375 | téléphone d'office | MOYENNE |
| Fenêtre PC étroite | n'importe | jamais limite (appareil `pc`) | règle |

Attention : le descripteur Playwright « iPad (gen 11) » déclare 656 x 944 (dpr 2.5), ce qui ne correspond pas à l'iPad A16 réel (820 x 1180 en points, confiance MOYENNE) : ne pas l'utiliser, régler les tailles à la main.

### Pattern 6 : la question, une seule fois, jamais fermable sans choix
- **Accueil** (`prepare.html`, `state.accueil`) : à la suite de la chaîne existante de `app.js` l. 5522 à 5539 (langue, puis affichage, puis phase du méchant), une fenêtre de plus, mêmes gardes : `!creationCampagne()`, `estEcranLimite()`, clé `mc_ecran_limite_v1` absente. Mise en fin de chaîne : aucun ordre existant ne bouge.
- **Entrée du plateau** : dans `PagePartie` seulement (pas `PageEtat`, pas spectateur, pas `estCadre()`), mêmes conditions. Couvre « arrivé par un lien de partie » sans avoir à le détecter : si la clé manque en zone limite, on demande.
- Rotation ou redimensionnement EN PARTIE vers la zone limite sans réponse : ne pas interrompre, garder le comportement d'aujourd'hui (téléphone) ; la question viendra à la prochaine entrée d'accueil ou de plateau.
- Stockage indisponible (navigation privée) : ne pas demander, comme `langueDejaChoisie()` (`langue.js` l. 80 à 88).
- Forme : modèle `demanderLAffichage()` (`app.js` l. 1646 à 1703 : `.deck-modal`, `.af-choix`, pas de fermeture au clic extérieur), mais **le toucher d'une vignette vaut réponse et ferme** (pas de bouton Valider : CONTEXT dit « il faut toucher une vignette »). Vignettes en SVG en ligne (plateau en bandes / table complète), aucune image : évite toute question de route serveur pour les images côté plateau.
- Note produit : une application installée sur iOS repart d'un localStorage vide (STACK du jalon) : la question y sera reposée une fois. Acceptable (« par appareil »), à ne pas contourner.

### Pattern 7 : mesures d'écran invisibles, partout où l'on signale
Points d'envoi recensés (tous POST `/post_rapport_bug`, JSON `{nom, description, ecran, siege, journal, capture}`) :
- plateau : `ui-app/src/board/RapportBug.tsx` l. 153 à 178 (`journal` = `rapportEnTexte(rapport)`, ou `''` si le monde manque) ;
- pages : `public/js/prepare/panneau-bug.js` l. 284 à 302 (`journal: ""`), module unique chargé par `prepare.html` l. 46, `galerie.html` l. 44, `salon.html` l. 52.
- `public/js/marvel/error_dialog.js` (ancien plateau) : intouchable, hors périmètre.

Recommandation : une seule implémentation, `window.marvelSaisie.mesures()` dans `saisie.js`, qui rend des lignes de texte. Le plateau l'appelle (accès typé, repli « mesures indisponibles » sous Vitest) et l'insère dans `ContexteBug` (`rapport-bug.ts` l. 106) puis dans la section CONTEXTE de `rapportEnTexte` (l. 480 à 504), donc aussi dans « Copier » et « Télécharger » ; si le monde manque, envoyer le bloc seul. Les pages remplacent `journal: ""` par le bloc. **Toujours en TÊTE** : le site tronque `journal` à 400 000 caractères (`site/orchestrateur.py` l. 185, l. 2446) et l'affiche replié sous « Journal de la partie » (l. 6010 à 6012).

Contenu du bloc :
- Fenêtre : `innerWidth x innerHeight`, `visualViewport` (largeur, hauteur, `scale`), `screen.width x height`, `devicePixelRatio`, orientation, mode installé (`(display-mode: standalone)` ou `navigator.standalone`), contenu de la balise viewport (dit si `viewport-fit=cover` est posé, utile pour SAISIE-05 en phase 12).
- Zones sûres : haut, droite, bas, gauche lus sur une sonde (voir Code Examples).
- Saisie : `data-saisie`, réglage Écran tactile, `data-appareil`, dernier `pointerType` vu, `maxTouchPoints`, `platform`, `(pointer)`, `(hover)`, `(any-hover)`.
- Plateau : réglage Plateau, préférence écran limite, zone limite oui/non, forme rendue (plateau seulement : `mode` de `useModeMobile`, passé par `board.tsx` à `useRapportBug`), `html.tel` côté pages.

### Anti-patterns
- **Mettre la saisie dans `useModeMobile`** : chaque passage doigt / trackpad démonterait le plateau (ARCHITECTURE du jalon, anti-pattern 2).
- **Remplacer les `(pointer: coarse)` existants** (liste plus bas) : hors phase, change le PC tactile et l'iPad sans décision.
- **Réutiliser le module `affichage.js` tel quel** : il envoie à `/save_preferences` (l. 27 à 36) et se synchronise avec le compte ; la décision est « par appareil uniquement ».
- **Mettre le réglage dans `ui-app/src/board/mobile/`** : il concerne d'abord le plateau PC (même erreur que `useAppuiLong`).
- **Un projet Playwright sans `testMatch`** : `npm run captures` (sans `--project`) tenterait des captures WebKit contre des références inexistantes, et chaque spec sans projet tournerait aussi sous WebKit.

## Détections pointeur / tactile existantes (à NE PAS modifier en phase 8)

| Fichier : ligne | Détection | Rôle |
|---|---|---|
| `ui-app/src/board/mobile/useModeMobile.ts:37` | `(max-width: 767px)` | disposition (axe séparé) |
| `ui-app/src/board/mobile/telephone.ts:17` | `(max-width: 767px), (pointer: coarse) and (max-height: 500px)` | fonctions du téléphone |
| `ui-app/src/board/mobile/telephone.ts:56-63` | `pointerdown` + `keydown` en capture (horodatage seul) | dernier geste pour vibrations / Annuler |
| `ui-app/src/board/Board.tsx:149` | `(pointer: coarse) and (orientation: landscape) and (max-height: 520px)` | échelle du téléphone couché |
| `ui-app/src/board/board.css:574` | `(min-width: 861px) and (pointer: fine)` | |
| `ui-app/src/board/board.css:2163` | `(max-width: 860px), (pointer: coarse)` | menu de carte en feuille basse |
| `ui-app/src/board/board.css:5602` | `(pointer: coarse) and (orientation: landscape) and (max-height: 560px)` | Fin du tour masqué |
| `ui-app/src/board/board.css:6017` | `(max-width: 1100px), (pointer: coarse)` | barre qui s'enroule |
| `ui-app/src/board/manuel/VoletAideManuel.tsx:114` | `(max-width: 1099px), (pointer: coarse)` | aide auto |
| `ui-app/src/board/manuel/appui-tactile.ts:25` | `touch` ou `pen` | appui compté |
| `ui-app/src/board/CartouchePhase.tsx:1647` | `pointerType !== 'mouse'` | |
| `ui-app/src/board/NomsDeCartes.tsx:47-53` | `pointerType === 'mouse'` | survol des noms |
| `ui-app/src/board/RecapPhaseMechant.tsx:828, 878` | `pointerType === 'mouse'` | |
| `ui-app/src/board/CoucheTriche.tsx:620, 633` | `appuiCompte`, `TouchEvent` | |
| `ui-app/src/board/sons.ts:219` | `pointerType` | |
| `ui-app/src/board/glisser/useGlisser.ts:88`, `placement/useGlisserPanneau.ts:160`, `ordre/useReordonner.ts:180`, `manuel/CoucheSelection.tsx:84, 111` | `pointerType` | glisser, sélection |
| `public/js/prepare/app.js:76` | `SANS_SURVOL = !matchMedia('(hover: hover)')`, lu une fois | survol de l'assistant |
| `public/js/prepare/tel.js:8` | `(max-width: 767px)` -> `html.tel` | disposition des pages |
| `public/js/prepare/sons.js:197`, `public/js/campagne/app.js:294` | `pointerType` | |
| `public/css/prepare/prepare.css:1922, 2534, 2639`, `public/css/deckbuilder.css:345` | `(hover:none)`, `(pointer: coarse)` | |

Aucune lecture de `navigator.userAgent` ni `platform` dans `ui-app/src` ni `public/js` (hors `marvel/`, `lib/`) : `saisie.js` sera la seule, commentée.

## Don't Hand-Roll

| Problème | Ne pas construire | Utiliser | Pourquoi |
|---|---|---|---|
| Fenêtre modale des pages | une nouvelle modale | `ouvrirModale` / `fermerModale` d'`app.js` (l. 4095, 4113) et le gabarit `.deck-modal` + `.af-choix` de `demanderLAffichage` | même apparence, même règle « pas de fermeture à côté » |
| Bouton d'en-tête iconisé | du CSS d'icône | `poserIcone` d'`icones-entete.js` ; Font Awesome 4.7 a `fa-hand-pointer-o`, `fa-tablet`, `fa-mobile`, `fa-sliders` | cohérence avec FR/EN et Affichage |
| Ligne de choix dans les Réglages | un nouveau composant | `LigneChoix` de `FenetreReglages.tsx` | pastilles, `detail`, grisé déjà gérés |
| Envoi du signalement | une nouvelle route | `/post_rapport_bug` et le champ `journal` | aucune modification moteur ni site |
| Paramétrer un projet Playwright (iPad qui se dit Mac) | des conditions sur `testInfo.project.name` | option de fixture `test.extend({ ipadMac: [false, { option: true }] })` réglée par projet | motif documenté « Parameterized Projects » |
| Appui long, glisser | rien en phase 8 | `useAppuiLong`, `useGlisser` existants | phases 9 et 10 |

## Common Pitfalls

### Piège 1 : la base des suites est fausse dans la feuille de route
**Ce qui se passe :** ROADMAP et REQUIREMENTS disent `boutons-bd.test.ts` déjà rouge. Mesuré le 13/10 : **vert** (4 tests), et Vitest complet vert (290 fichiers, 3315 tests, 68 s). La base dépend en plus de l'arbre de travail actuel, qui porte 136 fichiers modifiés par d'autres sessions (refonte de la phase du méchant : `board.tsx`, `Board.tsx`, `board.css`, `boutons-bd.css`...).
**Comment l'éviter :** premier geste du premier plan = relever la base (commandes en Code Examples) dans `.planning/phases/08-.../08-BASE-SUITES.md`, avec `git status --short | wc -l` et `git stash list` (10 entrées au 13/10). Ne pas réécrire la feuille de route sans accord, mais signaler l'écart à l'utilisateur (règle « corriger la doc au passage »). Autre écart à signaler : STATE.md parle encore d'un codebase de travail `~/marvel-work/fusion/marvel-lcg-src`, supprimé le 31/08 (GUIDE-CREATION-CONTENU §1.1).

### Piège 2 : `board.tsx` est en cours de modification par une autre session
**Ce qui se passe :** la phase 8 doit toucher `board.tsx` (props de `FenetreReglages` l. 5068 à 5140, `useModeMobile` l. 1485 et 1976 à 1981, question d'entrée, `useRapportBug`). Le fichier est `M` dans l'arbre, comme `Board.tsx` et `board.css`.
**Comment l'éviter :** appliquer à `board.tsx` la règle commune prévue pour `Board.tsx` : `git stash list`, vérifier que la refonte de la phase du méchant est close ou demander, et limiter les modifications de `board.tsx` à des ajouts de lignes localisés. Ne jamais écraser un fichier depuis HEAD (mémo « plateau local = arbre de travail »).

### Piège 3 : l'émulation WebKit ne dit pas qu'elle est un iPad
**Ce qui se passe :** WebKit Playwright sous Windows rapporte `maxTouchPoints = 0`, `platform = "Win32"`, et l'agent utilisateur par défaut de WebKit Playwright est déjà « Macintosh » ; Chromium `hasTouch` rapporte `maxTouchPoints = 1`.
**Comment l'éviter :** projets `ipad` et `ipad-mini` avec un `addInitScript` qui surcharge `Navigator.prototype.maxTouchPoints` (5) et `platform` (`MacIntel`) (vérifié : la surcharge prend, en WebKit comme en Chromium), plus un agent utilisateur de Mac explicite. Garder la classification par `(pointer: coarse)` pour ne pas dépendre de la surcharge.

### Piège 4 : décider sur le `click`
**Ce qui se passe :** mesuré, WebKit émet après un toucher : `pointerover:touch pointerdown:touch pointerup:touch`, puis `mouseover`, `mousedown` et un `click` dont `pointerType` vaut `"mouse"`.
**Comment l'éviter :** ne lire que `pointerdown` / `pointerup` / `pointercancel` / `pointermove`. Test Playwright : après un `tap()`, l'attribut doit valoir `doigt`.

### Piège 5 : réenfermer un joueur en plateau téléphone sur PC
**Ce qui se passe :** `useModeMobile.ts` l. 39 à 56 et le test « n'accepte JAMAIS de rendre un PC en mode telephone » existent parce que l'utilisateur s'est déjà retrouvé enfermé (réglage inatteignable). Un « Plateau : Téléphone » honoré sur un PC large rouvre ce piège.
**Comment l'éviter :** garder la règle `appareil === 'pc' && !etroit -> 'pc'` et **masquer la ligne Plateau sur un PC à fenêtre large** (montrée si appareil tactile OU fenêtre étroite, à l'image de `montrerDisposition = surAppareilMobile` aujourd'hui) : pas de faux bouton (piège 14 du jalon). Test : sur le gabarit téléphone, choisir Téléphone puis revenir à Automatique par les Réglages du plateau en bandes. Si l'utilisateur veut au contraire « Téléphone » partout, le lui faire trancher (voir Questions ouvertes).

### Piège 6 : les spectateurs et la relecture rejouent les réglages du joueur
**Ce qui se passe :** `cadre-joueur.ts` l. 27 recopie toute clé `mc_*` et `mode-plateau` dans le cadre du spectateur, mais en remplaçant `localStorage` depuis un MODULE (`board.tsx`), donc après l'exécution de `saisie.js` dans `<head>` du cadre : `saisie.js` y lira les réglages réels du spectateur.
**Comment l'éviter :** en phase 8, `saisie.js` ne pose rien de plus dans un cadre (`?cadre` dans l'adresse : garder `souris` par défaut) et la question d'écran limite ne s'affiche jamais dans un cadre ni pour un spectateur. Noter pour les phases 9 et 10 que la saisie du joueur devra être publiée si le rendu en dépend. Les nouvelles clés en `mc_` voyagent déjà avec le joueur : voulu pour la forme du plateau.

### Piège 7 : le formulaire change alors qu'il ne doit pas
**Ce qui se passe :** CONTEXT exige des mesures invisibles.
**Comment l'éviter :** aucun champ ni case ajouté à `PanneauBug.tsx` ni à `panneau-bug.js` ; test Playwright qui intercepte `/post_rapport_bug` par `page.route` (rien ne part au site) et vérifie le bloc dans `journal`, plus un test Vitest du corps envoyé par `useRapportBug().envoyer`.

### Piège 8 : nouveau fichier invisible au serveur, ou en cache
**Ce qui se passe :** sous `launcher.py`, `public/` est copié dans `.game/` au démarrage : un fichier ajouté ensuite est en 404 silencieux ; sous `launcher_fast.py`, `.game/public` est un lien et le fichier est servi tout de suite. Les pages sont en cache 60 s.
**Comment l'éviter :** tester sur un moteur `launcher_fast` (ou le moteur d'essai, voir plus bas) ; `?v=` déclaré dans `deployer.sh`. Pour Node, les chemins WSL ne passent pas : `//wsl.localhost/Ubuntu/...` pour un `node --check`.

### Piège 9 : `node --test` sur un dossier échoue sous Node Windows
**Mesuré :** `node --test tools/tests-lanceur/` rend un faux échec (« test failed » sur le dossier). Il faut le motif entre guillemets : `node --test "tools/tests-lanceur/*.test.mjs"` (187 tests verts le 13/10).

### Piège 10 : le plateau sur fixture n'a ni Réglages ni signalement
**Ce qui se passe :** `PageEtat` (`board.tsx` l. 1473 à 1625) rend `Board` ou `PlateauMobile` avec `outils` = seulement les boutons de mode d'action ; `FenetreReglages` (l. 5068) et `PanneauBug` (l. 4843) n'existent que dans `PagePartie`.
**Comment l'éviter :** voir Questions ouvertes ; en attendant, la partie « toucher une carte, bascule » se teste sur fixture, et « ouvrir Réglages » + « signalement depuis la partie » sur une partie neuve d'un moteur d'essai.

## Code Examples

### Relever la base AVANT tout changement (depuis WSL)
```bash
# Mesuré le 13/10/2026 : Vitest 290 fichiers / 3315 tests verts (68 s) ; tsc vert (14 s) ; node --test 187/187.
cd "/mnt/c/Users/arnau/Desktop/Marvel LCG"
git status --short | wc -l ; git stash list | wc -l
cd ui-app
npx vitest run --reporter=dot 2>&1 | grep -v 'localstorage-file\|trace-warnings' | tail -8
npx tsc --noEmit && echo "typecheck vert"
cd ../Fusion/marvel-lcg-src
node --test "tools/tests-lanceur/*.test.mjs" 2>&1 | tail -8
# Playwright (moteur requis, voir ci-dessous), suites non destructives :
cd "/mnt/c/Users/arnau/Desktop/Marvel LCG/ui-check"
export UI_CHECK_BASE=http://127.0.0.1:<port> WSLENV=UI_CHECK_BASE
npx playwright test tests/captures.spec.ts          # pc, tablette, mobile contre references/
npx playwright test tests/fixtures.spec.ts
npx playwright test tests/plateau-mobile.spec.ts tests/menus-mobile.spec.ts tests/assistant-mobile.spec.ts --project=s24
npx playwright test tests/langue-premiere-fois.spec.ts --project=pc
```
Les avertissements `--localstorage-file was provided without a valid path` sont du bruit de Node 25, pas des échecs. Les suites qui appellent `/new` (`plateau-telephone`, `lancement`, campagnes...) détruisent la partie en cours : seulement sur un moteur d'essai.

### Moteur d'essai pour Playwright (recette vérifiée le 07/10, mémo « tester l'écran sans casser le cache »)
Copie de `launcher_fast.py` vers un `.game-essai-*`, config avec `server_addresses` sur un port libre **inférieur à 32768**, hors 2345 à 2400 et différent des ports cités dans les mémos (2330, 2340 déjà utilisés par d'autres sessions), dossiers de replays et statistiques vers le scratchpad, lancé par `~/marvel-work/python/bin/python3.10 ... --no-browser --config ...`, attente d'un marqueur dans le journal ou d'un PID (jamais `pgrep` sur son propre nom), arrêt par PID, suppression de la copie et du cache avant tout déploiement.

### Projets Playwright (esquisse vérifiée par sonde, à adapter)
```ts
// ui-check/playwright.config.ts : à AJOUTER dans projects (les existants ne bougent pas)
const TACTILE = /tactile\.spec\.ts$/;
const UA_IPAD_MAC = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/26.0 Safari/605.1.15';
{ name: 'tablette-doigt', testMatch: TACTILE,
  use: { browserName: 'chromium', viewport: { width: 1180, height: 820 }, hasTouch: true, isMobile: true } },
{ name: 'ipad', testMatch: TACTILE,
  use: { browserName: 'webkit', viewport: { width: 820, height: 1180 }, hasTouch: true, isMobile: true,
         userAgent: UA_IPAD_MAC, ipadMac: true } },
{ name: 'ipad-mini', testMatch: TACTILE,
  use: { browserName: 'webkit', viewport: { width: 744, height: 1133 }, hasTouch: true, isMobile: true,
         userAgent: UA_IPAD_MAC, ipadMac: true } },
```
```ts
// ui-check/tests/tactile.spec.ts : option de projet + vrai toucher
import { test as base, expect } from '@playwright/test';
const test = base.extend<{ ipadMac: boolean }>({
  ipadMac: [false, { option: true }],
  page: async ({ page, ipadMac }, use) => {
    if (ipadMac) await page.addInitScript(() => {
      Object.defineProperty(Navigator.prototype, 'maxTouchPoints', { get: () => 5, configurable: true });
      Object.defineProperty(Navigator.prototype, 'platform', { get: () => 'MacIntel', configurable: true });
    });
    await use(page);
  },
});
test('le toucher met en doigt, le trackpad en souris, APRES le geste', async ({ page }) => {
  await page.addInitScript(() => {
    const w = window as unknown as { journal: string[] };
    w.journal = [];
    for (const t of ['pointerdown', 'pointerup']) document.addEventListener(t, () => w.journal.push(t), true);
    new MutationObserver(() => w.journal.push('saisie=' + document.documentElement.dataset.saisie))
      .observe(document.documentElement, { attributes: true, attributeFilter: ['data-saisie'] });
  });
  await page.goto('/app/board.html?etat=<fixture existante>');
  await expect(page.locator('html')).toHaveAttribute('data-saisie', 'doigt'); // avant tout geste
  await page.mouse.move(300, 300); await page.mouse.move(320, 330);
  await expect(page.locator('html')).toHaveAttribute('data-saisie', 'souris');
  await page.locator('.scan-card').first().tap();                               // vrai toucher
  await expect(page.locator('html')).toHaveAttribute('data-saisie', 'doigt');
  const journal = await page.evaluate(() => (window as unknown as { journal: string[] }).journal);
  expect(journal.lastIndexOf('saisie=doigt')).toBeGreaterThan(journal.lastIndexOf('pointerup'));
});
```
`package.json` de `ui-check` : `"tactile": "playwright test tests/tactile.spec.ts --project=tablette-doigt --project=ipad --project=ipad-mini"` (une seule commande : npm passe par `cmd.exe`, pas de `&&`). Depuis WSL : `UI_CHECK_BASE=... WSLENV=UI_CHECK_BASE npm run tactile`.

`global-setup.ts` l. 42 à 48 : ajouter `localStorage.setItem('mc_ecran_limite_v1', 'tablette')` (ou la clé retenue) à côté des autres réponses de premier lancement ; le test de la question l'efface lui-même avec le garde `sessionStorage` de `langue-premiere-fois.spec.ts` l. 19 à 27 (sinon le rechargement efface la réponse et le test accuse le produit). `storageState` est produit par Chromium mais vaut aussi pour WebKit.

### Sonde des zones sûres (vérifiée : rend `"0px"` en émulation)
```js
// dans saisie.js, utilisé par mesures()
function zonesSures() {
  var s = document.createElement("div");
  s.style.cssText = "position:fixed;left:0;top:0;width:0;height:0;visibility:hidden;pointer-events:none;" +
    "padding:env(safe-area-inset-top) env(safe-area-inset-right) env(safe-area-inset-bottom) env(safe-area-inset-left)";
  (document.body || document.documentElement).appendChild(s);
  var cs = getComputedStyle(s);
  var r = { haut: cs.paddingTop, droite: cs.paddingRight, bas: cs.paddingBottom, gauche: cs.paddingLeft };
  s.remove();
  return r;
}
```
En émulation, les zones sûres valent toujours 0 (PITFALLS du jalon, point 4) : seul un vrai appareil donnera des valeurs, c'est justement l'intérêt de les joindre.

### Tester `saisie.js` (script classique) depuis Vitest
Précédent d'import d'un fichier du jeu : `ui-app/src/board/halo-heros-accord.test.ts`. Pour un script classique, lire le fichier (`readFileSync(resolve(__dirname, '../../../Fusion/marvel-lcg-src/public/js/saisie.js'))`), l'exécuter dans jsdom (`new Function(code)()` après avoir bouchonné `matchMedia` et `navigator`), puis comparer `window.marvelSaisie.classerAppareil` / `saisieApresGeste` à la même table de cas que `saisie.ts`. Sous jsdom sans `saisie.js` chargé, l'attribut est absent : `useSaisie()` doit valoir `souris` et `useModeMobile` garder son comportement (le bouchon de `test-setup.ts` l. 7 à 18 rend `matches: false` partout), ce qui laisse les 3315 tests existants inchangés.

## State of the Art

| Ancien | Actuel | Quand | Impact |
|---|---|---|---|
| `mode-plateau` : `auto` / `pc` (« Table complète comme sur PC », onglet Avancé, visible sur écran étroit seulement) | `mc_plateau_v1` : `auto` / `telephone` / `tablette` dans l'onglet Apparence + `mc_ecran_limite_v1` | phase 8 | migration `pc` -> `tablette` ; tests `FenetreReglages.test.tsx` et `useModeMobile.test.ts` à revoir |
| `SANS_SURVOL` figé au chargement (`app.js` l. 76) | inchangé en phase 8 | | branchement sur `data-saisie` : plus tard (ARCHITECTURE du jalon, T3) |
| `PlateauPaysage.tsx` (cité par le brief) | supprimé (`9f0b6fac`) | 10/2026 | ne pas le recréer |

## Open Questions

1. **« Ouvrir Réglages » sur fixture (décision verrouillée) alors que la page fixture n'a pas de Réglages.**
   - Ce qu'on sait : `PageEtat` n'a ni `FenetreReglages` ni `PanneauBug` (`board.tsx` l. 1473 à 1625, l. 5422).
   - Options : A) tester Réglages et signalement sur une partie neuve d'un moteur d'essai (aucun code de plus, recommandé) ; B) monter `FenetreReglages` dans `PageEtat` (une cinquantaine de props, `board.tsx` en cours d'édition par une autre session) ; C) n'éprouver que `ContenuOnglet` en Vitest.
   - Recommandation : A pour Playwright + C pour le détail des lignes. À confirmer avec l'utilisateur, la décision disant « plateau sur fixture ».
2. **« Plateau : Téléphone » sur un PC à fenêtre large.**
   - Recommandation : ligne masquée et sans effet (garantie anti-enfermement conservée). Si l'utilisateur veut l'inverse, il faut supprimer le test « n'accepte JAMAIS de rendre un PC en mode telephone » en connaissance de cause.
3. **Le réglage « Plateau » doit-il changer la mise en page des pages de menus ?**
   - Ce qu'on sait : les pages basculent en téléphone par CSS `(max-width: 767px)` (`tel.js` l. 8, `prepare-tel.css`, `tel-pages.css`) : aucun réglage JS ne peut l'inverser sans réécrire ces feuilles.
   - Recommandation : en phase 8, les pages AFFICHENT et MODIFIENT la valeur (critère 2 : « respecté sur le plateau et sur les pages » lu comme « même valeur partagée ») ; l'effet sur les menus relève de la phase 11. À faire confirmer.
4. **Comportement réel d'un iPad avec trackpad** (`pointer: fine` ou `coarse` ? `pointermove` souris après un toucher ?) : non vérifiable ici ; l'exception iPad-Mac et l'hystérésis couvrent les deux cas. À contrôler sur un vrai iPad quand l'occasion se présente (hors backlog automatique).
5. **Les largeurs Split View des iPad récents** sont calculées, pas mesurées (MOYENNE) ; la borne 500 tient de toute façon (au-dessus des 480 du gabarit `s24`, en dessous des 507 mesurés en 1/2).

## Sources

### Primaires (HAUTE)
- Code lu, lignes citées : `ui-app/board.html`, `ui-app/vite.config.ts`, `ui-app/deployer.sh`, `ui-app/src/board.tsx`, `ui-app/src/board/{FenetreReglages.tsx, RapportBug.tsx, rapport-bug.ts, affichage.ts, cadre-joueur.ts, mobile/useModeMobile.ts, mobile/useModeMobile.test.ts, mobile/telephone.ts}`, `ui-app/src/test-setup.ts`, `Fusion/marvel-lcg-src/public/{*.html, js/ui-version.js, js/teinte-page.js, js/tel-pages.js, js/prepare/{app.js, affichage.js, affichage-choix.js, langue.js, tel.js, panneau-bug.js, icones-entete.js}}`, `Fusion/marvel-lcg-src/src/engine/device/web/server/{server_get.py, server_html.py, server_files.py}`, `site/orchestrateur.py`, `ui-check/{playwright.config.ts, global-setup.ts, package.json, tests/langue-premiere-fois.spec.ts, tests/plateau-telephone.spec.ts}`.
- Mesures du 13/10/2026 sur ce poste : sonde Playwright 1.62.0 (WebKit 2336 / 26.5, Chromium 1234) sur `maxTouchPoints`, `platform`, media queries, séquence d'événements de `tap()`, `touchscreen.tap()`, `mouse.move`, surcharge par `addInitScript` ; Vitest complet ; `tsc --noEmit` ; `node --test`.
- Descripteurs d'appareils Playwright lus dans `ui-check/node_modules/playwright-core/lib/coreBundle.js`.
- [Playwright, Parameterized Projects](https://playwright.dev/docs/test-parameterize) : option `{ option: true }` réglée par projet.

### Secondaires (MOYENNE)
- [useyourloaf, iOS 9 Slide Over and Split View](https://useyourloaf.com/blog/ios-9-slide-over-and-split-view/) : 1024, 694, 507 (couché) et 438 (debout) sur iPad Air 2.
- [Apple, Adopting Multitasking on iPad](https://developer.apple.com/library/archive/documentation/WindowsViews/Conceptual/AdoptingMultitaskingOniPad/QuickStartForSlideOverAndSplitView.html) : proportions 1/3, 1/2, 2/3, sans valeurs en points.
- Recherche du jalon `.planning/research/v1.1/` (STACK, ARCHITECTURE, PITFALLS) pour l'iPad qui se déclare Mac (`maxTouchPoints`) et le trackpad en `pointerType: mouse`.

### Tertiaires (BASSE)
- Valeur de `(pointer)` / `(hover)` rapportée par iPadOS avec trackpad : une issue GitHub citée par le jalon, non vérifiée.

## Metadata

**Confiance :**
- Stack : HAUTE, rien à installer, WebKit déjà présent et lancé avec succès.
- Architecture : HAUTE pour les points d'intégration ; MOYENNE pour le modèle à deux clés (recommandation dans la latitude laissée, à valider au plan).
- Pièges : HAUTE pour ceux mesurés (base verte, WebKit sans `maxTouchPoints`, `click` en `mouse`, `node --test` sur dossier, fixture sans Réglages) ; MOYENNE pour le comportement iOS réel.

**Date :** 13/10/2026
**Valable jusqu'au :** environ 20/10/2026 pour la base des suites (l'arbre bouge chaque jour), 30 jours pour le reste.
