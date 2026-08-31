# Pitfalls Research

**Domain:** Refonte UI/UX complète d'un client de jeu de cartes fonctionnel (moteur figé, frontend vanilla, serveur local, dev solo)
**Researched:** 2026-07-28
**Confidence:** HIGH sur les pièges spécifiques au codebase (vérifiés par lecture de source et mesures), MEDIUM sur les pièges de méthode (littérature 2026 + précédents du domaine)

## Méthode et périmètre

Chaque piège ci-dessous a été soit vérifié dans le code réel (`~/marvel-work/fusion/marvel-lcg-src`), soit corroboré par des sources externes datées. Les faits mesurés sont marqués `[MESURÉ]`, les faits lus en source `[SOURCE]`, les inférences de méthode `[LITTÉRATURE]`.

**Trois constats préalables qui invalident des hypothèses du PROJECT.md.** À traiter avant la construction de la roadmap :

1. **Le plateau n'est pas « pas responsive », il est anti-responsive par construction.** `--scene-width: 1920` / `--scene-height: 1080` avec `camera.style.transform = scale(min(vw/1920, vh/1080))` et **zéro `@media` dans les 59 CSS de `public/css/marvel/`**. Ce n'est pas un manque de media queries, c'est un modèle de layout à taille fixe homothétique. `[SOURCE: css/marvel/marvel.css:60-61, js/marvel/scene.js:38-55]`
2. **L'app n'est pas self-contained aujourd'hui.** `launch.json` configure deux CDN externes (`cerebrodatastorage.blob.core.windows.net`, `marvelcdb.com`) et un second dossier d'images en chemin absolu Windows. Seules **387 des 4317 clés d'image** existent dans `assets/pics/`. Les 3930 autres viennent de `/mnt/c/.../Jeux original/assets/pics/` (4263 fichiers, 349 Mo, hors zip livrable) ou du réseau. `[SOURCE: launch.json, engine/file/cache.py:29-110]` `[MESURÉ]`
3. **Le runtime de partie est du TypeScript compilé dont les sources sont perdues.** 31 des 48 fichiers de `public/js/` portent un `//# sourceMappingURL=X.js.map` orphelin ; aucun `.ts` ni `.js.map` n'existe nulle part sur la machine. Le runtime a exactement le même statut que le moteur Python : code généré, source de vérité perdue. `[MESURÉ]`

---

## Critical Pitfalls

### Pitfall 1 : Le big-bang sur le plateau de jeu (l'écran qui ne shippe jamais)

**What goes wrong:**
La refonte avance bien sur les menus, la préparation, la galerie. Puis vient le plateau : 59 fichiers CSS, 7318 lignes de JS compilé sans sources, un système de coordonnées custom, des animations orchestrées en `setTimeout`. Le réflexe est « on ne peut pas refondre ça par morceaux, il faut le réécrire proprement ». Le chantier démarre, ne converge pas, et le projet se termine avec 4 écrans magnifiques menant à un plateau inchangé. Ce qui est exactement l'inverse de la valeur : le plateau est l'écran où l'utilisateur passe 95 % de son temps.

**Why it happens:**
- Le plateau concentre toute la dette : code généré illisible, timings dupliqués JS/CSS, 165 `!important`, `div > .card:nth-child(N)` généré jusqu'à 99. Il *semble* irréparable par retouches.
- Les écrans faciles sont faits en premier (biais naturel), donc l'énergie et la motivation sont déjà consommées quand arrive le morceau dur.
- 68 à 79 % des projets de modernisation échouent ou sous-performent, principalement par « incomplete system assessment » et boucles de feedback trop longues. `[LITTÉRATURE]`
- Précédent direct du domaine : MTG Arena a été conçu desktop puis « retrofitté » sur téléphone, et « has had issues ever since it released because of that ». `[LITTÉRATURE]`

**How to avoid:**
- **Ne pas mettre le plateau en dernier.** L'attaquer dès qu'un filet de sécurité existe (Pitfall 3), avant la galerie et les decks. Ordonner par valeur/risque, pas par facilité.
- **Découper le plateau en 4 chantiers indépendants et livrables séparément**, chacun ayant sa propre valeur même si les suivants n'arrivent jamais :
  1. **Lecteur de carte** (nouveau composant, autonome, zéro dépendance au layout) → Pitfall 5
  2. **Modèle de layout / caméra** (remplacer l'homothétie 1920x1080) → Pitfall 4
  3. **Interactions tactiles** (hover → tap/long-press) → Pitfall 6
  4. **Habillage visuel** (tokens, couleurs, typo appliqués aux CSS existants)
- Le chantier 1 est un ajout pur : il se branche sur `HoverCard`/`image-preview` sans toucher au reste. C'est le bon premier pas, il livre 80 % de la douleur « lisibilité » pour 10 % du risque.
- **Règle de non-régression du strangler fig :** l'ancien plateau reste la route par défaut ; le nouveau s'active par un flag (`?ui=next` ou une clé localStorage), pas par remplacement de fichier.

**Warning signs:**
- Une tâche « refonte du plateau » sans sous-découpage dans la roadmap.
- Le plateau est planifié après la galerie ou les decks.
- Une session de travail où l'on ouvre `cards.js` (1123 lignes) « pour comprendre avant de commencer » et où rien n'est livré.
- Apparition d'un dossier `public/js/marvel2/` ou `board-new/` qui grossit sans être atteignable depuis l'app.
- Le mot « proprement » dans une description de tâche.

**Phase to address:**
Structure de la roadmap elle-même. Le plateau doit apparaître comme **3 ou 4 phases distinctes** (lecteur de carte, layout, tactile, habillage), la première juste après le filet de sécurité. Jamais comme une phase unique, jamais en dernier.

---

### Pitfall 2 : Le glissement « refonte UI » → « réécriture du runtime »

**What goes wrong:**
En touchant au plateau, on découvre que `public/js/marvel/*.js` est du TS compilé sans sources : `var _a;`, `(_a = class WebSocketHandler {`, `//# sourceMappingURL=` orphelins. La conclusion naturelle est « je ne peux pas travailler là-dedans, je reconstruis les sources TS ». À ce moment, le projet n'est plus une refonte de présentation : c'est une réécriture du client de jeu, avec la même classe de risque que réécrire le moteur, mais **sans le filet de 3766 tests**.

**Why it happens:**
- Le PROJECT.md protège explicitement le moteur Python mais **ne dit rien du runtime JS**, qui a exactement le même statut de code généré à sources perdues. La contrainte est asymétrique par oubli, pas par décision.
- La décision techno annoncée (« moderniser le vanilla vs React+TS+Vite ») rend le glissement légitime : « on migre en TS de toute façon, autant reconstruire ».
- « These attempts to make it better often end up making the project unfinishable. » `[LITTÉRATURE]`

**How to avoid:**
- **Étendre explicitement la contrainte moteur au runtime de partie**, dans PROJECT.md : *« `public/js/marvel/` est du code généré à sources perdues. Les modifications sont chirurgicales et motivées par un besoin UI précis. Toute reconstruction de sources est un projet séparé. »*
- **Tracer la frontière sur les données, pas sur les fichiers.** Le client est un *renderer de snapshot* : le WebSocket ne transporte qu'une notification (`processQueue` fait `pop()` puis `messageQueue.length = 0`, donc les messages intermédiaires sont jetés) et le client refait `fetch('get_world?p=0')`. `[SOURCE: js/marvel/client.js:180, 400-452]` Conséquence exploitable : **une nouvelle UI peut être une fonction pure de `get_world`**, écrite à côté, sans lire le JS existant.
- Marquer les divergences volontaires dans le JS avec la même convention que le moteur (`// CORRECTIF`), pour que la dette reste visible.
- Interdire les refactos opportunistes du JS existant : renommer, réindenter ou « nettoyer » du code tsc n'apporte rien et détruit la comparabilité avec l'original.

**Warning signs:**
- Un `tsconfig.json` apparaît à la racine avec `include: ["public/js/marvel/**"]`.
- Une tâche formulée « reconstruire les types de X » ou « typer le runtime ».
- Un diff qui touche `message.js`, `command.js` ou `client.js` sans qu'aucun bug visuel n'ait été constaté.
- Le mot « pendant qu'on y est » dans une session.

**Phase to address:**
Phase 0 (cadrage) : inscrire la contrainte dans PROJECT.md. Puis critère de Definition of Done de chaque phase plateau : *« aucune modification de la logique de protocole ou d'état »*.

---

### Pitfall 3 : Casser l'app en migrant, sans filet côté frontend

**What goes wrong:**
Le projet a 3766 tests cartes + 4331 tests de génération + un bot autoplay in-process. **Aucun de ces tests ne charge une ligne de HTML/CSS/JS.** `test_autoplay` joue en in-process : il valide le moteur en contournant totalement le client. Le frontend a donc une couverture de zéro, et le seul détecteur de régression est l'œil du développeur sur les écrans qu'il pense à ouvrir. Résultat typique : la refonte du wizard casse silencieusement le champ campaign log de NeXt, découvert trois semaines plus tard en pleine campagne, avec une sauvegarde corrompue.

**Why it happens:**
- La qualité perçue du projet est élevée (3766/0), ce qui crée un faux sentiment de sécurité qui ne s'applique pas au périmètre refondu.
- Écrire des tests frontend paraît disproportionné pour un projet solo, et les tests unitaires de composants sont effectivement de faible valeur ici.
- Le cas critique n'est pas un composant isolé : c'est le **contrat de lancement de partie** (formulaire → payload → moteur), déjà signalé comme non testé et à intégration possiblement incomplète. `[SOURCE: .planning/codebase/CONCERNS.md, recommandation Priority High #1]`

**How to avoid:**
Trois filets, par ordre de rapport valeur/effort. Le premier est non négociable.

**a) Fixtures de snapshot `get_world` + rendu golden (le filet qui colle à cette archi)**
Le client étant un renderer de snapshot complet, capturer des états de jeu réels donne un jeu de fixtures gratuit et exhaustif :
- Ajouter un dump des réponses `get_world` pendant les runs de `test_autoplay` (le bot joue déjà de vraies parties sur 7+ combos).
- Stocker 20 à 40 snapshots couvrant les cas durs : main pleine, encounter deck vide en reshuffle, side scheme, minion attaché, carte tuckée (Photographic Reflexes), mission AoA sur compteur, game over.
- Le nouveau renderer est testé comme fonction pure : snapshot en entrée, DOM/screenshot en sortie, comparaison au golden.
- Bénéfice secondaire : le développement de l'UI ne nécessite plus de lancer une partie pour voir un état rare. C'est le gain de vélocité le plus important du projet.

