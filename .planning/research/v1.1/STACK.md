# Stack Research : jalon v1.1 « Tablette et téléphone »

**Domaine :** jeu de cartes en navigateur, plateau React rendu tactile (tablette) et téléphone repensé (plateau et menus)
**Recherché le :** 13/10/2026
**Confiance globale :** HAUTE pour le support navigateur (données MDN browser-compat-data 8.1.5 du 08/10/2026, caniuse, blogs WebKit et Chrome), MOYENNE pour les comportements fins sur appareil réel (iPad avec trackpad, haptique iOS), qui restent à confirmer sur un vrai iPad et un vrai iPhone.

## Conclusion en une phrase

Aucune dépendance à ajouter : tout ce que le jalon demande existe dans la plateforme (Pointer Events, scroll-snap, `dvh`, `env()`, container queries) ou est déjà écrit à la maison dans le dépôt (appui long, glisser, feuille basse, Wake Lock, vibrations, installation) ; le travail de stack consiste à **brancher un détecteur de dernier geste**, à **corriger trois trous de plateforme** (aperçu au `mouseover`, `viewport-fit=cover` absent, manifeste posé trop tard) et à **accepter trois impossibilités iOS** (pas de vibration, pas de verrou d'orientation, pas de plein écran sur iPhone).

## Ce qui existe déjà (lu dans le code, à réutiliser)

| Brique | Fichier | État |
|---|---|---|
| Choix mobile / PC par largeur 768 px + réglage auto/mobile/pc | `ui-app/src/board/mobile/useModeMobile.ts` | Décide le **composant** (bandes ou PC), pas le mode de saisie. Le mode tablette doit être un axe **séparé** (saisie), pas un troisième rendu. |
| Suivi du dernier geste (horodatage seulement) | `mobile/telephone.ts` (`installerSuiviDuGeste`, écoute `pointerdown` en capture) | Sert aux vibrations. Ne mémorise pas le `pointerType` : c'est le point d'extension naturel du lot T1. |
| Appui long 450 ms | `mobile/useAppuiLong.ts`, `manuel/appui-tactile.ts` (`appuiCompte` filtre déjà `touch`/`pen`) | Maison, testé. À réutiliser pour les infobulles à l'appui long (T2). |
| Glisser (Pointer Events, seuil 6 px) | `glisser/useGlisser.ts`, `placement/useGlisserPanneau.ts`, `ordre/useReordonner.ts` | Maison, déjà conçu « pour le jour où le tactile viendra ». |
| Feuille basse fermable en glissant + Retour Android | `public/js/tel-pages.js` (`ouvrirFeuille`, `feuilleDansHistorique`) | JS non compilé, utilisé par les pages de menus. |
| Écran allumé, vibrations, verrou portrait | `mobile/telephone.ts` (`useEcranAllume`, `vibrer`, `useVerrouPortrait`) | Fait en zone 3, avec repli silencieux. Voir les limites iOS ci-dessous. |
| Plein écran au premier toucher | `mobile/plein-ecran.ts` | Inopérant sur iPhone (voir plus bas), fonctionne sur Android et iPad. |
| Installation (manifeste, SW, `beforeinstallprompt`) | `mobile/installation.ts`, `public/pwa/` | Manifeste injecté **seulement** par le plateau en bandes. Voir le piège `start_url`. |
| Écran « tourne ton téléphone » | `mobile/EcranTourne.tsx` | Le seul « verrou » possible sur iPhone. |

## Recommandation par point (support réel vérifié)

Légende du support : version minimale d'après MDN browser-compat-data 8.1.5 (instantané du 08/10/2026), recoupée avec caniuse quand indiqué. Les joueurs connus sont sur iPhone Safari et iPad, donc iOS 17, 18, 26 et 27 (Safari 27 sorti le 17/09/2026).

### 1. Détection du dernier geste (lot T1) : maison, environ 40 lignes

| API | Safari iOS | Chrome Android | Verdict |
|---|---|---|---|
| `PointerEvent.pointerType` (`touch` / `pen` / `mouse`) | 13 | 55 | Utiliser. C'est LA source de vérité. |
| `navigator.maxTouchPoints` | 13 | 35 | Utiliser seulement pour l'**état initial** avant tout geste. |
| `@media (pointer)`, `(any-pointer)`, `(hover)` | 9 | 41 à 50 | Ne PAS s'en servir pour décider : Chrome Android a un faux positif `(hover: hover)` sur certains Samsung (crbug 41445959, note MDN) et l'iPad avec trackpad est mal décrit par ces requêtes (source communautaire, confiance BASSE). |

Faits utiles :
- L'iPad se déclare Mac par défaut depuis iPadOS 13 (navigation « classe ordinateur ») : l'agent utilisateur contient `Macintosh`. Le seul discriminant fiable sans geste est `maxTouchPoints > 1` (un Mac renvoie 0). Confiance MOYENNE (forums Apple, Sentry, pratique répandue ; pas de page officielle Apple qui le documente).
- Le trackpad et la souris de l'iPad émettent `pointerType === 'mouse'`, le doigt `touch`, l'Apple Pencil `pen`. Confiance MOYENNE (spec Pointer Events + retours WebKit).

**Prescription :**
- Étendre `installerSuiviDuGeste()` (déjà en capture sur `document`) pour retenir aussi `evenement.pointerType`, et écouter `pointermove` côté souris (un trackpad qui bouge sans cliquer doit faire repasser en souris). Exposer un petit magasin (`useSyncExternalStore`, natif React 19) `useSaisie(): 'tactile' | 'souris'`.
- État initial : réglage « Écran tactile : automatique / toujours / jamais » (décision 5), sinon `maxTouchPoints > 0 && !matchMedia('(pointer: fine)').matches`, sinon `souris`.
- Poser `data-saisie="tactile|souris"` sur `<html>` et écrire le CSS tablette sur ce sélecteur (`[data-saisie="tactile"] .barre-haut button { min-height: 44px }`), **pas** sur `@media (hover)`. Une seule source de vérité pour le JS et le CSS, et la bascule automatique de la décision 4 devient gratuite.
- Hystérésis : ne repasser en `souris` qu'au `pointermove` de type `mouse`, jamais sur un `mouseover` (Safari iOS en émet des synthétiques après un toucher).
- Le stockage du réglage suit le modèle existant de `useModeMobile.ts` (localStorage, jamais l'adresse ni un cookie).

**Point d'intégration bloquant identifié :** `Board.tsx` lignes 1423 et 1620 ouvrent l'aperçu sur `onMouseOver={survol}`. Safari iOS émet des événements souris de compatibilité après un toucher : c'est la cause de « un toucher ouvre aperçu + menu et l'aperçu ne se ferme plus ». Remplacer par `onPointerOver` et ignorer si `pointerType !== 'mouse'` (ou si `data-saisie="tactile"`). Le type `PointerEvent` de React expose `pointerType`.

### 2. Gestes : maison, AUCUNE bibliothèque

| Besoin | Solution | Support | Pourquoi |
|---|---|---|---|
| Appui long (infobulles, lecture d'une carte) | `useAppuiLong.ts` existant | Pointer Events iOS 13 | Déjà écrit et testé. iPad n'envoie pas `contextmenu` à l'appui long (constaté et commenté dans `appui-tactile.ts`) : la minuterie est la bonne approche. |
| Empêcher la loupe / le menu de copie iOS pendant l'appui long | `-webkit-touch-callout: none` + `-webkit-user-select: none` sur les cartes | `-webkit-touch-callout` : Safari iOS 2, **iOS seulement** ; `user-select` : préfixe `-webkit-` requis sur Safari iOS | Sans eux, l'appui long ouvre le menu système par-dessus le nôtre. |
| Glisser une carte agrandie à gauche / à droite (Raven 2), livre de campagne page par page | **CSS `scroll-snap-type: x mandatory`** + `scroll-snap-stop: always` sur une rangée défilante | `scroll-snap-type` iOS 11, Chrome 69 ; `scroll-snap-stop` iOS 15, Chrome 75 | Zéro JS, inertie native d'iOS, accessible au clavier et au trackpad. Un `IntersectionObserver` ou `scrollend` suffit pour savoir quelle carte est affichée. |
| Feuille basse fermable en glissant (plateau React) | Petit hook maison `useFeuilleGlissante` (pointerdown sur la poignée, `setPointerCapture`, translation, seuil de distance ou de vitesse) | `setPointerCapture` iOS 13, Chrome 55 | 60 à 80 lignes, même logique que `ouvrirFeuille` de `tel-pages.js` déjà en service. |
| Feuille basse (pages de menus en JS non compilé) | `ouvrirFeuille` existant dans `tel-pages.js` | idem | Ces pages ne sont pas en React : une bibliothèque React ne peut pas les servir. |
| Empêcher le défilement de la page pendant un glisser | `touch-action: none` sur la poignée ou la carte tenue | voir point 7 | Sans ça Safari envoie `pointercancel` dès qu'il décide de défiler. |

**Pourquoi pas de bibliothèque :**
- `@use-gesture/react` 10.3.1 : dernière publication le 21/03/2024 (vérifié sur npm le 13/10/2026). Deux ans et demi sans version, et le dépôt a déjà ses propres hooks qui couvrent appui long, glisser et réordonner.
- `vaul` 1.1.2 : dernière publication le 14/12/2024, **déclaré non maintenu par son auteur** (README et discussion shadcn-ui #8982). À exclure.
- `@base-ui/react` 1.9.0 (09/10/2026) a un composant Drawer avec glissement et crans (page de doc Base UI ; la version exacte d'apparition n'est pas confirmée, confiance MOYENNE). Solide et maintenu, mais il ne servirait que le plateau React, pas les menus en JS non compilé, et il apporte son propre système de calques et de focus à concilier avec les fenêtres existantes. À ne considérer que si les pages de menus migrent en React (voir « Variantes »).
- `motion` 14.1.0 / `react-modal-sheet` 5.6.0 : animation à ressort non demandée (spec : « animations courtes et sobres, coupées en mode sobre »), poids inutile.

### 3. Screen Wake Lock : déjà en place, rien à ajouter

| | Safari iOS | Chrome Android |
|---|---|---|
| `navigator.wakeLock` dans Safari | 16.4 | 84 |
| Dans une application installée (écran d'accueil) | **18.4 seulement** (bug WebKit 254545, cassé de 16.4 à 18.3) | 84 |

Sources : MDN BCD (note explicite « Does not work in standalone Home Screen Web Apps », version_removed 18.4), caniuse, blog WebKit Safari 18.4.

**Conséquence :** un joueur sur iOS 17 qui lance le jeu **depuis l'icône** n'aura pas l'écran maintenu allumé ; dans Safari, si. `useEcranAllume` gère déjà le refus et la redemande au retour au premier plan (`visibilitychange`) : c'est le schéma recommandé. Ne PAS ajouter NoSleep.js ni l'astuce de la vidéo en boucle (batterie, et iOS 17 est en voie de disparition).

### 4. Vibration : impossible sur iOS, assumer

| | Safari iOS | Chrome Android | Firefox Android |
|---|---|---|---|
| `navigator.vibrate` | **Jamais** (aucune version jusqu'à 27.2) | 32, exige une activation utilisateur « collante » (sticky) | Présente mais **désactivée** : renvoie `true` et ne vibre pas |

Sources : MDN BCD, caniuse (« Safari on iOS : not supported 3.2 through 27.2 »), page MDN `Navigator.vibrate` (« Sticky user activation is required »).

**Prescription :**
- Garder `vibrer()` tel quel : il fonctionne sur Android, et l'activation collante est acquise dès le premier toucher, donc la vibration « c'est ton tour » déclenchée par le serveur passe.
- **Masquer l'interrupteur « Vibrations »** quand `typeof navigator.vibrate !== 'function'` (iPhone). Afficher un réglage qui ne fait rien sur l'appareil des joueurs réels est un faux bouton.
- **Ne PAS** adopter l'astuce `<input type="checkbox" switch>` (Safari 17.4+, bibliothèques `ios-haptics` 3.2.0, `web-haptics` 0.0.6) : depuis iOS 26.5, Apple a fermé le déclenchement programmatique, seul un toucher réel sur l'interrupteur caché vibre encore (une seule impulsion). Donc « ton tour » et « attaque subie », qui viennent du serveur, ne peuvent **jamais** vibrer sur iPhone. Seule la « validation » le pourrait, au prix d'un calque invisible sous chaque bouton. Fragile, contourné par Apple une fois déjà : à exclure. Confiance MOYENNE (sources communautaires concordantes, pas de note officielle WebKit).

### 5. Installation en application (PWA)

**Compatibilité avec le routage par extension, vérifiée dans `src/engine/network/web_server.py` (`AddDefaultGet`) :**

| Fichier | Route | Résultat |
|---|---|---|
| `/pwa/plateau.webmanifest` | `r'/pwa/{fichier:[a-z0-9-]+\.(?:png|webmanifest)}'`, sans session ni contrôle de version | OK. Type `application/manifest+json` (`mime_type.py`). |
| `/pwa/icone-*.png` | même route | OK. Un nouvel icône doit garder un nom `[a-z0-9-]` (pas de majuscule, pas de point en plus). |
| `/sw-plateau.js` | route dédiée à la racine (portée `/`), sans session | OK. |
| `.json` générique | **aucune route** | 404 : ne pas servir le manifeste en `.json`. |
| `.woff2` | **aucune route** (seulement `.eot`, `.woff`, `.ttf`, lus à plat dans `public/fonts/`) | 404 : une police auto-hébergée doit être en `.woff`, ou il faut ajouter la route. |
| `.png` générique | route présente, mais lit le chemin **depuis la racine du jeu**, pas depuis `public/` | Une image produite par Vite dans `/app/assets/` serait en 404. `assetsInlineLimit: () => true` dans `vite.config.ts` reste donc indispensable. Le commentaire de `vite.config.ts` (« AUCUNE route pour .png / .webp ») est inexact sur la lettre (les routes existent depuis les livrets de campagne) mais juste sur l'effet. |
| `.svg` | lu à plat dans `assets/textures/` par nom de fichier | Un SVG de l'application doit rester inline. |

Support navigateur (MDN BCD) :

| Membre / API | Safari iOS | Chrome Android | Conséquence |
|---|---|---|---|
| `display: standalone` | 11.3 | 39 | OK. |
| `display: fullscreen` | **non** | 39 | iOS retombe sur `standalone` (chaîne de repli de la spec). Le manifeste actuel est correct. |
| `display_override` | non | 89 | Ignoré sur iOS, sans dommage. |
| `orientation` du manifeste | **non** | 39 | Voir point 6. |
| `icons` | 15.4 (si pas d'`apple-touch-icon` et `purpose` absent ou `any`) | 39 | Le manifeste actuel convient. Ajouter une icône `purpose: "maskable"` pour Android est un plus, non requis. |
| `beforeinstallprompt` | **non** (jusqu'à 27.2) | oui | Le bouton « Installer » discret ne peut exister que sur Android. Sur iPhone : une ligne d'aide « Partager, puis Sur l'écran d'accueil ». |

Faits iOS qui changent la conception :
- **Depuis iOS 26, tout site ajouté à l'écran d'accueil s'ouvre en application web par défaut**, manifeste ou pas (interrupteur « Ouvrir comme app web » activé par défaut). Sans manifeste lu, l'adresse de départ est **la page courante**. Or le manifeste n'est injecté que par le plateau en bandes (`preparerInstallation`) : un joueur qui ajoute l'icône depuis l'accueil ou la préparation n'a pas de manifeste, et un joueur qui l'ajoute en pleine partie risque de rouvrir `/app/board.html?p=...` d'une partie finie. **Prescription :** poser `<link rel="manifest" href="/pwa/plateau.webmanifest">` en dur dans le `<head>` des pages d'entrée (prepare.html, accueil) pour que `start_url: "/"` s'applique partout. Confiance MOYENNE sur la lecture d'un manifeste injecté en JS par iOS (non documenté) : la balise statique supprime la question.
- **Cookies :** à l'ajout sur l'écran d'accueil, Safari copie les cookies du site dans l'application web, puis les deux stockages vivent séparément (WWDC23, blog WebKit Safari 17). Le `session_token` (1 an) et `app_version` sont donc repris, mais **localStorage ne l'est pas** : les réglages (mode, taille du texte, sobre, écran tactile) repartent des valeurs par défaut dans l'application installée. À dire au joueur, pas à contourner.
- **Service worker :** Chrome n'exige plus de gestionnaire `fetch` pour l'installation par le menu depuis Chrome 108 sur mobile (blog Chrome « Revisiting installability criteria »), et signale depuis Chrome 112 un gestionnaire vide comme « no-op ». Le même billet indique que l'affichage automatique de l'invitation exige encore un gestionnaire `fetch`. Incertitude réelle (confiance BASSE) : un gestionnaire vide est-il compté pour `beforeinstallprompt` ? **À vérifier sur un vrai Android** (DevTools, onglet Application, section Manifest et Installability) avant de toucher `sw-plateau.js`. Ne pas ajouter de cache hors ligne : le jeu a besoin du moteur.
- Le Service Worker Static Routing API arrive dans Safari 27 : sans intérêt ici (pas de cache).

### 6. Verrou d'orientation : impossible sur iPhone, la décision d'orientation doit en tenir compte

| | Safari iOS | Chrome Android |
|---|---|---|
| `screen.orientation` (lecture, événement `change`) | 16.4 | 38 |
| `screen.orientation.lock()` | **Jamais** (jusqu'à 27.2, MDN BCD et caniuse) | 38, seulement en plein écran ou en application installée |
| `orientation` du manifeste | **non** | 39 |
| `Element.requestFullscreen()` | **iPad seulement**, 16.4 sans préfixe, « Only available on iPad, not on iPhone » ; bouton de sortie non masquable et glisser vers le bas en sort, « unsuitable for some use cases like games » (note MDN BCD) | 71 |

**Conséquences pour la roadmap :**
- Sur iPhone, ni le verrou portrait ni le plein écran ne marcheront jamais par API. Le seul « verrou » est `EcranTourne.tsx` (demander de tourner le téléphone) piloté par `matchMedia('(orientation: landscape)')`. La décision d'orientation de la partie (portrait, paysage ou les deux) doit donc partir du principe que **les deux orientations arriveront** sur iPhone, quel que soit le réglage.
- Le plus proche du plein écran sur iPhone est l'application installée (`standalone`, barre d'état visible). C'est un argument pour mettre en avant l'installation sur iPhone plutôt que le bouton plein écran.
- `useVerrouPortrait` et `demanderPleinEcran` restent utiles sur Android ; ne rien changer, juste ne pas afficher l'option de verrou quand `screen.orientation.lock` est absent ou rejette.
- TypeScript 6.0.3 type déjà `navigator.wakeLock` et `ScreenOrientation.lock()` dans `lib.dom.d.ts` (vérifié) : les types maison `NavigateurAvecVerrou` et `OrientationVerrouillable` ne sont plus nécessaires. À ne nettoyer que si le fichier est touché pour une autre raison (pas de refacto opportuniste).

### 7. `touch-action`

| Valeur | Safari iOS | Chrome Android |
|---|---|---|
| `manipulation`, `auto`, `none` | 9.3 | 36 |
| `pan-x`, `pan-y`, `pinch-zoom` | 13 | 36 / 56 |
| `pan-left`, `pan-right`, `pan-up`, `pan-down` | **non** | 55 |

**Prescription :** `touch-action: manipulation` sur le corps du plateau en mode tactile (supprime le zoom au double toucher et son délai, garde défilement et pincement), `touch-action: none` uniquement sur les éléments qu'on glisse (carte tenue, poignée de feuille, languettes), `pan-y` sur une rangée verticale qui contient des éléments glissables horizontalement. N'utiliser **aucune** valeur directionnelle (`pan-left`...) : Safari les ignore.

### 8. `100dvh` et zones sûres

| | Safari iOS | Chrome Android |
|---|---|---|
| `dvh`, `svh`, `lvh` | 15.4 | 108 |
| `env(safe-area-inset-*)` | 11 | 69 |
| `env(keyboard-inset-*)`, VirtualKeyboard API, `interactive-widget` | **non** | 94 / 108 |
| `visualViewport` | 13 | 61 |

**Trou trouvé :** le CSS du plateau utilise `env(safe-area-inset-*)` 11 fois et `dvh`/`svh` 49 fois, mais `ui-app/board.html` déclare `width=device-width, initial-scale=1.0` **sans `viewport-fit=cover`** (seul `public/marvel.html` l'a). Avec la valeur par défaut, Safari insère lui-même la page dans la zone sûre (blog WebKit « Designing Websites for iPhone X ») : les `env()` ne servent qu'une fois le contenu étendu sous l'encoche. **Prescription :** ajouter `viewport-fit=cover` au plateau et aux pages téléphone, en même temps qu'on vérifie que chaque bord collé (barre du bas, Fin de tour, languettes) a son `padding: env(...)`. Les deux vont ensemble : ajouter l'un sans l'autre fait passer des boutons sous la barre d'accueil. À vérifier en paysage sur iPhone (encoche à gauche ou à droite). Ne pas ajouter `user-scalable=no` / `maximum-scale=1` (accessibilité, et iOS l'ignore depuis iOS 10).

Hauteur utile : `100dvh` pour le plateau (suit la barre d'adresse), `100svh` pour ce qui ne doit jamais être recouvert. Clavier (connexion, recherche de la galerie) : sur iOS, seul `visualViewport` (événement `resize`) permet de savoir où est le clavier ; `env(keyboard-inset-height)` n'existe pas sur Safari.

### 9. Container queries

| | Safari iOS | Chrome Android |
|---|---|---|
| `container-type` + `@container` (taille) | 16 | 105 |
| Requêtes de style (`style(--x: y)`) | 18 (pas sur l'élément racine) | 111 |
| Requêtes `scroll-state()` | **non** | 133 |

**Prescription :** utiliser les requêtes de **taille** pour ce qui doit s'adapter à sa boîte et non à l'écran : la carte agrandie (Raven 7, moitié haute seulement en paysage), la boîte de la phase du méchant, une rangée « une ligne par famille » (Raven 4). C'est exactement le cas où une même pièce vit dans le plateau PC, sur tablette et en bandes. Proscrire les requêtes de style (iOS 17 exclu) et `scroll-state()` (absent de Safari). Déjà utilisé 4 fois dans le dépôt : pas une nouveauté.

### 10. Fermer un aperçu en touchant ailleurs (décision 2)

| | Safari iOS | Chrome Android |
|---|---|---|
| `<dialog>` | 15.4 | 37 |
| `popover` (attribut) | 17, mais **fermeture au toucher extérieur cassée jusqu'à 18.2** (bug WebKit 267688), correcte depuis 18.3 | 114 |
| `dialog closedby="any"` | **non** (Safari Technology Preview seulement) | 134 |
| `HTMLDialogElement.requestClose()` | 18.4 | 134 |

**Prescription :** ne PAS compter sur `popover` ni `closedby` pour « toucher ailleurs ferme l'aperçu » : sur iOS 17 et 18.0 à 18.2, ça ne marche pas. Garder la méthode maison : un voile transparent (ou une écoute `pointerdown` en capture sur le document) qui ferme, plus la croix de 44 px. C'est ce que fait déjà `ouvrirFeuille` avec son voile.

### 11. Animations et confort

- `prefers-reduced-motion` : iOS 10.3, Chrome 74. Déjà prévu par la spec (couper en sobre ou sur demande système).
- View Transitions (même document) : iOS 18, Chrome 111. Optionnel, absent d'iOS 17 : seulement en amélioration progressive, jamais nécessaire à la compréhension.
- `overscroll-behavior` : iOS 16, partiel (sans effet sur un conteneur sans débordement). Utile pour que la feuille basse ne fasse pas « rebondir » la page derrière.

## Installation

```bash
# Rien à installer pour ce jalon.
# Dépendances existantes conservées : react ^19.2.8, react-dom ^19.2.8,
# typescript ^6.0.3, vite ^8.1.5, vitest ^3.2.7 (ui-app), @playwright/test 1.62.0 (ui-check).
```

### Outils de test (ui-check)

| Outil | Rôle | Remarque |
|---|---|---|
| Projet Playwright **WebKit** avec `devices['iPad Pro 11']` (et un iPhone) | Filet du mode tablette : `hasTouch`, agent utilisateur iPad, `maxTouchPoints` | Aujourd'hui `playwright.config.ts` n'a que du Chromium (projet `s24` tactile). Le moteur WebKit de Playwright n'est pas Safari iOS (pas de barre d'adresse dynamique, pas de zones sûres réelles) mais il attrape les écarts de Pointer Events et de CSS WebKit. Aucune dépendance nouvelle : `npx playwright install webkit`. |
| Tests Vitest du détecteur de geste | Fonction pure (suite d'événements vers `tactile` / `souris`) | Même style que `appui-tactile.ts` : la logique pure à part, le branchement à part. |
| Vrai iPad et vrai iPhone | Wake Lock en application installée, `viewport-fit`, haptique, trackpad | Déjà prévu en T3 ; non remplaçable par l'émulation. |

## Alternatives envisagées

| Recommandé | Alternative | Quand l'alternative serait meilleure |
|---|---|---|
| Hooks maison (appui long, glisser, feuille) | `@use-gesture/react` 10.3.1 | Si l'on devait gérer pincement, rotation et inertie sur un canevas libre. Pas le cas ici, et le paquet n'a pas bougé depuis mars 2024. |
| Feuille basse maison | `@base-ui/react` Drawer (1.9.0) | Si les pages de menus migrent en React et qu'on veut des crans multiples, des feuilles imbriquées et la gestion du clavier virtuel sans les écrire. À réévaluer à ce moment-là. |
| `scroll-snap` CSS pour le glissement latéral | Carrousel en JS (Embla, Swiper) | Jamais pour ce jalon : le défilement natif d'iOS est meilleur et gratuit. |
| `data-saisie` posé par le dernier `pointerType` | `@media (hover: hover) and (pointer: fine)` | Pour un site sans bascule souris / doigt. Ici la décision 4 exige une bascule à l'usage, que les media queries ne donnent pas fiablement sur iPad. |
| Masquer les vibrations sur iPhone | Astuce de l'interrupteur `switch` (`ios-haptics`) | Jamais : contournée par Apple en 26.5, incapable de vibrer sur un événement serveur. |

## À ne PAS utiliser

| Éviter | Pourquoi | Utiliser à la place |
|---|---|---|
| `vaul` | Déclaré non maintenu par son auteur, dernière version 12/2024 | Feuille maison (déjà dans `tel-pages.js`) |
| `onMouseOver` / `onMouseEnter` pour l'aperçu | Safari iOS émet des événements souris après un toucher : c'est le bogue « aperçu qui ne se ferme plus » | `onPointerOver` filtré sur `pointerType === 'mouse'` |
| Glisser-déposer HTML5 (`draggable`) | Inerte au doigt (déjà documenté dans `useGlisser.ts`) | Pointer Events |
| `touchstart` / `touchmove` à la main | Double les Pointer Events, pas de stylet, pas de trackpad | Pointer Events (iOS 13+) |
| `popover` ou `dialog closedby` pour fermer au toucher extérieur | Cassé sur iOS avant 18.3 ; `closedby` absent de Safari | Voile maison + croix |
| `screen.orientation.lock()` comme garantie | N'existe pas sur iOS, même installé | `EcranTourne.tsx` + mise en page qui tient dans les deux sens |
| `display: fullscreen` pensé comme acquis sur iPhone | iOS retombe sur `standalone` | Concevoir pour `standalone` (barre d'état visible, zones sûres) |
| NoSleep.js / vidéo en boucle | Batterie, inutile depuis iOS 18.4 | `navigator.wakeLock` (déjà branché) |
| Unités directionnelles `touch-action: pan-left` etc. | Ignorées par Safari | `pan-x` / `pan-y` |
| Requêtes de conteneur de style, `scroll-state()` | Absentes d'iOS 17 ou de Safari | Requêtes de taille, classes |
| `user-scalable=no`, `maximum-scale=1` | Nuit à l'accessibilité, ignoré par iOS | `touch-action: manipulation` |
| Manifeste en `.json` ou police en `.woff2` | Pas de route serveur (404) | `.webmanifest` sous `/pwa/`, `.woff` sous `public/fonts/` ou inline |

## Variantes de stack selon les décisions à venir

**Si la partie sur téléphone est en portrait seul :**
- Garder `EcranTourne.tsx` comme seul garde-fou sur iPhone ; le verrou réel n'existera que sur Android installé.

**Si la partie supporte les deux orientations :**
- Container queries de taille sur chaque pièce réutilisée (carte agrandie, boîte de phase), parce que la même pièce change de boîte à chaque rotation (Raven 6 et 7 sont des défauts de ce type).
- `env(safe-area-inset-left/right)` obligatoire en paysage (encoche sur le côté).

**Si les pages de menus migrent en React pendant le jalon :**
- Une seule feuille basse partagée devient possible ; c'est le seul cas où `@base-ui/react` mérite une évaluation sérieuse. Sinon, garder deux petites implémentations (React pour le plateau, `tel-pages.js` pour les menus) au même comportement, testées par le même filet Playwright.

## Compatibilité des versions

| Élément | Compatible avec | Notes |
|---|---|---|
| React 19.2 `useSyncExternalStore` | détecteur de geste | Natif, aucune dépendance. |
| TypeScript 6.0.3 `lib.dom` | `wakeLock`, `ScreenOrientation.lock`, `vibrate`, `maxTouchPoints`, `getCoalescedEvents`, `userActivation`, `requestClose` | Tous typés (vérifié dans `node_modules/typescript/lib/lib.dom.d.ts`). `BeforeInstallPromptEvent` reste à typer à la main (déjà fait dans `installation.ts`). |
| Vite 8.1 `assetsInlineLimit: () => true` | routage serveur par extension | À conserver : seuls `.html`, `.js`, `.css` doivent sortir du build. |
| Playwright 1.62 (installé) | `devices['iPad Pro 11']`, WebKit | 1.64.0 est la dernière publiée ; la montée de version n'est pas nécessaire pour ce jalon. |
| Plancher iOS visé | 17 | Tout ce qui est recommandé fonctionne en 17, sauf Wake Lock en application installée (18.4) et la fermeture des popovers (18.3), toutes deux contournées. |

## Sources

- MDN browser-compat-data 8.1.5 (instantané du 08/10/2026, téléchargé via unpkg) : `api.Element.requestFullscreen`, `api.Navigator.vibrate`, `api.WakeLock`, `api.ScreenOrientation(.lock)`, `api.Navigator.maxTouchPoints`, `api.PointerEvent.pointerType`, `css.properties.touch-action.*`, `css.types.length.viewport_percentage_units_*`, `css.types.env.*`, `css.at-rules.container.*`, `manifests.webapp.display(.fullscreen)`, `manifests.webapp.orientation`, `manifests.webapp.icons`, `html.elements.dialog.closedby`, `api.HTMLElement.popover`, `api.VisualViewport`, `html.elements.input.switch`, `css.at-rules.media.hover`. Confiance HAUTE.
- [caniuse : Vibration](https://caniuse.com/vibration), [Wake Lock](https://caniuse.com/wake-lock), [ScreenOrientation.lock](https://caniuse.com/mdn-api_screenorientation_lock), [beforeinstallprompt](https://caniuse.com/mdn-api_window_beforeinstallprompt_event), [Fullscreen](https://caniuse.com/fullscreen). Confiance HAUTE.
- [MDN Navigator.vibrate](https://developer.mozilla.org/en-US/docs/Web/API/Navigator/vibrate) : activation collante requise. HAUTE.
- [MDN manifeste display](https://developer.mozilla.org/en-US/docs/Web/Progressive_web_apps/Manifest/Reference/display) : chaîne de repli. HAUTE.
- [Bug WebKit 254545](https://bugs.webkit.org/show_bug.cgi?id=254545) et [WebKit Features in Safari 18.4](https://webkit.org/blog/16574/webkit-features-in-safari-18-4/) : Wake Lock en application installée. HAUTE.
- [WebKit Features for Safari 27.0](https://webkit.org/blog/18325/webkit-features-for-safari-27-0/) : rien de neuf sur orientation, vibration, plein écran iPhone. HAUTE.
- [Designing Websites for iPhone X (WebKit)](https://webkit.org/blog/7929/designing-websites-for-iphone-x/) : `viewport-fit`. HAUTE.
- [Web Push for Web Apps on iOS (WebKit)](https://webkit.org/blog/13878/web-push-for-web-apps-on-ios-and-ipados/), [WWDC23 What's new in web apps](https://developer.apple.com/videos/play/wwdc2023/10120/), [WebKit Safari 17 beta](https://webkit.org/blog/14205/news-from-wwdc23-webkit-features-in-safari-17-beta/) : copie des cookies à l'installation. MOYENNE.
- [iDownloadBlog : iOS 26 ouvre tout ajout à l'écran d'accueil en app web](https://www.idownloadblog.com/2025/06/17/apple-ios-26-safari-web-apps-home-screen-bookmarks/), [MacRumors iOS 26](https://www.macrumors.com/how-to/save-safari-bookmark-web-app-iphone-home-screen/). MOYENNE.
- [Chrome : Revisiting installability criteria](https://developer.chrome.com/blog/update-install-criteria), [web.dev install criteria](https://web.dev/articles/install-criteria), [Intent to Ship : skip no-op fetch handler](https://groups.google.com/a/chromium.org/g/blink-dev/c/tEFS0BH8UmE/m/kSIIFJFOBAAJ). MOYENNE (ambiguïté sur `beforeinstallprompt`).
- [haptics.kushagragolash.dev](https://haptics.kushagragolash.dev/), [issue Ionic 29942](https://github.com/ionic-team/ionic-framework/issues/29942) : astuce `switch` et sa fermeture en iOS 26.5. MOYENNE à BASSE.
- [Discussion shadcn-ui #8982 « Vaul is unmaintained »](https://github.com/shadcn-ui/ui/discussions/8982), [dépôt vaul](https://github.com/emilkowalski/vaul) ; `npm view` le 13/10/2026 pour vaul 1.1.2, @use-gesture/react 10.3.1, @base-ui/react 1.9.0, motion 14.1.0, react-modal-sheet 5.6.0, ios-haptics 3.2.0, @playwright/test 1.64.0. HAUTE pour les versions.
- [Base UI Drawer](https://base-ui.com/react/components/drawer). MOYENNE (version d'apparition non confirmée).
- [Forums Apple : agent utilisateur iPadOS](https://developer.apple.com/forums/thread/119186), [Sentry #12127](https://github.com/getsentry/sentry-javascript/issues/12127) : iPad se déclare Mac. MOYENNE.
- Code lu : `Fusion/marvel-lcg-src/src/engine/network/web_server.py` (`ReadFile`, `AddDefaultGet`, routes `/pwa/` et `/sw-plateau.js`), `src/engine/lib/mime_type.py`, `public/pwa/*`, `ui-app/vite.config.ts`, `ui-app/board.html`, `ui-app/src/board/Board.tsx` (l. 1133, 1423, 1620), `ui-app/src/board/mobile/{telephone,installation,plein-ecran,useModeMobile,useAppuiLong}.ts`, `manuel/appui-tactile.ts`, `glisser/useGlisser.ts`, `public/js/tel-pages.js`, `ui-check/playwright.config.ts`.

---
*Stack research pour : jalon v1.1 Tablette et téléphone*
*Recherché le : 13/10/2026*
