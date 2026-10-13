# Recherche des pièges : jalon v1.1 Tablette et téléphone

**Domaine :** plateau de jeu de cartes web (React + Vite, plateau PC mis à l'échelle) rendu tactile sur iPad, et plateau + menus refaits pour iPhone Safari
**Recherché le :** 13/10/2026
**Confiance globale :** MOYENNE (mécanismes WebKit bien documentés ; plusieurs causes rattachées au code sont des hypothèses à confirmer sur appareil, signalées comme telles)

Code lu pour rattacher chaque piège : `ui-app/src/board/mobile/useModeMobile.ts`, `telephone.ts`, `useAppuiLong.ts`, `CarteOuverte.tsx`, `plein-ecran.ts`, `installation.ts`, `ui-app/src/board/Board.tsx` (survol, `useEchelle`), `apercu-survol.ts`, `manuel/appui-tactile.ts`, `board.css`, `portrait.css`, `ui-app/board.html`, `ui-check/playwright.config.ts`, `ui-check/tests/plateau-telephone.spec.ts`, `telephone-finitions.spec.ts`, `pages-telephone.spec.ts`, et le commit `959f1402` (retours de Raven).

Phases utilisées ci-dessous : **Tablette** (lots T1, T2), **Téléphone menus**, **Téléphone plateau**, **Orientation**, **Tests**.

---

## Pièges critiques

### Piège 1 : le survol souris se déclenche au toucher, l'aperçu reste collé et le clic est avalé

**Ce qui casse :**
Sur iPad, un toucher rejoue `mouseover`/`mouseenter` avant le `click`. Le plateau PC ouvre son aperçu sur `onMouseOver` avec un minuteur de 200 ms (`Board.tsx`, fonction `survol` vers la ligne 1133). Aucun `mouseout` ne viendra jamais le refermer : c'est exactement le symptôme de la fiche (« un toucher ouvre aperçu + menu et l'aperçu ne se ferme plus »). Pire : WebKit iOS applique une heuristique de « changement de contenu ». Si le contenu change pendant le `mouseover` rejoué (immédiatement, ou via un minuteur court, de l'ordre de 400 ms ou moins selon des retours de terrain), Safari considère le toucher comme un survol et **n'envoie pas le clic** : il faut toucher deux fois. Le même mécanisme vise les règles CSS `:hover` qui basculent `display` ou `visibility`, par exemple `.ma-action.est-indisponible:hover .ma-action-raison { display: block }` (`board.css` vers la ligne 967).

**Pourquoi on se trompe :**
On teste dans Chromium avec la souris, ou avec `hasTouch` sous Chromium : l'heuristique de changement de contenu n'existe que dans WebKit iOS, et ni Chromium ni le WebKit de bureau de Playwright ne la reproduisent.

**Prévention :**
- Remplacer `onMouseOver`/`onMouseEnter` par `onPointerOver`/`onPointerEnter` filtrés sur `evenement.pointerType === 'mouse'` partout où un survol ouvre quelque chose : `Board.tsx` (survol), `apercu-survol.ts`, `MenuActionsCarte.tsx` (lignes 647 et 739), `StatsPartie.tsx:64`, `RecapPhaseMechant.tsx:825`. Le stylet (`pen`) en survol (Apple Pencil récent) reste à trancher, par défaut l'exclure.
- Les règles CSS de révélation au survol passent sous une classe posée par la détection (`html.saisie-souris .x:hover`), pas sous `@media (hover: hover)` seul : la décision 4 (dernier geste) doit pouvoir trancher même sur un iPad avec trackpad.
- La raison « injouable » a déjà sa classe `.a-raison-visible` : au toucher, la poser explicitement (lot T2), ne pas compter sur `:hover`.

**Signes avant-coureurs :** un joueur dit « il faut toucher deux fois » ; aperçu qui reste affiché après un toucher ; tout nouveau `onMouseEnter` dans une revue de code du plateau.

**Phase :** Tablette (T1). Rappel aussi pour Téléphone menus (galerie, assistant : la fiche impose déjà « pas de survol »).

---

### Piège 2 : fermer une couche au `pointerdown` fait traverser le toucher jusqu'à la carte du dessous

**Ce qui casse :**
`CarteOuverte.tsx:97` ferme l'agrandissement sur `onPointerDown` du voile. Au doigt, le `click` de compatibilité est émis après `pointerup`, à l'endroit du toucher : le voile ayant disparu entre-temps, le clic peut tomber sur la carte ou le bouton situé dessous (« clic fantôme »). La décision 2 de la tablette (« toucher ailleurs ferme l'aperçu ») multiplie ce risque sur tout le plateau PC, où sous l'aperçu se trouvent des cartes jouables.

**Pourquoi on se trompe :** à la souris, `mousedown` puis disparition puis `click` sur un autre élément ne produit pas de clic (cibles différentes) ; le comportement tactile de WebKit, qui retrouve la cible au relâchement, est différent. Confiance MOYENNE sur le détail du ciblage selon le moteur : à vérifier par un test, pas à supposer.

**Prévention :**
- Fermer sur `click` du voile (ou sur `pointerup` suivi d'un `preventDefault` sur le `click` qui suit), jamais sur `pointerdown`.
- Le toucher qui ferme ne fait rien d'autre : règle écrite, et test qui touche le voile au-dessus d'une carte jouable puis vérifie que le menu de cette carte ne s'est pas ouvert.

**Signes avant-coureurs :** « j'ai fermé la carte et ça a joué autre chose » ; menu qui s'ouvre juste après une fermeture.

**Phase :** Tablette (T1), Téléphone plateau (le voile actuel est déjà concerné).

---

### Piège 3 : la rotation laisse des mesures périmées (cause probable du « Fin du tour » sur la main)

**Ce qui casse :**
Le correctif `959f1402` masque `.bouton-fin-tour` en `(pointer: coarse) and (orientation: landscape) and (max-height: 560px)`. Il supprime le symptôme, pas la cause. Le retour disait « après **plusieurs** rotations » : un défaut qui dépend de l'historique ne vient pas d'une règle CSS statique, il vient d'un état accumulé. Plusieurs mécanismes du code se combinent :
- iOS fournit des `innerWidth`/`innerHeight` faux ou encore ceux de l'orientation précédente pendant les gestionnaires `resize`/`orientationchange` (WebKit bug 170595). Or au moins sept composants mesurent sur `window.resize` (`CoucheTraitPhase.tsx:67`, `FlechesPhase.tsx:101`, `useAncrageSurTable.ts:74`, `CartouchePhase.tsx:231` et `1392`, `CoucheRencontreSurTable.tsx:108`, `hauteur-de-question.ts:39`, `CadreJoueur.tsx:28`).
- `useEchelle` (`Board.tsx`) écrit `--echelle` sur la racine et bascule `body.plateau-paysage-tel` depuis un `ResizeObserver` : une mesure prise pendant l'animation de rotation fige une échelle fausse si aucun événement ne suit.
- Le seuil de 768 px de `useModeMobile.ts` démonte `PlateauMobile` et monte le plateau PC à chaque rotation d'un grand téléphone (844 px couché) : tout état local (carte agrandie, sélection, place des languettes) est perdu ou recréé.

Ces causes sont des **hypothèses** (confiance MOYENNE) : le défaut n'a pas été reproduit en émulation, et l'émulation ne produit pas les valeurs intermédiaires fausses d'iOS.

**Prévention :**
- Une seule source de géométrie d'écran (un crochet partagé) : `ResizeObserver` sur la racine + `visualViewport` `resize` + `screen.orientation` `change`, mesure au `requestAnimationFrame` suivant puis une seconde mesure après stabilisation (environ 300 à 700 ms). Les composants lisent cette source au lieu d'écouter `window.resize` chacun de leur côté.
- Avant de toucher au code : reproduire chez Raven avec un panneau de diagnostic (voir piège 12) qui affiche `innerWidth`, `innerHeight`, `visualViewport`, `--echelle`, mode rendu, à chaque rotation.
- Test de non-régression qui enchaîne 6 rotations (`setViewportSize` portrait/paysage alternés) puis vérifie par `elementFromPoint` au centre de chaque carte de la main que c'est bien la carte qui est touchée, et aucun élément fixe.

**Signes avant-coureurs :** un défaut qui « apparaît après un moment » ou « après avoir tourné » ; un correctif qui cache un élément au lieu d'expliquer sa position ; un nouveau `window.addEventListener('resize', ...)` dans le plateau.

**Phase :** Orientation (à traiter avant de refaire le plateau téléphone), Tests.

---

### Piège 4 : l'iPad mal classé (se déclare Mac, iPad mini, Split View, trackpad)

**Ce qui casse :**
- Depuis iPadOS 13, Safari envoie un agent utilisateur de Mac et `navigator.platform === 'MacIntel'`. Toute détection par agent utilisateur classe l'iPad comme un ordinateur. Le seul signal fiable est `navigator.maxTouchPoints > 1` (Mac : 0).
- `REQUETE_MOBILE = '(max-width: 767px)'` envoie sur le **plateau téléphone** : l'iPad mini en portrait (744 px de large), un iPad en Split View ou Slide Over (320 à 700 px environ), une fenêtre réduite de Stage Manager. Ce n'est pas un défaut si c'est voulu, mais la fiche tablette ne le dit nulle part.
- Un iPad avec trackpad ou souris envoie des événements de pointeur de type `mouse` : la décision 4 (dernier geste) est la bonne, mais une détection fondée sur `(pointer: coarse)` ou sur `maxTouchPoints` seul se tromperait (confiance BASSE sur la valeur exacte de `pointer`/`hover` rapportée par iPadOS avec trackpad : ne pas s'y fier).

**Prévention :**
- Deux axes indépendants, jamais mélangés : **disposition** (largeur, déjà `useModeMobile`) et **mode de saisie** (dernier `pointerType` sur `pointerdown`, plus le réglage auto / toujours / jamais). `maxTouchPoints > 1` ne sert qu'à choisir le mode de saisie de départ, avant le premier geste.
- Aucune lecture de `navigator.userAgent` ou `platform` dans le nouveau code (aujourd'hui il n'y en a aucune dans `ui-app/src` : garder cet acquis).
- Trancher explicitement le sort de l'iPad mini portrait et de Split View dans la phase Orientation.

**Signes avant-coureurs :** « sur mon iPad j'ai l'écran du téléphone » ; tactile non activé au chargement sur iPad jusqu'au premier toucher.

**Phase :** Tablette (T1), Orientation.

---

### Piège 5 : la bascule doigt/souris fait sauter la mise en page sous le doigt

**Ce qui casse :**
Décision 3 : la barre du haut passe à 44 px en mode tactile. Si la classe tactile est posée au `pointerdown`, la barre grandit pendant le geste, tout descend de 14 px et le `click` atterrit sur autre chose. Autre variante : écouter `mousedown`/`mousemove` pour revenir en mode souris. Les événements souris de compatibilité émis après chaque toucher repasseraient en mode souris aussitôt : bascule à chaque toucher.

**Prévention :**
- Ne lire que `PointerEvent.pointerType`, jamais les événements `mouse*`, pour décider du mode.
- Appliquer le changement de mode après la fin du geste (au `pointerup` ou à l'image suivante après le `click`), avec une hystérésis : un seul mouvement de trackpad ne repasse pas en souris si un toucher vient d'avoir lieu (quelques centaines de ms).
- `telephone.ts` installe déjà un suivi de geste global (`installerSuiviDuGeste`, `pointerdown` en capture) : l'étendre plutôt que d'en créer un second.

**Signes avant-coureurs :** la barre « clignote » ; premier toucher d'une partie qui rate son bouton.

**Phase :** Tablette (T1).

---

### Piège 6 : des cibles de 44 px dans une scène réduite par `transform: scale` ne font plus 44 px

**Ce qui casse :**
Le plateau PC est une scène de 1920 x 940 mise à l'échelle (`SCENE`, `useEchelle`). Sur iPad Air en paysage (1180 x 820) l'échelle vaut environ 0,61 ; en portrait (820 x 1180) environ 0,43. Un compteur de 44 px dans la scène fait donc 27 px, puis 19 px à l'écran. La décision « cibles de 44 px » est vraie dans le CSS et fausse au doigt.

**Prévention :**
- Les commandes tactiles (barre du haut, croix, compteurs) vivent hors de la scène mise à l'échelle, ou compensent l'échelle (`calc(44px / var(--echelle))`).
- Le contrôle des 44 px des tests (`pages-telephone.spec.ts` mesure déjà par `getBoundingClientRect`, ce qui est juste) doit être étendu au plateau en gabarit tablette, en portrait ET en paysage.

**Signes avant-coureurs :** test vert sur le CSS, joueur qui rate les petits boutons ; capture où les compteurs paraissent minuscules.

**Phase :** Tablette (T2), Tests.

---

### Piège 7 : hauteur d'écran Safari (`100vh`, barre d'adresse, barre flottante d'iOS 26, zones sûres)

**Ce qui casse :**
- `100vh` vaut la grande hauteur (barre d'adresse repliée) : il en reste dans `board.css` (lignes 3535, 3570, 4048, 7329), `fleches-phase.css:8` (`height: 100vh` du calque des flèches, qui se décale alors du contenu calé en `dvh`) et `mise-en-place.css:45`.
- `100dvh` varie quand la barre se replie : si la page défile, la scène se redimensionne, `useEchelle` recalcule, la table « respire ».
- **`viewport-fit=cover` est absent** de `ui-app/board.html` et `vitrine.html` (`width=device-width, initial-scale=1.0` seulement). Sans lui, Safari renvoie 0 pour `env(safe-area-inset-*)` : tous les `padding-bottom: calc(... + env(safe-area-inset-bottom, 0px))` (`portrait.css`, `menus-mobile.css`, `board.css:9111`) sont inertes. Ajouter `viewport-fit=cover` change tout d'un coup : en paysage, le contenu passe sous l'encoche.
- iOS 26.0 : les éléments `position: fixed` en bas s'arrêtaient au-dessus de la barre flottante translucide, et le viewport visuel ne se réinitialisait pas après fermeture du clavier (WebKit bug 297779, corrigé en 26.1 d'après les forums Apple). Safari 26 ignore aussi `theme-color` et teinte sa barre d'après les éléments fixes proches des bords.

**Prévention :**
- Pendant une partie, le document ne défile pas (racine fixe, `overflow: hidden` sur `html`/`body`, défilement dans des conteneurs internes) : la barre ne bouge plus et `dvh` reste stable. `plateau-paysage-tel` fait aujourd'hui glisser la table « dans les deux sens » : vérifier que ce défilement est interne.
- `svh` pour ce qui fixe l'échelle, `dvh` pour les conteneurs ; chasser les `100vh` restants.
- Ajouter `viewport-fit=cover` seulement avec un audit de toutes les marges latérales en paysage (encoche, île dynamique) et du bas (indicateur d'accueil), dans une étape dédiée.
- Couleur de fond explicite sur `html` et `body` (Safari 26 échantillonne la racine).

**Signes avant-coureurs :** bouton du bas à moitié sous la barre de Safari ; bande blanche ou teintée sous la barre ; table qui change de taille quand on fait défiler.

**Phase :** Téléphone plateau, Téléphone menus, Orientation.

---

### Piège 8 : l'appui long réveille iOS (bulle de copie, loupe, sélection, glisser d'image)

**Ce qui casse :**
L'appui long est le geste central (lire une carte au téléphone, infobulles à l'appui long en T2, menu du mode manuel). iOS n'émet pas `contextmenu` à l'appui long (le commentaire de `manuel/appui-tactile.ts` le constate déjà) : le `preventDefault` de `useAppuiLong` ne protège donc qu'Android. Sur iOS, il faut `-webkit-touch-callout: none` (bulle « Copier / Ajouter aux Photos » sur les images) et `user-select: none` (loupe, sélection bleue). Sur iPadOS, un appui long sur une `<img>` peut aussi « soulever » l'image pour le glisser-déposer système. `portrait.css` pose déjà `-webkit-touch-callout: none` à trois endroits ; le plateau PC n'en a qu'un (`cartouche-essai.css:995`).

**Prévention :**
- En mode tactile, poser sur les cartes et les boutons : `-webkit-touch-callout: none`, `-webkit-user-select: none`, `user-select: none`, `-webkit-user-drag: none`, et `draggable={false}` sur les `<img>`.
- Ne jamais le poser sur `body` entier : les champs de saisie et le journal doivent rester sélectionnables (et un `user-select: none` hérité a déjà empêché la saisie dans certains Safari, confiance BASSE).
- Un appui long a un seul sens par élément : sur une carte du plateau PC, appui long = infobulle ou menu, pas les deux. La décision 7 (infobulles) et le mode manuel (menu à l'appui long) doivent être réconciliés avant T2.

**Signes avant-coureurs :** sélection bleue sur le nom d'une carte ; menu iOS « Copier » ; image qui suit le doigt.

**Phase :** Tablette (T1, T2), Téléphone plateau.

---

## Pièges modérés

### Piège 9 : double déclenchement (toucher + clic, appui long + clic)

**Ce qui casse :** un gestionnaire `onTouchEnd` ajouté à côté d'un `onClick` exécute l'action deux fois ; après un appui long réussi, le relâchement émet encore un `click`. `useAppuiLong` le gère (`vientDeDeclencher`), mais seulement si chaque `onClick` concerné le consulte.

**Prévention :** un seul canal dans le nouveau code, événements de pointeur + `click`, aucun `onTouch*`. Tout élément qui reçoit `useAppuiLong` vérifie `vientDeDeclencher()` dans son `onClick` (règle de revue, et un test par composant). Le `dblclick` du mode manuel (`CoucheTriche.tsx:1240`) ne se déclenche pas de façon fiable au doigt : ne pas le promettre en T3 sans test sur iPad.

**Phase :** Tablette, Téléphone plateau.

### Piège 10 : zoom au double toucher et au pincement

**Ce qui casse :** un double toucher rapide (compteur +1 +1) zoome la page ; le pincement reste toujours possible car iOS ignore `user-scalable=no` depuis iOS 10. Une page zoomée décale les éléments fixes par rapport au viewport visuel et fausse `elementFromPoint`.

**Prévention :** `touch-action: manipulation` (décidé en T1) sur les éléments interactifs ou leurs conteneurs (la propriété ne s'hérite pas : la poser sur un ancêtre via un sélecteur, pas seulement sur `html`). WebKit documente qu'elle coupe le zoom au double toucher et le délai du clic. Ne pas combattre le pincement : rendre le texte lisible pour qu'il soit inutile, et vérifier que les recalculs utilisent `visualViewport` quand `visualViewport.scale !== 1`. Le support de chaque valeur de `touch-action` par Safari (`pan-x`, `pan-y`, `none` utilisés dans `portrait.css`) est à revérifier sur appareil : les sources consultées divergent.

**Phase :** Tablette (T1), Téléphone plateau.

### Piège 11 : défilement élastique et « tirer pour actualiser »

**Ce qui casse :** si c'est le document qui défile, l'effet élastique d'iOS emporte la table et ses éléments fixes, et un geste vers le bas en haut de page peut recharger la partie. `overscroll-behavior: contain` est posé sur des panneaux (`board.css:186`, `portrait.css:138`, `menus-mobile.css:89`), pas sur la racine.

**Prévention :** document non défilant pendant la partie (piège 7) et `overscroll-behavior: none` sur `html` du plateau (supporté par Safari depuis la version 16, confiance MOYENNE). Dans les menus, garder le défilement natif mais contenir les feuilles basses.

**Phase :** Téléphone plateau, Téléphone menus.

### Piège 12 : régressions PC causées par le code tactile partagé

**Ce qui casse :** le plateau PC devient la base de la tablette. Risques : règles sous `(pointer: coarse)` qui touchent les portables Windows tactiles et les Surface (déjà présent : `board.css` 2163, 6017, 5602, `VoletAideManuel.tsx:114`) ; `user-select: none` qui empêche de copier le journal sur PC ; survol remplacé par un filtre de pointeur qui casse l'aperçu au clavier (`viser` dans `apercu-survol.ts`) ; barre de 44 px qui apparaît sur PC.

**Prévention :** tout le nouveau comportement tactile derrière une classe posée par la détection (`html.saisie-tactile`), jamais derrière `(pointer: coarse)` brut. Le réglage « Écran tactile : jamais » doit redonner le PC au pixel près : réutiliser la comparaison avant/après au pixel déjà faite en zone 2 (`ui-check/comparaison`, 768 à 1920) à chaque lot tablette. Test PC dédié : survol souris, aperçu après 200 ms, toujours vert.

**Phase :** Tablette (T1, T2), Tests.

### Piège 13 : clavier virtuel qui cache le bouton (menus)

**Ce qui casse :** iOS ne redimensionne pas le viewport de mise en page à l'ouverture du clavier ; `interactive-widget` et l'API VirtualKeyboard ne sont pas disponibles dans Safari public. Une barre fixe en bas (« Continuer », « Se connecter ») reste derrière le clavier ou flotte au milieu. Un champ de moins de 16 px déclenche un zoom automatique qui persiste après la saisie. Bug d'iOS 26.0 cité au piège 7.

**Prévention :** champs à 16 px minimum sur téléphone ; bouton d'envoi dans le flux, juste sous le champ, plutôt qu'en barre fixe pendant la saisie ; écoute de `visualViewport` `resize` pour masquer la barre basse quand le clavier est ouvert (écart de hauteur nettement supérieur à 100 px) ; `scrollIntoView` du champ au focus. Concerne connexion, inscription, recherche de la galerie, import marvelcdb, nom de deck.

**Phase :** Téléphone menus.

### Piège 14 : des API absentes sur iPhone affichées comme des réglages

**Ce qui casse :** Raven joue sur iPhone Safari. Or `navigator.vibrate` n'existe dans aucun Safari (retiré de WebKit en 2017) : l'interrupteur « Vibrations » de `telephone.ts` ne fait rien pour lui. Le plein écran (`plein-ecran.ts`) n'existe pas sur iPhone, seulement sur iPad. `screen.orientation.lock` n'existe pas sur iOS : `useVerrouPortrait` retombe sur l'écran « Tourne ton téléphone ». `beforeinstallprompt` (`installation.ts:55`) n'existe pas sur iOS : le bouton d'installation n'apparaît jamais. Un réglage sans effet est exactement le retour n° 5 de Raven.

**Prévention :** détecter la fonction et masquer le réglage qui ne peut rien faire sur l'appareil ; pour l'installation sur iOS, afficher l'instruction « Partager, puis Sur l'écran d'accueil ». Wake Lock existe dans Safari récent (code déjà tolérant au refus).

**Phase :** Téléphone plateau, Téléphone menus.

### Piège 15 : deux orientations = deux fois la surface de défauts

**Ce qui casse :** les sept retours de Raven se partagent entre vertical (4, 5) et horizontal (6, 7) ; un réglage marchait dans une orientation et pas l'autre. Chaque orientation retenue double la matrice à tester, et la rotation elle-même (piège 3) est une troisième source.

**Prévention :** la phase Orientation tranche une orientation principale soignée et dit précisément ce que devient l'autre (tolérée avec les mêmes composants, ou bloquée par `EcranTourne.tsx`), sachant qu'iOS ne permet pas de verrouiller. Chaque réglage du plateau téléphone a un test dans chaque orientation conservée. L'état visible (carte agrandie, sélection en cours) survit à la rotation ou est explicitement refermé.

**Phase :** Orientation (avant Téléphone plateau).

---

## Pièges mineurs

- **Infobulles `title` invisibles au doigt :** remplacées par l'appui long (décision 7) ; vérifier que la même icône n'a pas aussi un appui long métier. Phase Tablette (T2).
- **`:hover` cosmétique collant :** environ 70 règles `:hover` dans `board.css` ; après un toucher l'état reste jusqu'au toucher suivant. Sans gravité si cela ne change que la couleur ; les passer progressivement sous `html.saisie-souris`. Phase Tablette.
- **`touch-action: none` sur des zones larges :** posé pour le glisser (`board.css:91`, `1194`, `glisser.css:212`), il empêche aussi de faire défiler au doigt une liste qui commence sur cette zone. Vérifier au doigt chaque liste du plateau PC sur iPad. Phase Tablette.

---

## Dette technique tentante

| Raccourci | Bénéfice immédiat | Coût à long terme | Acceptable quand |
|-----------|-------------------|-------------------|------------------|
| Masquer un élément qui gêne dans une orientation (`display: none` sous media query) | Retour joueur fermé le jour même | La cause (mesure périmée) frappe ensuite un autre élément fixe | Seulement si la cause est notée et une fiche ouverte |
| `(pointer: coarse)` comme interrupteur tactile | Une ligne de CSS | Faux sur iPad avec trackpad, sur portables Windows tactiles ; impossible à forcer par le réglage | Jamais pour du nouveau code |
| Un `window.resize` de plus par composant | Composant autonome | Mesures incohérentes entre composants pendant une rotation iOS | Jamais dans le plateau |
| Tester la tablette en 1180 x 820 sans `hasTouch` | Projet existant réutilisé | Aucun chemin tactile n'est exercé | Seulement pour les captures de référence visuelles |
| `user-select: none` sur `body` | Plus de loupe nulle part | Champs et journal bloqués | Jamais |

## Intégration avec l'existant

| Point d'intégration | Erreur courante | Approche correcte |
|---------------------|-----------------|-------------------|
| `useModeMobile.ts` (disposition par largeur) | Y ajouter la détection tactile | Garder la disposition seule ; mode de saisie dans un module séparé |
| `telephone.ts` (`installerSuiviDuGeste`, `REQUETE_TELEPHONE`) | Créer un second suivi de geste | Étendre le suivi existant pour mémoriser le `pointerType` |
| `useAppuiLong.ts` / `appui-tactile.ts` | Une troisième implémentation pour la tablette | Réutiliser `APPUI_LONG_MS` et `issueAppui`, comme le prévoit la fiche (« gestes du téléphone réutilisés ») |
| `useEchelle` (`Board.tsx`) | Ajouter des tailles tactiles en px dans la scène | Commandes tactiles hors scène, ou compensées par `--echelle` |
| Runtime `public/js/marvel/` | Le patcher pour le tactile | Interdit (même statut que le moteur) : tout passe par le nouveau code d'affichage |
| `ui-app/board.html` (meta viewport) | Ajouter `viewport-fit=cover` en passant | Étape dédiée avec audit des marges en paysage |

## Pièges de performance

| Piège | Symptôme | Prévention | Quand ça casse |
|-------|----------|------------|----------------|
| Recalcul d'échelle à chaque variation de `dvh` | Table qui tremble au défilement | Document non défilant, `svh` pour l'échelle | Dès que la page défile sur iPhone |
| Scans pleine définition sur iPad | Onglet rechargé par Safari (« un problème est survenu ») en pleine partie | Images à la taille affichée, chargement paresseux (déjà prévu pour le téléphone, à étendre à la tablette) ; confiance BASSE sur le seuil mémoire | Grosses tables, multijoueur, longues parties |
| Sept écouteurs `resize` qui mesurent tous | Saccade à la rotation | Source de géométrie unique (piège 3) | À chaque rotation |

## Sécurité

Rien de propre à ce jalon au-delà de l'existant (jeu servi par le serveur du projet, pas de nouvelle donnée sensible). Seul point : le panneau de diagnostic d'écran (piège 3) ne doit envoyer que des dimensions et des capacités, aucun identifiant.

## Pièges d'expérience joueur

| Piège | Impact | Mieux |
|-------|--------|-------|
| Toucher deux fois pour agir (piège 1) | Sentiment que « le tactile n'est pas terrible » (retour exact du joueur iPad) | Survol réservé à `pointerType === 'mouse'` |
| Fermer un aperçu déclenche une action (piège 2) | Action non voulue, partie faussée | Le toucher de fermeture ne fait rien d'autre |
| Réglage visible mais sans effet (piège 14, retour n° 5) | Perte de confiance dans les réglages | Masquer ce que l'appareil ne sait pas faire |
| Rotation qui perd la carte agrandie | Lecture interrompue | Conserver ou refermer explicitement l'état à la rotation |

## « Ça a l'air fini mais ça ne l'est pas »

- [ ] **Détection tactile :** vérifier sur un iPad réel que le mode tactile est actif AVANT le premier toucher (`maxTouchPoints`), puis qu'un trackpad repasse en souris et qu'un toucher revient en tactile sans saut de mise en page.
- [ ] **Aperçu au toucher :** vérifier qu'un seul toucher ouvre aperçu + menu, que toucher ailleurs ferme SANS action en dessous, et que la croix fait 44 px à l'écran (mesure, pas CSS).
- [ ] **44 px :** mesurés par `getBoundingClientRect` sur le plateau PC à l'échelle d'un iPad, portrait et paysage.
- [ ] **Rotation :** 6 rotations de suite, puis main entièrement touchable (`elementFromPoint`), aucun élément fixe sur la main.
- [ ] **Réglages téléphone :** chacun testé dans chaque orientation conservée ; aucun réglage affiché sans effet sur iPhone (vibrations).
- [ ] **PC :** comparaison au pixel avant/après à 1366, 1536 et 1920 avec le réglage tactile sur « jamais », et survol souris inchangé.
- [ ] **Champs des menus :** 16 px minimum, bouton visible clavier ouvert sur iPhone réel.

## Rattrapage si un piège passe quand même

| Piège | Coût | Étapes |
|-------|------|--------|
| Survol collant découvert après livraison | FAIBLE | Filtrer `pointerType` au point d'entrée du survol ; le réglage « jamais » sert de contournement immédiat |
| Mise en page fausse après rotation | MOYEN | Panneau de diagnostic chez le joueur, puis source de géométrie unique ; contournement : recharger |
| `viewport-fit=cover` qui casse le paysage | MOYEN | Retirer la clé (retour exact à l'état actuel), puis refaire l'audit des marges |
| Régression PC | FAIBLE à MOYEN | Réglage tactile « jamais » ; comparaison au pixel pour localiser |

## Tests : ce que l'émulation ne voit pas

Constat sur `ui-check/playwright.config.ts` : tous les projets tournent sous Chromium. Le gabarit `tablette` (1180 x 820) est explicitement « souris, sans émulation tactile » : `(pointer: coarse)` et `(hover: none)` n'y sont jamais vrais, donc aucun chemin tactile de la tablette n'est exercé. Seul le projet `s24` (et les fichiers qui posent `test.use({ hasTouch: true })`) émule le toucher.

Pièges et préventions :
1. **`hasTouch` ne fait pas un iPad.** Il bascule `pointer: coarse` / `hover: none` et active `tap()`, mais l'agent utilisateur reste celui de Chromium. Ajouter un projet `tablette-tactile` (1180 x 820 et 820 x 1180, `hasTouch`, `isMobile`, agent utilisateur de Mac comme l'iPad réel) et forcer `navigator.maxTouchPoints` par `addInitScript` (la valeur exposée par l'émulation n'a pas été vérifiée, confiance BASSE).
2. **`click()` reste un clic souris même avec `hasTouch`.** Les tests tactiles utilisent `locator.tap()`. Les fichiers téléphone le font déjà (`tap(` présent dans `plateau-telephone.spec.ts`, `pages-telephone.spec.ts`...).
3. **Les gestes longs n'ont pas d'API.** La documentation Playwright n'offre que `tap` ; le pan et le pincement passent par `dispatchEvent` de `TouchEvent` non fiables (`isTrusted` faux), qui ne génèrent PAS d'événements de pointeur. Or `useAppuiLong` écoute des événements de pointeur. Pour l'appui long et le glisser : soit `PointerEvent` synthétiques avec `pointerType: 'touch'`, soit `Input.dispatchTouchEvent` via CDP (Chromium seulement). Le choisir une fois, dans un utilitaire partagé.
4. **Le WebKit de Playwright n'est pas Safari iOS**, encore moins sous Windows : pas d'heuristique de changement de contenu (piège 1), pas de barre d'adresse ni de barre flottante (piège 7), `svh = lvh = dvh`, zones sûres à 0, rotation instantanée sans valeurs intermédiaires (piège 3), pas de clavier (piège 13), pas de bulle d'appui long (piège 8). Ajouter un projet WebKit n'apporte donc que les différences de rendu CSS, pas les pièges de ce jalon.
5. **`setViewportSize` n'est pas une rotation** : il émet `resize` et change `(orientation)`, mais pas `screen.orientation` ni la taille de l'écran. Un code qui lit `screen.*` passe en test et échoue sur appareil.
6. **Conséquence :** chaque phase se termine par une courte liste de contrôle sur appareil réel (iPhone de Raven, un iPad), centrée sur les pièges 1, 2, 3, 7, 8, 13. Sans Mac, l'inspecteur web distant de Safari n'est pas disponible : prévoir le panneau de diagnostic d'écran (dimensions, `visualViewport`, `--echelle`, mode rendu, mode de saisie, `maxTouchPoints`) consultable par le joueur et joignable au signalement (`PanneauBug`).

Rappel d'environnement : Playwright tourne sous Node Windows depuis WSL, les variables passent par `WSLENV` ; un harnais qui ouvre Chrome doit effacer son `--user-data-dir`.

## Correspondance pièges / phases

| Piège | Phase de prévention | Vérification |
|-------|---------------------|--------------|
| 1 Survol au toucher | Tablette T1 | Test `tap` : menu ouvert, pas d'aperçu collé après 500 ms ; iPad réel : un seul toucher suffit |
| 2 Fermeture traversante | Tablette T1, Téléphone plateau | Test : toucher le voile au-dessus d'une carte jouable ne l'active pas |
| 3 Rotation et mesures | Orientation, Tests | 6 rotations puis `elementFromPoint` sur la main ; diagnostic chez Raven |
| 4 iPad mal classé | Tablette T1, Orientation | Projet `tablette-tactile` avec agent Mac ; décision écrite pour iPad mini et Split View |
| 5 Saut de mise en page | Tablette T1 | Test alternant souris et toucher, position du bouton inchangée pendant le geste |
| 6 44 px dans la scène | Tablette T2 | Mesure à l'écran, plateau PC à l'échelle iPad |
| 7 Hauteur et zones sûres | Téléphone plateau, menus | iPhone réel : bas visible, rien sous la barre ; plus de `100vh` dans le plateau |
| 8 Appui long iOS | Tablette, Téléphone plateau | iPhone et iPad réels : ni bulle, ni loupe, ni image soulevée |
| 9 Double déclenchement | Tablette, Téléphone plateau | Test : un appui long = une action |
| 10 Zoom | Tablette T1 | Double toucher rapide sur un compteur : +2, pas de zoom |
| 11 Élastique | Téléphone plateau | Le document ne défile pas pendant une partie |
| 12 Régressions PC | Tablette, Tests | Comparaison au pixel PC avec réglage « jamais » |
| 13 Clavier | Téléphone menus | iPhone réel, connexion et recherche |
| 14 API absentes | Téléphone plateau, menus | Aucun réglage sans effet sur iPhone |
| 15 Deux orientations | Orientation | Matrice réglages x orientations dans les tests |

## Sources

- WebKit, « More Responsive Tapping on iOS » (`touch-action: manipulation`, délai du clic) : https://webkit.org/blog/5610/more-responsive-tapping-on-ios/ (HAUTE)
- WebKit, « New WebKit Features in Safari 15.4 » (unités `svh`, `lvh`, `dvh`) : https://webkit.org/blog/12445/new-webkit-features-in-safari-15-4/ (HAUTE)
- MDN, `touch-action` : https://developer.mozilla.org/Web/CSS/touch-action (HAUTE)
- Apple, Safari Web Content Guide, « Handling Events » (séquence d'événements souris au toucher, changement de contenu) : https://developer.apple.com/library/archive/documentation/AppleApplications/Reference/SafariWebContent/HandlingEvents/HandlingEvents.html (HAUTE, document ancien mais comportement toujours observé)
- Retours de terrain sur le clic avalé après révélation au survol (seuil d'environ 400 ms) : https://github.com/kirodotdev/KiroCrew/pull/17366 et https://humanwhocodes.com/blog/2012/07/05/ios-has-a-hover-problem/ (MOYENNE)
- WebKit bug 170595 (dimensions fausses pendant la rotation) : https://bugs.webkit.org/show_bug.cgi?id=170595 (MOYENNE)
- WebKit bug 297779 et forum Apple (iOS 26, éléments fixes et viewport visuel après le clavier) : https://bugs.webkit.org/show_bug.cgi?id=297779 , https://developer.apple.com/forums/thread/800125 (MOYENNE)
- Safari 26 et la barre « Liquid Glass » (teinte, `theme-color` ignoré, fond de racine) : https://1ar.io/updates/safari-26-liquid-glass-web/ (BASSE à MOYENNE, source unique)
- iPad qui se déclare Mac, `maxTouchPoints` : https://developer.apple.com/forums/thread/119186 (MOYENNE)
- Vibration absente de Safari : https://caniuse.com/mdn-api_navigator_vibrate (HAUTE)
- `ScreenOrientation.lock` absent d'iOS : https://caniuse.com/mdn-api_screenorientation_lock (HAUTE)
- `interactive-widget` et clavier sur iOS : https://github.com/bramus/viewport-resize-behavior/blob/main/explainer.md , https://www.htmhell.dev/adventcalendar/2024/4/ (MOYENNE)
- Playwright, émulation et événements tactiles : https://playwright.dev/docs/emulation , https://playwright.dev/docs/touch-events (HAUTE pour ce qui y est écrit ; l'effet de `hasTouch` sur `pointer`/`hover` vient de sources secondaires, MOYENNE)
- Limites de l'émulation WebKit contre Safari mobile : https://firm86.com/blog/playwright-mobile-emulation.html (BASSE à MOYENNE)

---
*Recherche des pièges pour : v1.1 Tablette et téléphone*
*Recherché le : 13/10/2026*