**b) Screenshots de référence Playwright sur les écrans, capturés AVANT de toucher au CSS**
- Capturer les baselines de `main.html`, `scene.html` (4 étapes), `cards.html`, `deck.html`, `replay.html` et du plateau sur 3 viewports, **sur l'app actuelle, avant la première ligne de refonte**. Une fois le CSS modifié, cette référence est définitivement perdue.
- « Visual regression testing is the safety net that functional tests cannot provide. » Générer les baselines dans un environnement de rendu fixe (image Docker Playwright), masquer tout contenu dynamique (compteurs, timestamps, cartes tirées au hasard) sous peine de flake permanent. `[LITTÉRATURE]`
- Attention : ces baselines servent à protéger les **écrans pas encore refondus** contre les fuites CSS (Pitfall 7), pas à valider les nouveaux écrans. Ne pas les « mettre à jour » par réflexe : une baseline qui bouge sur un écran non touché est exactement le signal recherché.

**c) Un test E2E du contrat de lancement de partie**
Un seul scénario Playwright : ouvrir le wizard, sélectionner héros + scénario + difficulté + campagne, lancer, vérifier que le moteur démarre et que le campaign log contient les clés attendues. C'est le chemin dont la casse est la plus coûteuse (partie de campagne perdue) et le moins détectable à l'œil.

**Warning signs:**
- Toute phase de refonte planifiée avant l'existence des baselines.
- « Je vérifierai à l'œil » dans un critère d'acceptation.
- Un écran non refondu qu'on n'a pas ouvert depuis plus de deux phases.
- Une correction de bug UI qui ne s'accompagne pas d'une fixture reproduisant le bug.

**Phase to address:**
**Phase 0, bloquante.** Aucune phase de refonte ne démarre avant (a) et (b). Node v25.3.0 est disponible localement, l'outillage ne coûte qu'un `npx playwright install`. (c) peut arriver en Phase 1.

---

### Pitfall 4 : Rendre « responsive » une scène homothétique 1920x1080

**What goes wrong:**
Le plateau est une scène virtuelle de 1920x1080 mise à l'échelle uniformément pour tenir dans le viewport (`scale = min(vw/1920, vh/1080)`), avec letterboxing et `rotateX(20deg)`. La police elle-même est mise à l'échelle (`--font-size-out = --font-size * scale`). Ajouter des `@media` par-dessus ne sert à rien : tout est déjà multiplié par un scalaire unique. Le piège est de croire que le travail responsive est un travail CSS, et de découvrir en fin de phase qu'il faut changer le modèle de layout, donc reprendre les positions de toutes les zones.

Chiffres réels, carte de 127x176 px en unités de scène et police de base à 26 px :

| Cible | Viewport CSS | Scale | Largeur carte rendue | Police effective |
|---|---|---|---|---|
| Desktop FHD | 1920 x 937 | 0.87 | 110 px | 22.5 px |
| Laptop 1366 | 1366 x 625 | 0.58 | 74 px | 15.0 px |
| Tablette paysage | 1180 x 820 | 0.61 | 78 px | 16.0 px |
| Tablette portrait | 820 x 1180 | 0.43 | 54 px | 11.1 px |
| Téléphone paysage | 844 x 390 | 0.36 | 46 px | 9.4 px |
| Téléphone portrait | 390 x 844 | **0.20** | **26 px** | **5.3 px** |

En portrait téléphone, le plateau entier occupe une bande de 390 x 219 px au centre de l'écran, et chaque carte fait 26 px de large. `[SOURCE + calcul]`

**Why it happens:**
- L'homothétie « marche » visuellement : rien ne casse, rien ne déborde, tout est proportionné. Le défaut n'est pas un bug de layout, c'est une illisibilité. Donc aucun test de layout ne l'attrape.
- `viewport-fit=cover, maximum-scale=1, user-scalable=0` sur `marvel.html` masque le symptôme en empêchant l'utilisateur de zoomer pour compenser. `[SOURCE: marvel.html:64]`
- Le modèle homothétique est le plus simple à écrire, c'est le choix par défaut de tout portage desktop → mobile, et c'est précisément l'erreur MTG Arena. `[LITTÉRATURE]`

**How to avoid:**
- **Trancher le modèle de layout comme une décision d'architecture explicite, avant tout travail visuel.** Trois options viables, à arbitrer en recherche STACK/ARCHITECTURE :
  1. **Scènes multiples** : plusieurs jeux de `--scene-width/height` et de positions de zones, choisis par breakpoint (ex. 1920x1080 desktop, 1200x1600 tablette portrait, 800x1400 téléphone). Conserve tout le moteur de rendu existant, dont les conversions de coordonnées. Coût : définir 3 layouts de zones.
  2. **Caméra pan/zoom** : la scène reste 1920x1080, l'utilisateur navigue. Rend le plateau utilisable mais l'ergonomie est mauvaise sur un jeu où l'on compare en permanence des zones distantes. Documenté comme mauvais choix pour les jeux de cartes : « zooming in and panning the board would lead to a terrible experience ». `[LITTÉRATURE]`
  3. **Layout en flux** (zones empilées/onglets sur petit écran, plus de scène absolue). La bonne réponse mobile, mais c'est la réécriture du renderer, donc Pitfall 2.

  Recommandation : option 1 pour tablette et desktop, option 3 en vue dédiée pour téléphone, jamais l'option 2 seule.
- **Ne surtout pas retirer l'homothétie sans traiter les consommateurs de coordonnées.** `Scene.scale` alimente `convertScenePosToWindowPos` et `convertWindowPosToScenePos`, utilisés par les flèches de ciblage, le drag, le hover et `move-card.js`. `[SOURCE: js/marvel/scene.js:18-35, move-card.js:22]` Changer le modèle de scène sans ces conversions produit des flèches qui pointent à côté et du drag décalé, symptômes qu'on attribuera à tort au CSS.
- **Pas de phase « responsive » en fin de roadmap.** Chaque phase d'écran a le responsive dans sa Definition of Done. Seul le plateau mérite une phase de layout dédiée, parce que c'est un changement de modèle, pas une adaptation.

**Warning signs:**
- Une tâche « ajouter les media queries au plateau ».
- Une phase « Responsive et tactile » située après les phases d'écran.
- Les flèches de ciblage ou le drag qui se décalent après un changement de layout.
- Un écran validé uniquement en redimensionnant la fenêtre desktop : l'homothétie a l'air correcte à toutes les tailles de fenêtre, ce qui est précisément ce qui rend le défaut invisible.
- Le développeur qui zoome avec Ctrl+molette pour lire pendant un test : il vient de simuler le geste que `user-scalable=0` interdit à l'utilisateur.

**Phase to address:**
Phase dédiée « Modèle de layout du plateau », avec la décision d'architecture posée en amont dans ARCHITECTURE.md. Prérequis : les fixtures `get_world` (Pitfall 3) pour valider les 3 layouts sur les mêmes états.

---

### Pitfall 5 : Croire que zoomer le scan résout la lisibilité (il ne peut pas)

**What goes wrong:**
Le réflexe pour « rendre les cartes lisibles sur mobile » est d'agrandir l'image de la carte. Ça ne peut pas fonctionner avec cette bibliothèque d'assets : **65 % des scans sont en 300x435**. Sur un téléphone à DPR 3, afficher une carte à 300 px CSS demande 900 px de source. On en a 300. Le résultat est un scan flou et un texte de règles illisible, quel que soit le CSS.

Profil réel de la bibliothèque (échantillon de 326 fichiers sur 4263) `[MESURÉ]` :

| Dimensions | Part | Poids typique |
|---|---|---|
| 300 x 435 | 65 % | ~25 Ko |
| 710 x 1030 | 15 % | ~330 Ko |
| 435 x 300 (paysage) | 10 % | ~25 Ko |
| 1030 x 710 (paysage) | 3 % | ~330 Ko |
| autres (450x630, 300x426, 300x300) | 7 % | variable |

Seuils de lisibilité, calculés depuis la carte physique (63,5 mm de large, corps de texte ≈ 2,4 mm, soit 3,8 % de la largeur) :

| Largeur carte rendue | Ce qui est lisible | Source minimale requise (DPR 3) |
|---|---|---|
| ≥ 300 px CSS | texte de règles | 900 px → **seuls les 710x1030 tiennent** |
| 200 à 300 px | nom, coût, stats, traits | 600 à 900 px |
| 120 à 200 px | nom et coût seulement | 360 à 600 px |
| < 120 px | jeton, reconnaissance de l'illustration | — |

Le plateau actuel affiche entre 26 et 110 px selon l'appareil : il est **par conception** en zone jeton, ce qui est cohérent, c'est pour ça que le panneau de preview existe.

**Why it happens:**
- La preview `vh` marche très bien sur desktop et en portrait tablette, ce qui cache le problème pendant tout le développement. `44.45vh` de large donne 416 px sur desktop, 524 px en portrait tablette : parfaitement lisible. `[SOURCE: css/marvel/image-preview.css:7-8]`
- Mais en **paysage téléphone** (390 px de haut), `44.45vh` = **173 px** : le texte de règles n'est plus lisible. Or le letterboxing du Pitfall 4 pousse justement l'utilisateur en paysage.
- Et les tailles sont en `vh`, non en `dvh`/`svh` : **55 occurrences de `vh`, 8 de `vw`, zéro `dvh`/`svh`/`lvh`** dans tout `public/css/`. `[MESURÉ]` Sur mobile, la barre d'URL qui se replie change `vh` et fait sauter/redimensionner la preview en pleine lecture.

**How to avoid:**
- **Rendre le texte de carte en HTML, pas en pixels.** `data/cards.json` contient les données structurées complètes pour **3915 des 4331 cartes** : `name`, `subtitle`, `type`, `traits`, `desc` (HP/ATK/THW/DEF/HS) et `text` avec balisage inline (`"Spider-Sense — <b>Interrupt</b>: When the villain initiates..."`). `[MESURÉ + SOURCE: data/cards.json]` Un lecteur de carte natif donne un texte net à n'importe quelle taille, respecte les réglages d'accessibilité, et se recompose en portrait. Le scan sert d'illustration, pas de support de lecture.
- Le projet a déjà les briques : `public/js/module/card_info.js` et `card_preview.js` sont des modules réutilisables. `[SOURCE: .planning/codebase]` La police d'icônes `ChampionsIcons.ttf` est embarquée. `[SOURCE: css/marvel/marvel.css:73-78]`
- **Prévoir le cas des 416 cartes sans `text`** (4331 - 3915) : fallback sur le scan, avec un indicateur visuel honnête plutôt qu'un panneau vide.
- Convertir tous les `vh` en `dvh` (ou `svh` pour les éléments qui ne doivent jamais grandir). Changement mécanique, gain immédiat sur mobile.
- Cibler **44 px minimum pour les cibles tactiles** (Apple HIG) et ne jamais descendre sous 24 px (WCAG 2.2 niveau AA). `[LITTÉRATURE]`
- Traiter les **cartes paysage** (13 % de la bibliothèque : side schemes, environnements) comme un cas de première classe dans le lecteur : `TryRotateImage` fait déjà de la rotation EXIF côté serveur, ne pas la redoubler côté CSS. `[SOURCE: engine/lib/image_creator.py:19-26]`

**Warning signs:**
- Une tâche « agrandir la preview » ou « améliorer le zoom des cartes ».
- Test de lisibilité fait uniquement sur desktop ou tablette portrait.
- Aucune tâche ne mentionne `cards.json` dans les phases plateau : signe qu'on part sur du bitmap.
- Un scan visiblement flou côté à côté d'un net : les 710x1030 et les 300x435 sont mélangés dans la même grille.
- La preview qui saute de taille au scroll sur téléphone : `vh` non converti.

**Phase to address:**
Phase « Lecteur de carte », **première phase plateau** et candidate à être la première phase de refonte du projet entier. C'est un ajout autonome, à fort impact, à risque quasi nul, et il débloque la lisibilité sur tous les autres écrans (galerie, decks, replay) par réutilisation.

---

### Pitfall 6 : Passer au tactile en gardant une UI pilotée par le hover

**What goes wrong:**
La révélation d'information sur le plateau repose sur le survol : **111 règles `:hover` réparties dans 31 fichiers CSS**, et un `HoverCard` avec temporisation (`setReveal`, `timer_id`, `pause()`). Côté événements, le runtime écoute **7 `click`, 3 `mousemove`, 2 `mouseup`, 1 `mousedown`, et seulement 1 `touchstart` / 1 `touchend`**. `[MESURÉ]` Sur tablette et téléphone, soit l'information ne se révèle jamais, soit elle reste collée (sticky hover), soit le premier tap sert à révéler et le second à agir, ce qui double tous les gestes et rend le jeu épuisant.

**Why it happens:**
- Le développement se fait au clavier/souris. Le hover marche toujours chez le développeur.
- Les navigateurs mobiles émulent le hover au tap pour compatibilité, donc « ça a l'air de marcher » lors d'un test rapide, jusqu'à ce que l'état reste collé.
- Le conflit tap/hover ne se manifeste que dans des enchaînements réels (cibler une carte pendant une fenêtre d'interrupt), pas dans une inspection statique.

**How to avoid:**
- **Séparer les deux intentions** au niveau du modèle d'interaction, pas au niveau du CSS : *inspecter* (lire la carte) et *agir* (jouer, cibler, défendre). Sur pointeur fin : hover = inspecter, clic = agir. Sur pointeur grossier : long-press ou zone dédiée = inspecter, tap = agir. Router via `@media (hover: hover) and (pointer: fine)` et `PointerEvent` plutôt que de dupliquer des handlers `mouse*` et `touch*` (source classique de double-déclenchement).
- **Auditer le drag.** `draggable.js` (349 lignes dans `move-card.js`, 4 lectures de layout dans `draggable.js`) est construit sur `mousedown/mousemove/mouseup`. Sur tactile, un drag non géré devient un scroll de page. Décider explicitement : drag conservé via Pointer Events, ou remplacé par un modèle sélection-puis-cible sur tactile.
- **Ne pas supprimer le hover.** Le desktop est la cible principale et le hover y est le bon geste. L'objectif est l'addition, pas la substitution.
- **Ne pas régler le problème par `user-scalable=0`.** C'est déjà en place et c'est un piège, pas une solution (Pitfall 4).
- Vérifier les 44 px de cible tactile sur les éléments les plus petits du plateau : compteurs de ressources, boutons d'exhaust, icônes de statut (`card-status.css` dimensionne à `--card-width * .5`, soit 13 à 55 px selon l'appareil). `[SOURCE: css/marvel/card-status.css:2-4]`

**Warning signs:**
- Un état visuel qui reste actif après un tap sur tablette.
- Une carte qui demande deux taps pour être jouée.
- Un drag qui scrolle la page.
- Des handlers `touchstart` ajoutés à côté des `mousedown` existants sans `preventDefault` ni déduplication.
- Aucun `@media (hover: hover)` ni `PointerEvent` dans le diff d'une phase tactile.

**Phase to address:**
Phase « Interactions tactiles du plateau », après le modèle de layout (les cibles tactiles dépendent de la taille rendue). À valider sur un vrai appareil, pas dans l'émulation devtools : l'émulation ne reproduit ni le sticky hover ni la latence de long-press.

---

### Pitfall 7 : Cohabitation CSS, et le piège `@layer` + `!important` inversé

**What goes wrong:**
`css/menu/style.css` est chargé par 4 pages (`scene.html`, `cards.html`, `deck.html`, `replay.html`) et contient des sélecteurs à portée globale : `*`, `body`, `button:hover`, `input[type="button"]`, `input[type="file"]`, `textarea:read-only`, plus une série de sélecteurs à ID (`#set-images`, `#encounter-sets`, `#modular-sets`, `#set-content`). `[MESURÉ]` Un nouveau design system ajouté par-dessus se fait donc écraser sur tout ce qui est à base d'ID, et écrase à son tour les 3 pages non encore refondues via les sélecteurs d'élément nus.

Le symptôme est déjà présent : **`wizard.css` contient 67 `!important` sur les 165 de tout l'arbre CSS**, soit 40 % à lui seul. `[MESURÉ]` C'est la trace exacte d'une surcouche qui a gagné par force brute contre les ID de `style.css`. Une troisième couche par-dessus n'a plus de niveau disponible.

**Why it happens:**
- La contrainte du projet (« les écrans actuels restent fonctionnels ») impose mécaniquement la cohabitation, et la solution la plus rapide à chaque conflit est `!important`.
- Le coût est invisible à court terme et paralysant à long terme : le seul recours au-delà de `!important` est `!important` + ID + inline.

**How to avoid:**
- **Isoler par `@layer`, dans cet ordre : `@layer legacy, tokens, base, components, utilities;`** avec `style.css` importé dans `legacy`. L'ordre de couche l'emporte sur la spécificité, donc une classe dans `components` bat `#set-images` dans `legacy` **sans aucun `!important`**. `[LITTÉRATURE, source officielle]`
- **Piège majeur et non intuitif : pour les déclarations `!important`, l'ordre des couches est inversé, et le CSS non layered `!important` bat tout.** `[SOURCE: css-tricks.com/css-cascade-layers, vérifié]` Concrètement :
  - Les 67 `!important` de `wizard.css`, s'ils restent hors couche, battront **toutes** les couches, y compris `utilities`.
  - Si on met `wizard.css` dans `legacy` sans purger ses `!important`, ils deviennent **plus forts** que les `!important` des couches supérieures, parce que `legacy` est la couche la plus basse.
  - **Donc : purger les `!important` de `wizard.css` est un prérequis à la mise en place de `@layer`, pas une amélioration ultérieure.** Faire l'inverse aggrave activement la situation. C'est le piège le plus coûteux de cette section, parce que le symptôme (« maintenant c'est encore pire qu'avant ») décourage l'abandon de la bonne approche.
- **Préfixer ou scoper le nouveau design system.** Il n'y a aujourd'hui **aucune collision de nom de classe entre `css/menu/` et `css/marvel/`** `[MESURÉ]`, c'est un acquis à préserver. Attention en particulier à `.card` : `css/marvel/index.css` déclare `div > .card:nth-child(N) { --index: N }` pour N de 1 à 99, un sélecteur de descendance direct extrêmement large. Nommer un composant `.card` dans le design system produira des `--index` fantômes sur des éléments arbitraires. Préfixer (`.mc-card`) ou passer par des custom properties scopées.
- **Nettoyer les 5 doublons de déclaration** au passage, dont `--anime-shuffle-time` déclaré deux fois dans le même bloc `:root`. `[SOURCE: css/marvel/marvel.css:49-50]` Symptomatique d'accrétion, et source de confusion en debug.
- **Les baselines Playwright du Pitfall 3 sont le détecteur de fuite.** Toute phase qui touche au CSS partagé doit rejouer les baselines des 3 pages non refondues.

**Warning signs:**
- Un `!important` ajouté dans un nouveau fichier CSS. Zéro tolérance dans le code neuf.
- Un sélecteur d'élément nu (`button`, `input`, `div`) dans un nouveau fichier CSS.
- Un écran non refondu dont l'apparence change dans un diff qui ne le mentionne pas.
- `@layer` introduit avant la purge des `!important` de `wizard.css`.
- Un `.card`, `.button`, `.info`, `.face` ou `.name` non préfixé dans le design system (tous existent déjà dans `css/marvel/`, 146 classes au total).

**Phase to address:**
Phase 1 « Fondations CSS », immédiatement après le filet de sécurité et **avant tout travail visuel**. Séquence obligatoire : baselines → purge des `!important` de `wizard.css` → `@layer` → tokens. Cette phase ne doit rien changer visuellement : c'est son critère de validation (baselines identiques au pixel).

---

### Pitfall 8 : Le pipeline d'images, et une galerie qui déclenche 3930 téléchargements

**What goes wrong:**
`Cache.LoadImage` cherche l'image dans les `image_folders`, puis, si absente, la **télécharge depuis internet en synchrone** (`requests.get`, timeout 3 s, sur 2 serveurs successifs), puis, en dernier recours, **génère un placeholder PIL et l'écrit sur disque** (`SAVE_EMPTY_IMAGE=True` par défaut). `[SOURCE: engine/file/cache.py:29-110]`

Configuration réelle `[SOURCE: launch.json]` :
```
"image_servers": ["https://cerebrodatastorage.blob.core.windows.net/...", "https://marvelcdb.com/..."]
"image_folders": ["./assets/pics/", "/mnt/c/Users/arnau/Desktop/Marvel LCG/Jeux original/assets/pics/"]
"cache_max_age": 60
```

Ce que ça produit sur une galerie refondue qui affiche le catalogue :
- **4317 clés d'image distinctes, 387 seulement dans `assets/pics/` (9 %).** Les 3930 autres passent par le dossier `/mnt/c` (4263 fichiers, 349 Mo) ou par le réseau. `[MESURÉ]`
- **Le dossier `/mnt/c` est 242x plus lent en `stat()` que ext4** : 1,61 ms par appel contre 0,0067 ms. `[MESURÉ]` `LoadImage` fait jusqu'à 3 `Exists()` par dossier (`.webp`, `.jpg`, `.png`) sur 4 dossiers, donc jusqu'à 12 `stat()` dont 3 à 1,6 ms.
- **Lecture d'un fichier depuis `/mnt/c` : 13,5 ms** pour 25 Ko en moyenne, plus **2,4 ms de décodage PIL** (`TryRotateImage` ouvre chaque image). `[MESURÉ]` Soit ~16 ms par image à froid, dominé par le pont WSL/NTFS. Une grille de 200 vignettes à froid = **~3,2 s de travail serveur**. Le catalogue complet = **~70 s**.
- **`cache_max_age: 60`** : les navigateurs re-demandent les images au bout d'une minute. Le cache mémoire serveur absorbe (voir ci-dessous) mais la latence réseau locale et les 4317 requêtes reviennent.
- **`Cache.cache` est un dict sans éviction** : chaque image servie reste en RAM du process pour toujours. Parcourir tout le catalogue fait monter le process Python de plusieurs centaines de Mo, définitivement.
- **Si le réseau est coupé ou lent** : 2 timeouts de 3 s par carte manquante, puis génération d'un placeholder PIL **écrit sur disque**. `assets/cache/` est vide aujourd'hui : le premier parcours complet du catalogue hors-ligne y écrirait des milliers de faux JPEG, qui seront ensuite servis **en priorité** aux prochains lancements, masquant durablement les vraies images. C'est un empoisonnement de cache silencieux et difficile à diagnostiquer.

**Why it happens:**
- L'app actuelle n'affiche jamais beaucoup de cartes d'un coup ; le problème est latent et se réveille exactement au moment où une refonte ajoute une galerie ou un deck builder attractifs.
- Le PROJECT.md postule « pas de CDN, tout self-contained ». C'est faux dans la configuration réelle, donc le risque n'est pas dans le radar.
- Les 3 comportements de repli (dossier lent, réseau, placeholder) sont invisibles : l'image finit toujours par s'afficher.

**How to avoid:**
- **Gain gratuit à faire en premier : convertir en WebP.** `try_load_image_path` teste `.webp` **avant** `.jpg` et `.png`. `[SOURCE: engine/file/cache.py:39]` Déposer les `.webp` à côté des `.jpg` suffit, **zéro ligne de code**. Sur 349 Mo à ~65 % de compression, on passe sous 120 Mo, avec un décodage plus rapide. À faire avant toute mesure de performance, sinon tous les chiffres ultérieurs sont pollués. Note : la réponse HTTP annonce `content_type='image/jpeg'` même pour du WebP `[SOURCE: server_files.py:21,28]` ; les navigateurs sniffent le format dans un `<img>` donc ça fonctionne, mais ne pas construire de logique côté client sur le `Content-Type`.
- **Rapatrier les images dans un seul dossier sur ext4** et sortir le chemin `/mnt/c` absolu de `launch.json`. Ce chemin rend en plus le zip livrable non reproductible sur une autre machine.
- **Décider explicitement de la politique réseau.** Pour respecter la contrainte self-contained : vider `image_servers` et pré-remplir le cache par un script de préchauffage hors ligne, plutôt que de laisser des `requests.get` synchrones dans le chemin de rendu.
- **Mettre `save_empty_image` à `false`** pendant toute la refonte, pour éviter l'empoisonnement de `assets/cache/`. Sinon, prévoir une procédure de purge documentée.
- **Générer un vrai jeu de vignettes** (ex. 150 px de large) pour les grilles, servi sur une clé distincte du scan pleine taille. Servir un 710x1030 de 330 Ko dans une vignette de 100 px est le gaspillage dominant sur les 15 % de cartes haute résolution.
- **Lazy-loading fait correctement** : `loading="lazy"` **plus** `decoding="async"` (le décodage près du paint provoque des saccades visibles dans les grilles défilantes, même en lazy), **plus** `width`/`height` ou `aspect-ratio` explicites pour éviter le layout shift. Le placeholder doit avoir exactement le bon ratio : « if the placeholder and final image frame differ, users perceive the swap as instability even if layout shift metrics look acceptable ». `[LITTÉRATURE]` Ici le ratio varie (portrait 0,69 vs paysage 1,45), donc le ratio doit venir du type de carte, pas d'une constante.
- **Borner le cache serveur** (LRU) ou l'accepter consciemment et documenter la consommation RAM attendue.

**Warning signs:**
- Une galerie qui met plusieurs secondes à se peupler au premier affichage, et redevient instantanée ensuite : c'est le chemin à froid.
- Le process Python qui grossit de façon monotone.
- Des cartes affichant un placeholder « no image » alors que le fichier existe : `assets/cache/` empoisonné.
- Des requêtes sortantes vers `marvelcdb.com` dans les logs pendant un test hors-ligne.
- Un onglet réseau devtools montrant 200+ requêtes d'images sur un affichage d'écran.
- Des mesures de performance faites avant la conversion WebP.

**Phase to address:**
Phase 1 « Fondations et pipeline d'assets », en parallèle des fondations CSS. La conversion WebP et le rapatriement du dossier sont des tâches courtes à très fort effet de levier, prérequis de la phase Galerie et de toute mesure de performance ultérieure.

---

### Pitfall 9 : Sur-animer, et re-rendre tout l'état à chaque message

**What goes wrong:**
Deux mécanismes se combinent mal.

**a) Le client est un renderer d'état complet, pas un applicateur d'événements.** `processQueue` fait `pop()` sur la file WebSocket puis `messageQueue.length = 0` : seul le dernier message est traité, les intermédiaires sont jetés, et le client refait un `fetch('get_world?p=0')`. `[SOURCE: js/marvel/client.js:400-452, 180]` Si la nouvelle UI reconstruit naïvement le DOM à chaque notification, chaque action de jeu détruit et recrée des centaines de nœuds de cartes, avec re-décodage des images et reflow complet. Sur tablette d'entrée de gamme, c'est plusieurs centaines de ms par action.

**b) Les animations dépendent d'états intermédiaires qui n'arrivent pas toujours.** Comme les messages sont coalescés, une animation calculée sur un diff se désynchronise dès que le moteur envoie deux notifications rapprochées. Symptôme : cartes fantômes, cartes qui restent en vol, compteurs qui affichent une valeur périmée.

Amplificateurs présents dans le code :
- **Deux systèmes de timing parallèles.** `UI.anime_time` côté JS pilote des `setTimeout` (`UI.anime_time * timeout * .5`, `CardAnimation.anime_start_time = 240`, `has_max_anime_time = 240`, `timeout = 1500` en dur) **et** écrit les custom properties via `document.body.style.setProperty('--anime-time', ...)`. `[SOURCE: js/marvel/ui.js:297-298, 331-342, card_animation.js:93,384,410, move-card.js:244]` Conséquence directe : **modifier `--anime-time` dans une feuille de style ne produit aucun effet**, parce qu'un style inline sur `body` posé au runtime gagne toujours. Et si on modifie la valeur JS, les `setTimeout` et les transitions CSS se désaccordent, produisant des cartes fantômes. C'est un piège à haute probabilité, parce que « rendre les animations plus nerveuses » est une tâche évidente de refonte.
- **23 lectures de layout** (`getBoundingClientRect`, `offsetWidth`, `getComputedStyle`) contre seulement 8 `requestAnimationFrame` et 18 `setTimeout`. `[MESURÉ]` Alternance lecture/écriture non batchée = layout thrashing. « Batch all reads before writes to fix it. » `[LITTÉRATURE]`
- **`ui.js:438` fait `document.querySelectorAll('.card')` et itère sur toutes les cartes** avec écriture par nœud. `[SOURCE]` Avec des piles de deck rendues en nœuds réels (les sélecteurs `nth-child` montent jusqu'à 99), on parle de 150 à 250 nœuds `.card`, chacun avec ses sous-éléments (`.face`, `.info`, `.image`, `.status`, `.cost`).
- **Animations sur propriétés non compositées** : `transition: .15s linear left`, `transition: height 300ms`, `transition: var(--anime-move-time) linear width`. `[SOURCE: side-bar.css:16, notification.css:23, target-arrow.css:11, top-bar.css:40]` Chaque frame déclenche un layout au lieu de rester sur le compositeur.
- **142 `text-shadow`, 26 `box-shadow`, 12 `filter`, 91 `transform`, 69 `opacity`, 4 `will-change`.** `[MESURÉ]` Les `text-shadow` et `filter` sur des éléments animés sont les plus coûteux sur GPU mobile.
- **Aucun `prefers-reduced-motion`** : zéro `@media` dans les 59 CSS du plateau. `[MESURÉ]`
- **59 feuilles de style bloquantes** dans `marvel.html`. Négligeable en localhost sur PC, mesurable sur téléphone via WiFi.

**Why it happens:**
- Les animations sont la partie gratifiante d'une refonte, et le développeur teste sur la machine la plus rapide dont il dispose.
- Le curseur `anime_time` existant permet au développeur de baisser les animations pour aller vite, ce qui masque les problèmes de timing pendant tout le développement.
- Le coût de re-rendu ne se manifeste qu'à état de jeu chargé (fin de partie, gros plateau), c'est-à-dire jamais pendant les tests courts.

**How to avoid:**
- **Réconciliation par clé, jamais de reconstruction.** Chaque carte du snapshot a un `card_id` stable : conserver l'identité du nœud DOM et ne muter que ce qui change. C'est la contrainte d'architecture la plus importante pour la nouvelle UI, à poser dans ARCHITECTURE.md avant d'écrire du code.
- **Une seule source de vérité pour les timings.** Le JS pose les custom properties, le CSS les consomme, et les `setTimeout` sont dérivés de la même valeur (idéalement remplacés par `transitionend`/`animationend`). Interdire tout nombre de millisecondes en dur dans le code neuf.
- **Batcher lectures puis écritures**, mesures dans `requestAnimationFrame`, éviter `querySelectorAll` global suivi d'écritures par nœud. Préférer la délégation d'événements à l'attachement par carte.
- **N'animer que `transform` et `opacity`.** Remplacer les transitions sur `left`, `width`, `height`, `top`.
- **Implémenter `prefers-reduced-motion`** et le câbler sur le réglage existant. `disable-animation.css` existe déjà, il suffit de l'activer aussi par media query.
- **Fixer un budget de performance mesurable** et le tester sur l'appareil le plus faible de la cible, avec un snapshot d'état lourd (fin de partie, plateau chargé) issu des fixtures. Sans fixtures, ce test est trop coûteux à reproduire et ne sera jamais fait.
- **Réduire le nombre de nœuds pour les piles** : une pile de 50 cartes n'a besoin que de 3 à 5 nœuds visibles plus un compteur. Gain immédiat sur le nombre total de nœuds et sur le coût des sélecteurs `nth-child`.

**Warning signs:**
- Une modification de `--anime-time` en CSS sans effet visible : le style inline sur `body` gagne, on est dans le piège du double timing.
- Cartes fantômes, cartes bloquées en vol, compteurs périmés après une action.
- Le nombre de nœuds DOM qui augmente au fil d'une partie (fuite de nœuds de cartes non nettoyés).
- Un `setTimeout` avec une constante en dur dans un diff de refonte.
- Une animation ajoutée sans avoir été testée sur téléphone avec un état de jeu chargé.
- Des warnings « Forced reflow » dans la console devtools.

**Phase to address:**
Contraintes d'architecture à poser en Phase 1 (réconciliation par clé, timing unifié, transform/opacity uniquement). Phase dédiée « Performance et animations » après le layout du plateau, avec budget mesuré sur appareil réel. Les animations *nouvelles* ne s'ajoutent qu'après cette phase, jamais pendant les phases de layout.

---

### Pitfall 10 : Le cache HTTP, la porte de version, et la route fourre-tout

**What goes wrong:**
Trois mécanismes du serveur transforment chaque itération de refonte en fausse piste de debug.

**a) Le cache HTTP.** Toute réponse porte `Cache-Control: public, max-age={cache_max_age}`. Le défaut du code est **31536000 (1 an)** ; `launch.json` le ramène à **60 s**. `[SOURCE: engine/network/web_server.py:20,39, launch.json]` Deux dangers distincts : 60 s suffit à faire croire qu'un correctif CSS n'a pas fonctionné (on recharge dans la minute) ; et si `launch.json` est absent ou régénéré côté livrable, on repasse à un an, ce qui rend l'app **non corrigeable** sans purge manuelle du cache.

Symptôme déjà présent : `prepare.html` charge `prepare.css?v=18` et `app.js?v=18`. `[SOURCE]` Le développeur a incrémenté ce numéro 18 fois à la main. C'est le signe qu'il a déjà payé ce piège.

**b) Les images sont mises en cache indépendamment du mode.** `ReadFile` n'applique `HeaderCache` que si `Build.release`, mais les handlers d'images l'appliquent **toujours**. `[SOURCE: server_files.py:21,28 vs web_server.py:155-158]` Conséquence : en dev, remplacer un scan de carte ne se voit pas dans le navigateur. Et comme `RELEASE=1` est obligatoire dans ce projet, le comportement dev diffère du comportement livré pour le CSS/JS mais pas pour les images : deux boucles de feedback incohérentes.

**c) La porte de version et la route fourre-tout.** Chaque requête vérifie le cookie `app_version` contre `Ver.ui_version_str` et, en cas d'écart, sert `clean_cache.html` au lieu de la page demandée. `[SOURCE: web_server.py:80-100]` Or `clean_cache.html` contient un script qui appelle `window.location.reload()` si les versions diffèrent : si le rechargement resert du cache, on obtient une **boucle de rechargement**. Par ailleurs, la dernière route enregistrée est `'/{path:.+}'` → `handle_image_request`, qui prend le **basename** du chemin et répond **toujours `content_type='image/jpeg'`**. `[SOURCE: server_files.py:22-28, 37]` Un nouvel asset placé hors des préfixes servis (un `/assets/fonts/x.woff2`, un `/api/x`) sera donc renvoyé comme une image JPEG, avec un header de cache, et le navigateur mettra en cache cette réponse absurde. Le diagnostic est très trompeur : la requête retourne 200.

**Why it happens:**
- Le cache et la porte de version sont des mécanismes du moteur, hors du périmètre mental « refonte UI ».
- Un `200 OK` fait supposer que le serveur a compris la requête.
- La différence dev/release du cache n'est visible qu'en lisant `ReadFile`.

**How to avoid:**
- **Automatiser le cache-busting.** Le `?v=18` manuel ne tiendra pas sur une refonte complète. Deux options : dériver la query string de `Ver.ui_version_str` (déjà exposé par `/get_version`), ou générer les balises `<link>`/`<script>` avec un hash de contenu. À faire en Phase 0, parce que chaque phase ultérieure paie le coût sinon.
- **Documenter et fixer la valeur de `cache_max_age`** dans le livrable, avec une valeur de dev (0) et une valeur de release, et ne jamais s'appuyer sur le défaut d'un an.
- **Vérifier la table de routage avant d'ajouter un asset ou un endpoint.** Tester explicitement qu'un nouveau chemin ne tombe pas dans le fourre-tout : un `Content-Type: image/jpeg` sur une requête CSS/JS/JSON est la signature du piège.
- **Ajouter les nouveaux écrans en respectant les préfixes servis** (`/public/...`), comme le fait déjà `prepare.html`.
- Considérer la porte de version comme un actif : elle protège les utilisateurs du cache périmé. Ne pas la contourner, l'utiliser (bumper la version fait partie du rituel de livraison, déjà présent : re-zip + relance + non-régression).

**Warning signs:**
- Une modification CSS ou JS sans effet, résolue par un hard refresh. Symptôme numéro un.
- Un `?v=` incrémenté à la main dans un diff.
- Une page qui recharge en boucle : conflit porte de version / cache.
- `Content-Type: image/jpeg` sur une réponse qui n'est pas une image.
- Un nouveau fichier statique qui « ne se charge pas » alors que le serveur répond 200.
- Un scan de carte remplacé mais toujours affiché à l'ancienne.

**Phase to address:**
Phase 0 « Boucle de dev », en même temps que le filet de sécurité. Le cache-busting automatique et une commande de reload propre sont un multiplicateur de vélocité sur toutes les phases suivantes.

---

### Pitfall 11 : Design-system-first, la paralysie ; screens-first, la dérive

**What goes wrong:**
Deux échecs symétriques.

**Design-system-first** : on commence par les tokens, la palette, l'échelle typographique, la grille, la bibliothèque de composants. Trois semaines plus tard il existe un design system complet et aucun écran refondu. Puis le premier écran réel révèle que les composants ne correspondent pas aux besoins (une « carte » de jeu de cartes n'est pas une « card » de design system, un plateau n'a pas de grille, un wizard a des états que le système n'a pas prévus), et le système est retravaillé. « A classic case of premature optimization is when a well-meaning founder orders a huge design system built... it's backwards. Far better if the company built a few digital products first and then figured out what made sense to abstract. » `[LITTÉRATURE]`

**Screens-first** : chaque écran est refondu isolément et « beau », mais les boutons n'ont pas le même rayon, les espacements dérivent, quatre bleus cohabitent. L'app est un patchwork, ce qui est exactement la douleur exprimée au départ. Le mode d'échec canonique des bibliothèques de composants est la dérive. `[LITTÉRATURE]`

**Why it happens:**
- Le design system est confortable : progrès mesurable, zéro risque de casser quoi que ce soit, aucune décision UX difficile. C'est du perfectionnisme déguisé en méthode.
- Screens-first est confortable aussi : résultat visible immédiatement, gratification rapide.
- Un développeur solo n'a personne pour dire « ça fait dix jours que tu es sur les tokens ».

**How to avoid:**
- **Extraire le design system de deux écrans pilotes, ne pas le déduire.** Séquence : refondre 2 écrans en dur (un simple, un dense), **puis** extraire ce qui se répète en tokens et composants, **puis** appliquer aux suivants. Le système est alors validé par construction.
- **Choisir les pilotes pour leur pouvoir révélateur, pas pour leur facilité.** Recommandation : le **lecteur de carte** (composant le plus dense, le plus réutilisé, contraint par le tactile et le responsive) et **les menus** (`main.html`, le plus simple, pour valider la navigation et les tokens de base). Ces deux écrans couvrent les deux extrêmes de contrainte.
- **Plafonner le design system à ce que 2 écrans ont prouvé nécessaire.** Pas de composant sans deux usages réels. Pas de token sans deux consommateurs.
- **Trancher la direction visuelle une fois, tôt, par écrit** (les 2-3 pistes prévues dans PROJECT.md), avec des maquettes du lecteur de carte et du plateau, pas des palettes abstraites. Une palette hors contexte ne permet pas de décider, et rouvrir la direction visuelle en phase 6 invalide tout le travail antérieur.
- **Verrouiller la direction visuelle comme une décision, pas une préférence.** Dans PROJECT.md, avec la date. La rouvrir doit être un acte explicite et coûteux.

**Warning signs:**
- Plus de 2 jours consécutifs sans qu'un écran atteignable par l'utilisateur n'ait changé.
- Un composant du design system sans consommateur.
- Une quatrième variante de bouton.
- Le mot « refondre la palette » après la phase 2.
- Des maquettes qui ne montrent jamais le plateau ni une carte réelle : la partie difficile est évitée.

**Phase to address:**
Ordonnancement de la roadmap. Phase 2 « Écrans pilotes » (lecteur de carte + menus), Phase 3 « Extraction du design system ». Jamais un design system en phase 1. La direction visuelle est tranchée en amont, avec des maquettes du plateau et d'une carte.

---

### Pitfall 12 : Dev solo, perfectionnisme, et aucune boucle de feedback

**What goes wrong:**
Le projet est un hobby solo mené avec Claude Code, sur un moteur validé à 3766/0. Ce niveau d'exigence a été atteint parce que le moteur a un **critère objectif** : la carte fait ce que son texte dit, le test passe ou échoue. **L'UI n'a aucun critère objectif.** Transposer la même exigence à un domaine subjectif produit une boucle infinie : chaque écran peut toujours être un peu mieux, aucune définition de « fini » n'existe, et le projet s'arrête d'épuisement à 60 %. Les développeurs solo rapportent un taux horaire effectif 65 % inférieur au devis, principalement à cause du refactoring sans fin. `[LITTÉRATURE]`

Aggravant spécifique : le seul utilisateur est le développeur, donc les préférences personnelles ne sont jamais contredites, et une décision d'ergonomie ratée n'est jamais détectée. Le collaborateur (Claude Code) est structurellement complaisant sur le goût : il ne dira pas « cet écran est confus ».

**Why it happens:**
- Le succès du moteur crée l'attente que la même méthode s'applique. Elle ne s'applique pas.
- L'itération visuelle est plaisante et sans risque, contrairement au chantier plateau.
- « Coding sessions get derailed by noticed design flaws » : chaque session découvre trois imperfections adjacentes. `[LITTÉRATURE]`
- Aucun coût externe au retard : rien ne force à livrer.

**How to avoid:**
- **Écrire les critères d'acceptation avant de commencer chaque phase, en termes observables**, pas esthétiques. Bons critères : « le texte de règles est lisible sans zoom sur téléphone en portrait », « lancer une partie de campagne NeXt depuis mobile en moins de 6 taps », « aucune baseline des écrans non refondus n'a bougé », « 60 fps sur tablette avec un plateau de fin de partie ». Mauvais critère : « l'écran est beau ».
- **Une passe par écran.** La deuxième passe est du backlog, pas de la phase courante. Le journal de session sert d'exutoire aux imperfections repérées, ce qui permet de ne pas les traiter tout de suite sans les perdre.
- **Jouer une partie complète après chaque phase.** C'est la seule boucle de feedback disponible, et c'est une bonne : une vraie partie révèle plus de problèmes d'ergonomie qu'une heure d'inspection. Sur l'appareil le plus contraint, pas sur le PC.
- **Faire tester par une personne extérieure au moins une fois**, sur le lancement de partie et une manche de jeu, sans aide. Un seul testeur naïf sur 20 minutes vaut plus que dix itérations solo. Communauté Marvel Champions ou n'importe quel proche : l'objet n'est pas l'avis esthétique mais l'observation de là où la personne bloque.
- **Rendre le progrès visible** : le nombre d'écrans refondus et atteignables est la seule métrique qui compte. Un design system à 80 % vaut zéro.
- **Utiliser la contrainte de livraison déjà en place** (re-zip vers `Fusion/`, relance serveur, autoplay 0 traceback) comme rythme imposé de fin de phase. Elle existe, elle force à atteindre un état cohérent.

**Warning signs:**
- Une phase qui dépasse le double de son estimation sans qu'un blocage technique ait été identifié.
- Retour sur un écran déjà marqué fini, hors correction de bug.
- Plus d'une semaine sans avoir joué une vraie partie sur l'app.
- Aucun critère d'acceptation observable dans la description d'une phase.
- Le journal de session qui ne fait que reformuler « continuer la refonte de X ».
- Aucune ligne de backlog : signe que les imperfections sont traitées au lieu d'être notées.

**Phase to address:**
Gouvernance de la roadmap : critères d'acceptation observables par phase, une seule passe par écran, partie complète jouée en fin de phase comme critère de sortie. Un test externe planifié après la phase Préparation de partie et après la phase Lecteur de carte.

---

## Technical Debt Patterns

| Shortcut | Immediate Benefit | Long-term Cost | When Acceptable |
|----------|-------------------|----------------|-----------------|
| `!important` pour battre `style.css` | Conflit réglé en 10 s | Rend `@layer` contre-productif (ordre inversé pour `!important`), plus aucun niveau disponible pour une 3e couche | **Jamais** dans du CSS neuf. Les 67 existants dans `wizard.css` sont à purger, pas à imiter |
| `?v=N` incrémenté à la main | Contourne le cache tout de suite | Oubli garanti sur une refonte multi-fichiers, debug de « correctif sans effet » à répétition | Uniquement jusqu'à l'automatisation en Phase 0 |
| Reconstruire le DOM entier à chaque snapshot | Rendu trivialement correct, zéro bug de réconciliation | Inutilisable sur tablette d'entrée de gamme, re-décodage d'images, perte des états CSS transitoires | Acceptable sur un écran statique (galerie), jamais sur le plateau |
| Garder l'homothétie 1920x1080 sur mobile | Rien à faire, ça « tient » à l'écran | Cartes à 26 px, texte à 5 px : l'objectif mobile du projet n'est pas atteint | Acceptable en desktop et tablette paysage. Jamais en portrait téléphone |
| `setTimeout` en dur pour séquencer une animation | Marche du premier coup sur la machine du dev | Désynchronisation dès que les timings CSS changent ou que l'appareil ralentit : cartes fantômes | Jamais dans du code neuf. Utiliser `transitionend`/`animationend` |
| Laisser `image_servers` peuplé | Toutes les images finissent par s'afficher | Contredit la contrainte self-contained, 2 timeouts de 3 s par carte hors-ligne, empoisonnement de `assets/cache/` | Acceptable comme filet pendant le développement, à vider pour le livrable |
| Servir les scans pleine taille dans les grilles | Un seul jeu d'assets à gérer | 330 Ko par vignette sur les 15 % haute résolution, décodage inutile | Acceptable jusqu'à la phase Galerie, à corriger avant |
| Garder les scans 300x435 comme support de lecture | Aucun travail d'asset | Texte de règles définitivement illisible sur mobile pour 65 % des cartes | Jamais. Le lecteur HTML depuis `cards.json` est la sortie |
| Refondre un écran sans baseline préalable | Une étape de moins avant le plaisir | Les fuites CSS sur les 3 autres pages deviennent indétectables, et la référence est perdue à jamais | Jamais |
| Le nouveau plateau remplace l'ancien fichier | Pas de flag à gérer | Viole la contrainte « le jeu reste jouable », plus de rollback | Jamais avant que le nouveau ne soit validé sur une partie complète |

## Integration Gotchas

Le projet a peu de dépendances externes, mais les points de couplage internes se comportent comme des intégrations.

| Integration | Common Mistake | Correct Approach |
|-------------|----------------|------------------|
| `get_world` (snapshot d'état) | Traiter le WebSocket comme un flux d'événements et animer les diffs | Le WS est une notification ; `processQueue` jette les messages intermédiaires. Refetch + réconciliation par clé sur le snapshot complet |
| Endpoints `/list_*`, `/get_*` | Les supposer stables et non documentés, les redécouvrir à chaque écran | Écrire une couche d'accès unique et typée (le `api.js` de `public/js/prepare/` est le bon précédent) et l'utiliser partout |
| Route fourre-tout `/{path:.+}` | Ajouter un asset ou un endpoint hors préfixe servi et obtenir un 200 en `image/jpeg` | Vérifier le `Content-Type` de toute nouvelle URL. Rester sous `/public/...` |
| `Cache.LoadImage` | Supposer que toutes les images sont locales | 91 % des clés ne sont pas dans `assets/pics/`. Repli sur `/mnt/c` (242x plus lent en stat) puis sur 2 CDN, puis génération d'un placeholder persisté |
| Porte de version (cookie `app_version`) | Bidouiller le cookie pour éviter `clean_cache.html` | Bumper `Ver.ui_version_str` fait partie du rituel de livraison. Le contournement produit des boucles de rechargement |
| Formulaires campaign log → moteur | Refondre la présentation du wizard sans revalider le payload | Intégration déjà signalée comme possiblement incomplète (MTS/MG/NeXt/AoA). Un E2E sur le contrat de lancement avant de toucher au wizard |
| `ChampionsIcons.ttf` | Réintroduire les icônes en SVG ou en emoji dans le design system | La police d'icônes est embarquée et cohérente avec le jeu. La conserver comme token de typographie |
| Checksums `data/*.json` | Lire `cards.json` côté frontend et le réécrire pour un besoin UI | Lecture seule. Toute écriture invalide le checksum et empêche le jeu de démarrer |

## Performance Traps

| Trap | Symptoms | Prevention | When It Breaks |
|------|----------|------------|----------------|
| Reconstruction complète du DOM à chaque snapshot | Saccade à chaque action, images qui re-flashent | Réconciliation par clé sur `card_id` | Dès ~150 nœuds `.card`, soit un plateau de milieu de partie sur tablette |
| Piles de deck rendues en nœuds réels | Compte de nœuds qui grimpe, sélecteurs `nth-child` jusqu'à 99 | 3 à 5 nœuds visibles par pile + compteur | Deck joueur 40-50 + encounter 30-40 + défausses = 150 à 250 nœuds |
| Layout thrashing | Warnings « Forced reflow », frames à 30+ ms | Batcher lectures puis écritures, mesures en rAF | 23 lectures de layout pour 8 rAF : déjà présent, s'aggrave à chaque nœud ajouté |
| Transitions sur `left`/`width`/`height` | Animations qui saccadent alors que le CPU n'est pas saturé | Uniquement `transform` et `opacity` | Visible dès l'entrée de gamme mobile, invisible sur desktop |
| `text-shadow` et `filter` sur éléments animés | Chute de framerate pendant les animations sur mobile | Limiter aux éléments statiques, sinon pré-composer | 142 `text-shadow` et 12 `filter` présents : critique si l'un se retrouve sur une carte animée |
| Grille du catalogue à froid | Plusieurs secondes de vide, puis instantané aux visites suivantes | Vignettes dédiées, WebP, dossier sur ext4, préchauffage du cache | 200 vignettes ≈ 3,2 s ; le catalogue complet ≈ 70 s `[MESURÉ]` |
| `Cache.cache` sans éviction | RAM du process qui monte de façon monotone et ne redescend jamais | Cache LRU borné, ou consommation documentée et assumée | Parcours du catalogue : plusieurs centaines de Mo résidents |
| `cache_max_age: 60` sur les images | Ré-téléchargement de toutes les images chaque minute | Cache long sur les images (immuables) + cache-busting par version sur le CSS/JS (mutables) | Sur téléphone via WiFi, sur un écran affichant beaucoup de cartes |
| 59 feuilles de style bloquantes | Flash de contenu non stylé, premier rendu lent sur mobile | Regrouper par écran, ou bundler | Négligeable en localhost sur PC, mesurable sur téléphone via WiFi |
| Décodage d'image près du paint | Micro-saccades au scroll d'une grille malgré `loading="lazy"` | Ajouter `decoding="async"` et des dimensions explicites | Grilles défilantes, phase Galerie |

## Security Mistakes

Le jeu est local, non officiel, mono-utilisateur : la surface est étroite, mais trois points méritent attention.

| Mistake | Risk | Prevention |
|---------|------|------------|
| Injecter `card.text` en `innerHTML` sans contrôle | `cards.json` contient du balisage inline (`<b>Interrupt</b>`) et est éditable à la main. Un `<img onerror>` s'exécuterait dans le lecteur de carte. Risque réel faible (données maîtrisées) mais le lecteur de carte va faire exactement cette opération sur 3915 cartes | Sanitizer via une whitelist de balises (`b`, `i`, `em`, `br`, et la police d'icônes), ou parser vers des nœuds construits. Ne jamais `innerHTML` la valeur brute |
| Exposer le serveur au-delà de `127.0.0.1` pour tester sur mobile | `server_addresses` en `0.0.0.0` avec `password: ""` ouvre le contrôle complet du jeu et la lecture de fichiers (`/read_file`) à tout le réseau local | Renseigner `password` avant tout binding non-loopback, ou passer par un tunnel local. Le test mobile est indispensable, la méthode doit être décidée en Phase 0 |
| Traiter les checksums `data/*.json` comme une protection | `CODE_KEY` est extractible du bytecode. Ce n'est pas un mécanisme anti-falsification, uniquement une détection de corruption | Ne pas fonder de logique UI sur la validité d'un checksum. Le recalculer à toute édition de données |
| `/read_file` accessible depuis un nouvel écran | Endpoint générique de lecture de fichier ; un nouvel écran qui le sollicite avec un chemin construit côté client élargit la surface | Passer par des endpoints spécifiques (`/get_card_json`, `/get_replay_json`), pas par `/read_file` paramétré côté client |

## UX Pitfalls

| Pitfall | User Impact | Better Approach |
|---------|-------------|-----------------|
| Le plateau homothétique en portrait téléphone | Cartes à 26 px, texte à 5 px : le jeu est visuellement présent mais injouable | Layout dédié petit écran, ou vue explicitement partielle avec navigation entre zones |
| `user-scalable=0` sur le plateau | L'utilisateur ne peut même pas zoomer pour compenser. On lui retire son seul recours | Fournir un lecteur de carte plein écran, et ne bloquer le zoom qu'une fois ce recours en place |
| Preview de carte en `vh` non `dvh` | Sur mobile, la preview saute et se redimensionne quand la barre d'URL se replie, en pleine lecture | `dvh` pour ce qui doit suivre le viewport, `svh` pour ce qui ne doit jamais grandir |
| Preview ancrée à gauche/droite | Hypothèse desktop paysage. En paysage téléphone, `44.45vh` tombe à 173 px : nom lisible, règles non | Position et taille dépendantes du viewport, plein écran sur petit écran |
| Information révélée uniquement au survol | Sur tactile : soit rien, soit un état collé, soit deux taps par action | Inspecter et agir comme deux gestes distincts, routés par `@media (hover: hover)` |
| Scans mélangés 300x435 et 710x1030 dans une même grille | Certaines cartes nettes, d'autres floues côte à côte : perçu comme un bug | Normaliser à la génération des vignettes, ou afficher les basse-résolution en dessous de leur seuil de flou |
| Cartes paysage traitées comme un cas dégradé | 13 % de la bibliothèque (side schemes, environnements) s'affichent tournées ou rognées | Cas de première classe du lecteur et des grilles, ratio piloté par le type de carte |
| Animations non désactivables ou non respectueuses des préférences système | Nausée, fatigue, temps d'attente forcé sur des parties longues | `prefers-reduced-motion` câblé sur `disable-animation.css`, réglage utilisateur conservé |
| Champs campaign log sans aide contextuelle | Formulaire de bookkeeping AoA/NeXt/MG rempli au hasard : campagne corrompue silencieusement | Aide inline par champ, valeurs prévalidées, récapitulatif avant lancement. Déjà identifié comme manquant |
| Wizard sans état de sortie visible | Sur mobile, wizard long, on ne sait pas combien il reste ni si on peut revenir | Progression persistante, retour non destructif, récapitulatif final (le plan 6 étapes de `Fusion/PREPARE-UI-PLAN.md` le prévoit déjà) |

## "Looks Done But Isn't" Checklist

À vérifier avant de déclarer une phase terminée.

- [ ] **Écran refondu :** souvent oublié, les 3 autres pages partageant `style.css`. Vérifier que les baselines de `cards.html`, `deck.html`, `replay.html`, `scene.html` n'ont pas bougé
- [ ] **Écran refondu :** souvent oublié, le portrait téléphone. Vérifier sur un appareil réel, pas en émulation devtools
- [ ] **Écran refondu :** souvent oublié, les cibles tactiles. Vérifier qu'aucun élément interactif n'est sous 44 px (24 px absolu minimum)
- [ ] **Lecteur de carte :** souvent oublié, les 416 cartes sans champ `text`, et les 13 % de cartes paysage. Vérifier le fallback et l'orientation
- [ ] **Lecteur de carte :** souvent oublié, la sanitization de `card.text`. Vérifier qu'aucun `innerHTML` ne reçoit de valeur brute
- [ ] **Layout du plateau :** souvent oublié, les consommateurs de `Scene.scale`. Vérifier flèches de ciblage, drag, positionnement du hover après tout changement de scène
- [ ] **Animations :** souvent oublié, `prefers-reduced-motion` et la cohérence entre `UI.anime_time` (JS) et `--anime-time` (inline sur `body`). Vérifier qu'aucun `setTimeout` en dur ne subsiste
- [ ] **Animations :** souvent oublié, le test sur un état de jeu chargé. Vérifier avec un snapshot de fin de partie, pas un plateau de début
- [ ] **Galerie / grille :** souvent oublié, le premier affichage à froid et le comportement hors-ligne. Vérifier la durée du premier remplissage et l'absence de placeholders générés
- [ ] **Assets :** souvent oublié, la conversion WebP et le rapatriement hors `/mnt/c`. Vérifier qu'aucun chemin absolu machine-spécifique ne subsiste dans `launch.json`
- [ ] **Nouveau fichier statique :** souvent oublié, la table de routage. Vérifier le `Content-Type` de la réponse (un `image/jpeg` signale le fourre-tout)
- [ ] **CSS neuf :** souvent oublié, l'absence de `!important` et de sélecteur d'élément nu. Vérifier par grep sur le diff
- [ ] **CSS neuf :** souvent oublié, les collisions de noms avec les 146 classes de `css/marvel/`, en particulier `.card`, `.face`, `.info`, `.name`, `.button`
- [ ] **Lancement de partie :** souvent oublié, le payload campaign log des 4 formats. Vérifier qu'une partie de campagne démarre et que le log contient les bonnes clés
- [ ] **Livraison de phase :** souvent oublié, le bump de version UI et le re-zip. Vérifier que le cache ne sert pas l'ancienne version, et que l'autoplay passe à 0 traceback
- [ ] **Livraison de phase :** souvent oublié, jouer une vraie partie complète. Vérifier sur l'appareil le plus contraint de la cible

## Recovery Strategies

| Pitfall | Recovery Cost | Recovery Steps |
|---------|---------------|----------------|
| Big-bang plateau enlisé | HIGH | Geler la branche, ne pas la supprimer. Identifier le sous-ensemble déjà fonctionnel (souvent le lecteur de carte), l'extraire comme ajout autonome derrière un flag, livrer ça. Reprendre le reste en 3 chantiers |
| Glissement vers la réécriture du runtime | HIGH | Revenir au dernier état livré. Reformuler le besoin UI initial et chercher la modification chirurgicale minimale. Si elle n'existe pas, la fonctionnalité sort du périmètre de la refonte |
| Régression découverte tardivement, sans baseline | HIGH | Récupérer l'écran depuis git (ou `scene.html.bak-avant-ui`), capturer la baseline manquante, puis rejouer la refonte. Coût du travail perdu, mais le filet est enfin en place. Évitable au prix d'une heure en Phase 0 |
| Fuite CSS vers un écran non refondu | LOW si baselines présentes, MEDIUM sinon | Le diff visuel localise la règle. Restreindre la portée du sélecteur ou déplacer la règle dans la bonne couche. Ne jamais compenser par un `!important` sur l'écran victime |
| `@layer` posé avant la purge des `!important` | MEDIUM | Ne pas revenir en arrière : la couche est correcte, ce sont les `!important` qui la sabotent. Les purger fichier par fichier en s'appuyant sur les baselines. Le symptôme « c'est pire qu'avant » est attendu et transitoire |
| `assets/cache/` empoisonné par des placeholders | LOW | Vider `assets/cache/`, passer `save_empty_image` à `false`, redémarrer. À documenter comme procédure, sinon le diagnostic prend des heures |
| Plateau injouable en performance sur tablette | MEDIUM | Réactiver le réglage `anime_time`, désactiver les animations, mesurer sur un snapshot lourd, identifier la source (nœuds, thrashing, propriétés animées). Ne pas optimiser au hasard : les fixtures rendent la mesure reproductible |
| Cartes fantômes / animations désynchronisées | MEDIUM | Chercher les `setTimeout` en dur et les écarts avec les valeurs CSS. Remplacer par `transitionend`. Vérifier la coalescence WS (deux notifications rapprochées) |
| Boucle de rechargement `clean_cache.html` | LOW | Bumper la version UI, purger le cache navigateur, vérifier `cache_max_age`. Documenter la procédure une fois pour toutes |
| Perfectionnisme, phase qui ne finit pas | MEDIUM | Écrire les critères d'acceptation observables a posteriori, considérer comme fini tout ce qui les satisfait, basculer le reste en backlog, livrer. Puis jouer une vraie partie |
| Design system construit à vide | MEDIUM | Ne pas le jeter. Refondre 2 écrans en dur avec, puis élaguer tout token et composant sans deux consommateurs réels |

## Pitfall-to-Phase Mapping

Numérotation indicative : ce qui compte est l'ordre relatif et le caractère bloquant de la phase 0.

| Pitfall | Prevention Phase | Verification |
|---------|------------------|--------------|
| 3. Pas de filet frontend | **Phase 0 (bloquante)** | Baselines Playwright des 5 écrans sur 3 viewports committées ; 20+ fixtures `get_world` dumpées depuis `test_autoplay` |
| 10. Cache, version, routage | **Phase 0** | Une modification CSS est visible au simple reload, sans hard refresh ni `?v=` manuel. Un nouveau chemin statique renvoie le bon `Content-Type` |
| 2. Glissement vers la réécriture | **Phase 0** (cadrage) | PROJECT.md étend la contrainte moteur à `public/js/marvel/` ; chaque phase plateau a « aucune modification du protocole » en DoD |
| Test mobile / sécurité réseau | **Phase 0** | Méthode de test sur appareil réel décidée et documentée, avec `password` renseigné si binding non-loopback |
| 7. Cohabitation CSS | **Phase 1** | 0 `!important` dans `wizard.css` ; `@layer legacy, tokens, base, components, utilities` en place ; baselines inchangées au pixel |
| 8. Pipeline d'images | **Phase 1** | WebP déposés, dossier unique sur ext4, aucun chemin absolu machine-spécifique, `save_empty_image: false`, poids total mesuré avant/après |
| 9. Contraintes d'archi (réconciliation, timings) | **Phase 1** (décision) | ARCHITECTURE.md fixe : réconciliation par clé, une seule source de timing, `transform`/`opacity` uniquement |
| 5. Lisibilité des cartes | **Phase 2** (écran pilote) | Texte de règles lisible sans zoom en portrait téléphone, sur un appareil réel, pour une carte dense. `vh` → `dvh`. Fallback des 416 cartes sans `text` |
| 11. Design system | **Phase 2 puis 3** | Phase 2 : 2 écrans pilotes refondus en dur. Phase 3 : tokens et composants extraits, aucun sans 2 consommateurs |
| 12. Perfectionnisme, feedback | **Toutes les phases** (gouvernance) | Critères observables écrits avant démarrage ; une seule passe ; partie complète jouée en sortie ; 1 test externe après phase 2 et après la phase Préparation |
| 1. Big-bang plateau | **Structure de la roadmap** | Le plateau apparaît en 3 ou 4 phases distinctes, la première (lecteur de carte) parmi les toutes premières du projet |
| 4. Layout homothétique | **Phase dédiée « Layout du plateau »** | Les 3 layouts validés sur les mêmes fixtures ; flèches de ciblage et drag corrects sur chacun ; carte ≥ 150 px sur tablette |
| 6. Hover vers tactile | **Phase dédiée « Interactions tactiles »** | Une manche complète jouée sur tablette sans hover collé, sans double tap, sans drag qui scrolle. Aucune cible sous 44 px |
| 9. Sur-animation et perf | **Phase « Performance et animations »**, après le layout | Budget de frame respecté sur l'appareil le plus faible avec une fixture de fin de partie ; `prefers-reduced-motion` actif ; 0 `setTimeout` en dur |

**Trois principes d'ordonnancement issus de cette recherche :**

1. **La phase 0 est bloquante.** Baselines, fixtures, cache-busting. Une heure ou deux, et sans elle chaque phase suivante travaille sans filet et paie plus cher.
2. **Pas de phase « Responsive et tactile » en fin de roadmap.** C'est l'erreur MTG Arena. Le responsive est dans la DoD de chaque phase d'écran. Seul le plateau a droit à une phase de layout dédiée, parce que c'est un changement de modèle et non une adaptation.
3. **Le lecteur de carte est le meilleur premier livrable.** Ajout autonome, risque quasi nul, il résout la douleur numéro un (lisibilité), il sert d'écran pilote pour le design system, et il est réutilisé par la galerie, les decks, le replay et le plateau.

## Sources

**Codebase (HIGH confidence, lecture de source et mesures du 2026-07-28, sur `~/marvel-work/fusion/marvel-lcg-src`)**
- `public/css/marvel/marvel.css:47-61` : `--scene-width: 1920`, `--scene-height: 1080`, `--font-size: 26px`, timings d'animation, `--anime-shuffle-time` déclaré deux fois
- `public/css/marvel/card.css:2-3` : `--card-width: 127px`, `--card-height: 176px`
- `public/js/marvel/scene.js:18-55` : `scale = min(vw/1920, vh/1080)`, conversions de coordonnées, `--font-size-out`
- `public/js/marvel/client.js:180, 400-452` : `fetch('get_world?p=0')`, `processQueue` avec `pop()` puis `messageQueue.length = 0`
- `public/js/marvel/ui.js:297-342, 438` : double système de timing, `document.body.style.setProperty('--anime-time')`, `querySelectorAll('.card')`
- `public/js/marvel/card_animation.js:93, 384, 410` et `move-card.js:244` : constantes de timing en dur (240, 1500)
- `public/css/marvel/image-preview.css:7-8, 18-19` : preview en `44.45vh` / `61.6vh`
- `public/css/marvel/index.css` : `div > .card:nth-child(N)` généré de 1 à 99
- `public/css/menu/style.css` : `*`, `body`, `button:hover`, `input[type=...]`, sélecteurs à ID ; chargé par 4 pages
- `public/marvel.html:64` : `maximum-scale=1, user-scalable=0` ; 59 `<link>` CSS
- `public/prepare.html` : `?v=18` de cache-busting manuel
- `src/engine/network/web_server.py:18-20, 39, 80-100, 155-164, 185-208` : `cache_max_age` (défaut 31536000), `HeaderCache`, `IsVersionMatch`, cache conditionné à `Build.release`
- `src/engine/device/web/server/server_files.py:18-37` : `handle_image_request`, `content_type='image/jpeg'` en dur, route fourre-tout `/{path:.+}`
- `src/engine/file/cache.py:11-110` : `.webp` testé en premier, `Cache.cache` sans éviction, `image_servers` synchrone timeout 3 s, `CreateNoImage` + `save_empty_image`
- `src/engine/lib/image_creator.py:19-26` : `TryRotateImage` ouvre chaque image avec PIL
- `launch.json` : `cache_max_age: 60`, 2 `image_servers`, `image_folders` avec chemin absolu `/mnt/c`
- `data/cards.json` : 4331 cartes, 3915 avec `text`, 3932 avec `desc` et `traits`, balisage inline

**Mesures (HIGH confidence, 2026-07-28)**
- `assets/pics/` : 387 fichiers, 81 Mo, moyenne 214 Ko, max 400 Ko
- `Jeux original/assets/pics/` : 4263 fichiers, 349 Mo, moyenne ~25 Ko
- Distribution des dimensions (échantillon 326) : 65 % 300x435, 15 % 710x1030, 10 % 435x300, 3 % 1030x710
- 4317 clés d'image distinctes, 3930 sans fichier dans `assets/pics/`
- `stat()` : 1,61 ms sur `/mnt/c` contre 0,0067 ms sur ext4 (242x)
- Lecture : 13,5 ms par fichier depuis `/mnt/c` ; décodage PIL 2,4 ms
- CSS : 165 `!important` au total dont 67 dans `wizard.css` ; 111 règles `:hover` dans 31 fichiers ; 0 `@media` dans `css/marvel/` ; 55 `vh`, 8 `vw`, 0 `dvh`/`svh`/`lvh` ; 142 `text-shadow`, 91 `transform`, 69 `opacity`, 26 `box-shadow`, 12 `filter`
- JS : 7318 lignes dans `public/js/marvel/`, 48 fichiers, 31 avec `sourceMappingURL` orphelin, 0 `.ts` et 0 `.js.map` sur la machine ; événements : 7 `click`, 3 `mousemove`, 2 `mouseup`, 1 `mousedown`, 1 `touchstart`, 1 `touchend` ; 23 lectures de layout, 8 `requestAnimationFrame`, 18 `setTimeout`
- Aucune collision de nom de classe entre `css/menu/` et `css/marvel/` (3 vs 146 classes)

**Documentation officielle (HIGH confidence)**
- [CSS-Tricks, Cascade Layers Guide](https://css-tricks.com/css-cascade-layers/) : ordre des couches inversé pour les déclarations `!important`, priorité du CSS non layered
- [Smashing Magazine, Integrating CSS Cascade Layers To An Existing Project](https://www.smashingmagazine.com/2025/09/integrating-css-cascade-layers-existing-project/) : legacy en couche basse, réécriture en couche haute
- [web.dev, Avoid large, complex layouts and layout thrashing](https://web.dev/articles/avoid-large-complex-layouts-and-layout-thrashing)
- [Chrome for Developers, Forced reflow](https://developer.chrome.com/docs/performance/insights/forced-reflow)

**Littérature et retours d'expérience (MEDIUM confidence)**
- [Security Boulevard, The Strangler Fig Pattern: Modernize Without a Big Bang Rewrite](https://securityboulevard.com/2026/07/the-strangler-fig-pattern-how-to-modernize-legacy-systems-without-a-big-bang-rewrite/) : 68-79 % des projets de modernisation échouent ou sous-performent
- [AWS Prescriptive Guidance, Strangler fig pattern](https://docs.aws.amazon.com/prescriptive-guidance/latest/cloud-design-patterns/strangler-fig.html)
- [ResetEra, The mobile Magic Arena app is such a broken mess](https://www.resetera.com/threads/the-mobile-magic-arena-game-app-is-such-a-broken-mess-and-it-bothers-me-how-little-attention-it-gets.941763/) : conçu desktop puis retrofitté mobile
- [GDKeys, The Card Games UI Design of Fairtravel Battle](https://gdkeys.com/the-card-games-ui-design-of-fairtravel-battle/) : « zooming in and panning the board would lead to a terrible experience »
- [TestQuality, Playwright Visual Regression: Baselines, Flake & CI Guide 2026](https://testquality.com/playwright-visual-regression-guide/) : filet que les tests fonctionnels ne fournissent pas, masquage du contenu dynamique
- [BrowserStack, Snapshot Testing with Playwright](https://www.browserstack.com/guide/playwright-snapshot-testing)
- [Practical Design Systems, Beware premature optimization](https://practicaldesignsystems.com/daily/beware-premature-optimization/) : construire des produits d'abord, abstraire ensuite
- [Cloudinary, React Lazy Loading Images: Best Practices and Common Pitfalls](https://cloudinary.com/guides/web-performance/react-lazy-loading-images) : `decoding="async"`, ratio du placeholder
- [ImageKit, Lazy Loading Images – The Complete Guide](https://imagekit.io/blog/lazy-loading-images-complete-guide/)
- [Smashing Magazine, Solo Development: Learning To Let Go Of Perfection](https://www.smashingmagazine.com/2025/01/solo-development-learning-to-let-go-of-perfection/)
- [Wayline, Scope Creep: The Silent Killer of Solo Indie Game Development](https://www.wayline.io/blog/scope-creep-solo-indie-game-development)
- [Mark Crosling, Why Solo Developers Ship Late](https://markcrosling.medium.com/why-solo-developers-ship-late-when-perfect-code-costs-you-clients-94cf4c209f93) : taux horaire effectif 65 % inférieur, refactoring sans fin
- [Site123, Designing Digital Cards for Mobile-First User Experience](https://www.site123.com/learn/designing-digital-cards-for-mobile-first-user-experience) : cible tactile minimale 44x44
- [CodeZone, JavaScript DOM Best Practices 2026](https://codezone.blog/javascript-dom-best-practices-2026/) : délégation d'événements, profondeur du DOM

**Documents internes**
- `.planning/PROJECT.md` (contraintes, périmètre, décisions en attente)
- `.planning/codebase/CONCERNS.md` (monolithe `scene.html`, absence de tests E2E, complexité campaign log)
- `Fusion/PREPARE-UI-PLAN.md` (plan wizard 6 étapes, contrainte de coexistence)

---
*Pitfalls research for: refonte UI/UX d'un client de jeu de cartes fonctionnel (Marvel Champions LCG local)*
*Researched: 2026-07-28*
