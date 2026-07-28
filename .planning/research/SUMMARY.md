# Résumé de la recherche projet

**Projet:** Refonte design/UI/UX complète du client web local Marvel Champions LCG (moteur Python intouchable ; frontend : menu, wizard de préparation, galerie de cartes, decks, replay, plateau de jeu ; cibles PC/tablette/mobile)
**Domaine:** Client web de jeu de cartes (LCG) coopératif, piloté par un moteur serveur autoritaire
**Recherché le:** 2026-07-28
**Confiance:** HIGH sur l'intégration technique et les contraintes serveur (vérifiées par lecture de code et mesures), MEDIUM sur les patterns UX de genre et les choix d'ergonomie tactile (sources croisées mais pas d'étalon officiel Marvel Champions)

## Résumé exécutif

Ce projet est une refonte de présentation d'un client de jeu de cartes déjà fonctionnel, pas une réécriture. Les quatre recherches convergent vers le même constat central : **le système actuel a déjà, sans le nommer, la bonne architecture** — un moteur serveur autoritaire qui pousse un snapshot complet (`get_world`) plus une demande d'action (`get_ask`), et un client purement présentationnel. Cette séparation nette est ce qui rend la refonte sûre : elle peut se faire **surface par surface**, en étranglement (strangler fig), sans jamais toucher au protocole ni au moteur. Le serveur route les fichiers statiques par extension, ce qui signifie qu'ajouter une page ou un composant ne demande aucune modification backend — c'est déjà le mécanisme utilisé pour `prepare.html`.

L'approche recommandée est : React 19 + TypeScript 6 + Vite 8 en multi-pages, une page migrée à la fois, avec l'ancien plateau qui reste la route par défaut jusqu'à ce que son remplaçant passe la non-régression. Le design system (tokens CSS) vient en premier car c'est le seul livrable qui améliore instantanément l'ancien ET le nouveau. Le composant Carte à double représentation (tuile lisible sur le plateau, scan complet à l'inspection) est le pivot de tout le projet : il résout le problème n°1 identifié par la recherche features (densité d'information / lisibilité), et il est réutilisé par la galerie, les decks, le replay et le plateau. Le plateau lui-même — la surface où l'utilisateur passe 95% de son temps — doit être découpé en 3-4 sous-phases de risque croissant (lecteur de carte → layout/responsive → interaction) et jamais traité comme une seule tâche ni repoussé en toute fin de projet.

Le risque principal, documenté par trois des quatre recherches indépendamment, est le **big-bang sur le plateau** : soit en le remettant à plus tard jusqu'à épuisement du temps/motivation, soit en glissant de « refonte UI » vers « réécriture du runtime JS » (`public/js/marvel/`, 7318 lignes de TypeScript compilé dont les sources sont perdues — un statut de code généré identique à celui du moteur Python). Le second risque majeur est le manque total de filet de régression côté frontend : les 3766 tests du moteur ne couvrent aucune ligne de HTML/CSS/JS. La mitigation validée par la recherche pitfalls est une Phase 0 bloquante : baselines Playwright + fixtures `get_world` capturées depuis l'autoplay, avant toute ligne de refonte visuelle.

## Constats clés

### Stack recommandée

Chemin B (React 19.2 + TypeScript 6.0.3 + Vite 8.1.5), mais **jamais en big-bang** : une page migrée à la fois, plateau en dernier, protocole extrait avant présentation. Le chemin A (moderniser le vanilla existant) a été écarté car le projet réinvente déjà React à la main sans ses garanties (helper `el()` maison, cache-buster manuel désynchronisé), et parce que réécrire d'un coup les ~1750 lignes de sémantique asks/options/ciblage sans sources TypeScript d'origine est le seul vrai risque calendaire du projet.

**Technologies core:**
- React 19.2.8 — `key={object_id}` correspond exactement au modèle serveur ; `<Activity>` stable utile pour les overlays hors écran
- TypeScript 6.0.3 (pas 7.0.2 — API compilateur publique absente avant 7.1, casserait typescript-eslint)
- Vite 8.1.5 en multi-pages (`build.rollupOptions.input`) — reproduit exactement le modèle de pages que le serveur sait déjà servir, hachage de contenu supprime les `?v=N` manuels
- Zustand 5.0.14 — remplacement complet du snapshot (`set({world: parsed})`), pas de reducers ni de merge
- Motion 12.42.2 — FLIP automatique (`layout`/`layoutId`) pour les déplacements de cartes, réservé au plateau
- CSS natif (Modules + custom properties + `@layer` + container queries), pas de Tailwind — les états combinatoires de carte (épuisée/confuse/étourdie/ciblable...) s'écrivent proprement en `[data-state~="..."]`

**Contrainte serveur déterminante :** routage par extension avec liste blanche stricte. Aucune route pour `.json`, `.png`/`.webp`, `.woff2`, `.svg` (hors `assets/textures/`) — tout asset de build doit respecter ces contraintes ou échoue silencieusement (200 OK avec `Content-Type: image/jpeg` vide, symptôme trompeur documenté dans PITFALLS).

Voir détail complet : `.planning/research/STACK.md`

### Fonctionnalités attendues

Le problème central n'est pas le look, c'est la **densité d'information** : afficher du texte de règles dense sur peu de surface sans zoom ni panoramique. Aucun client officiel Marvel Champions n'existe comme étalon ; les repères sont Hearthstone (carte digitale native), Legends of Runeterra (minimalisme, gabarits), MTG Arena (fidélité au scan, piège à éviter), et les outils communautaires (MarvelCDB, DragnCards).

**Incontournables (table stakes) :**
- Composant Carte à double représentation (tuile lisible + scan à l'inspection) — le composant le plus important du projet
- Zones du plateau explicitement délimitées et étiquetées (20+ zones sur un plateau coop 4 héros)
- Barre de demande (ask) à emplacement fixe, jamais une modale surgissante
- Indicateur de phase/tour permanent + rappel de l'action attendue
- Wizard de préparation avec stepper, récapitulatif persistant, validation en ligne explicite
- Responsive PC/tablette/mobile avec **navigation par zone** sur petit écran (pas de compression globale)
- Réglage de vitesse d'animation + animations interruptibles + `prefers-reduced-motion`
- Accessibilité de base : jamais la couleur seule, contrastes vérifiés

**Différenciateurs (v1.x) :**
- Tuiles adaptatives + vue d'ensemble sémantique du plateau
- Journal de partie consultable, puis cliquable
- Surlignage des cibles valides (dépend du descripteur backend)
- Solo multi-héros (aires repliables) — cas d'usage dominant mal traité par la concurrence

**À reporter en v2+ :** prévisualisation d'impact chiffrée (dépend d'infos moteur non confirmées), timeline de replay navigable, suivi de campagne visuel complet (4 formats de campagne à modéliser)

**Anti-features à exclure explicitement :** boutique/monnaie/battle pass, plateau 3D/pan-zoom libre, plateau très sombre à art plein cadre (échec documenté de Gwent Homecoming), réimplémentation de règles côté client, drag-and-drop comme seul moyen de jouer.

**Direction visuelle recommandée :** squelette clair/typographique (« instrument de jeu », meilleur rapport lisibilité/effort), personnalité comics dans le feedback transitoire (gouttières = délimitation de zones gratuite), thème sombre proposé en option plutôt qu'en fondation.

Voir détail complet : `.planning/research/FEATURES.md`

### Approche architecture

Le serveur route par extension de fichier, pas par dossier : toute nouvelle page `.html` est servie sans modification backend (pattern déjà amorcé avec `prepare.html`). Le plateau (`marvel.html`) devient une coquille avec interrupteur runtime ancien/nouveau (`?ui=old`/`?ui=new` ou localStorage), ce qui rend chaque étape réversible. Le contrat protocole (`WS notify → get_world snapshot → get_ask → POST /post → client_updated`) est encapsulé une fois pour toutes dans un module `session.js`/`protocol.ts` unique — aucune autre partie du nouveau code ne doit connaître ces endpoints.

**Composants majeurs :**
1. **Design system** (`tokens.css`, primitives, `card-tile`) — source unique consommée par legacy (via `bridge.css`) et nouveau code, livrable en premier
2. **Couche d'accès aux données** (`catalog`, `session`, `prefs`) — anti-corruption layer devant le protocole moteur, snapshot posé par remplacement complet jamais par patch
3. **Système de zones du plateau** — layout déclaratif par palier de viewport (table de données, pas du CSS dispersé), remplace l'homothétie fixe 1920x1080
4. **Couche d'interaction** (`interaction.js`) — machine à états à 4 temps (carte → effet → cibles → coût → post), ancrée sur les cartes via `bind_id`, jamais un menu global

**Patterns clés :** étranglement par nom de fichier HTML (menus/galerie/decks/replay), étranglement du plateau par coquille+interrupteur, tokens CSS comme source unique partagée legacy/nouveau, snapshot autoritaire sans aucune prédiction locale, réconciliation par clé (`object_id`) avec saut de rendu par hash, DOM+CSS (jamais canvas — le projet a déjà essayé et abandonné le canvas).

**Ordre de construction :** tokens+pont → core (api/catalog/prefs) + primitives/card-tile en parallèle → Menu (surface pilote) → Préparation → Galerie → Decks → Replay → **Plateau A (restylage+interrupteur, risque faible)** → **Plateau B (session+layout, risque moyen)** → **Plateau C (interaction, risque élevé)** → Nettoyage legacy.

Voir détail complet : `.planning/research/ARCHITECTURE.md`

### Pièges critiques

1. **Big-bang sur le plateau** — Ne jamais le mettre en dernier ni le traiter comme une tâche unique. Le découper en 3-4 chantiers indépendants et livrables séparément (lecteur de carte → layout/caméra → interactions tactiles → habillage), le premier (lecteur de carte) dès qu'un filet de sécurité existe.
2. **Glissement « refonte UI » → « réécriture du runtime »** — `public/js/marvel/` est du TypeScript compilé à sources perdues, même statut que le moteur. Étendre explicitement la contrainte d'intouchabilité à ce runtime dans PROJECT.md ; le nouveau code doit être une fonction pure de `get_world`, écrite à côté, sans lire le JS existant.
3. **Absence de filet frontend** — Zéro test ne charge une ligne de HTML/CSS/JS aujourd'hui. Phase 0 bloquante : baselines Playwright (5 écrans × 3 viewports, capturées AVANT la première ligne de CSS touché) + 20-40 fixtures `get_world` dumpées depuis l'autoplay + un test E2E du contrat de lancement de partie.
4. **Rendre « responsive » une scène homothétique 1920x1080** — Ajouter des `@media` ne sert à rien : tout est déjà multiplié par un scalaire unique (`scale = min(vw/1920, vh/1080)`). En portrait téléphone, cartes à 26px et texte à 5px. C'est une décision de modèle de layout (scènes multiples par palier + layout en flux dédié mobile), pas un ajustement CSS, et elle doit être tranchée en amont dans une phase de layout dédiée.
5. **Cohabitation CSS et piège `@layer`+`!important` inversé** — `wizard.css` contient déjà 67 `!important` sur 165 dans tout l'arbre. Poser `@layer` sans purger d'abord ces `!important` aggrave activement la situation (l'ordre des couches s'inverse pour les déclarations `!important`). Séquence obligatoire : baselines → purge `!important` → `@layer` → tokens.
6. **Zoomer le scan ne peut pas résoudre la lisibilité** — 65% des scans sont en 300x435 ; sur mobile DPR3 il faudrait 900px de source. Le texte de carte doit être rendu en HTML depuis `cards.json` (3915/4331 cartes ont un champ `text` structuré), le scan servant d'illustration.
7. **Passer au tactile en gardant une UI pilotée par le hover** — 111 règles `:hover`, quasi aucun événement tactile dans le runtime actuel. Séparer *inspecter* (hover desktop / long-press tactile) de *agir* (clic / tap), router via `@media (hover:hover) and (pointer:fine)` et Pointer Events.
8. **Dev solo, perfectionnisme, aucune boucle de feedback** — Aucun critère objectif n'existe pour l'UI (contrairement au moteur testé 3766/0). Écrire des critères d'acceptation observables par phase, une seule passe par écran, jouer une partie complète en sortie de phase, un test externe après les phases Préparation et Lecteur de carte.

Voir détail complet : `.planning/research/PITFALLS.md`

## Implications pour la roadmap

Sur la base des 4 recherches, structure de phases suggérée :

### Phase 0 : Filet de sécurité et boucle de dev (bloquante)
**Rationale :** Zéro test frontend existant aujourd'hui ; toute refonte sans filet transforme chaque régression en découverte tardive (ex. campaign log NeXt cassé, découvert 3 semaines plus tard). Le cache HTTP et le cache-busting manuel (`?v=18`) rendent aussi le debug trompeur sans automatisation préalable.
**Délivre :** Baselines Playwright (5 écrans × 3 viewports) capturées sur l'app actuelle ; 20-40 fixtures `get_world` dumpées depuis l'autoplay existant ; cache-busting automatisé ; extension explicite de la contrainte d'intouchabilité du moteur au runtime `public/js/marvel/` dans PROJECT.md.
**Évite :** Pitfall 3 (pas de filet), Pitfall 2 (glissement réécriture runtime), Pitfall 10 (cache/version/routage).

### Phase 1 : Fondations CSS et pipeline d'assets
**Rationale :** Le design system tokens est le seul livrable qui améliore instantanément les 6 surfaces existantes ET le nouveau code, pour un coût unique. La cohabitation CSS (legacy `style.css` à sélecteurs globaux + `wizard.css` à 67 `!important`) doit être assainie avant tout ajout, sinon `@layer` aggrave la situation. Le pipeline d'images (91% des clés hors `assets/pics/`, dossier `/mnt/c` 242x plus lent) doit être corrigé avant toute mesure de performance ultérieure.
**Délivre :** `tokens.css` + `bridge.css` (alias vers les anciens noms de variables, ne jamais les renommer) ; purge des `!important` de `wizard.css` ; `@layer legacy, tokens, base, components, utilities` ; conversion WebP + rapatriement des images hors `/mnt/c` ; décisions d'architecture figées (réconciliation par clé, timing unifié, `transform`/`opacity` uniquement).
**Utilise :** CSS natif + custom properties (STACK.md), `@layer` (ARCHITECTURE.md pattern 3).
**Évite :** Pitfall 7 (cohabitation CSS), Pitfall 8 (pipeline d'images), Pitfall 9 (contraintes d'archi posées trop tard).

### Phase 2 : Écrans pilotes — Lecteur de carte + Menu
**Rationale :** Le composant Carte est le goulot d'étranglement de tout le projet (galerie, decks, plateau, inspection en dépendent) ; le concevoir bien en le forgeant sur deux écrans réels (le plus dense + le plus simple) évite le double piège « design-system-first paralysant » et « screens-first qui dérive ». C'est aussi l'ajout à plus fort ratio valeur/risque : autonome, zéro dépendance au layout du plateau, résout la douleur n°1 (lisibilité).
**Délivre :** Composant Carte à double représentation (tuile + scan à l'inspection, texte HTML depuis `cards.json`) ; Menu refondu (shell, navigation, responsive de base).
**Adresse (FEATURES.md) :** Composant Carte, inspection non modale, hub d'accueil avec action primaire.
**Évite :** Pitfall 5 (zoomer le scan ne résout rien), Pitfall 11 (design-system-first/screens-first).

### Phase 3 : Extraction du design system
**Rationale :** Après deux écrans pilotes réels, extraire ce qui se répète en tokens/composants formels — jamais l'inverse. Plafonner à ce que les pilotes ont prouvé nécessaire (pas de composant sans deux usages réels).
**Délivre :** Primitives UI (boutons, panneaux, dialogues, onglets), design system documenté et réversible.
**Implémente :** Pattern 3 ARCHITECTURE.md (tokens comme source unique).

### Phase 4 : Wizard de préparation
**Rationale :** Contrat `/new?data=` non documenté, reconstruit par lecture de l'ancien `scene.html` — traiter séparément d'un problème de design system pur. Douleur explicitement citée par l'utilisateur (campaign logs sans guidage).
**Délivre :** Wizard 6 étapes (plan déjà défini dans `Fusion/PREPARE-UI-PLAN.md`), récapitulatif persistant, validation en ligne, aide contextuelle sur les champs de campaign log des 4 formats (MTS/MG/NeXt/AoA).
**Adresse (FEATURES.md) :** Wizard à stepper, validation en ligne, mémorisation de config.
**Évite :** Pitfall 6 dans FEATURES.md (contrat de lancement non testé) — nécessite un test E2E dédié.

### Phase 5 : Galerie de cartes
**Rationale :** Plus gros volume de données (2,3 Mo JSON, 4600+ cartes), zéro risque de jeu — le bon terrain pour éprouver la grille virtualisée et le chargement paresseux avant que le deck builder n'en dépende.
**Délivre :** Recherche instantanée, filtres à facettes, bascule grille/liste, grille virtualisée.
**Adresse (FEATURES.md) :** Recherche/filtres façon MarvelCDB, panneau de détail avec texte lisible.

### Phase 6 : Gestion de decks + Replay/Rapports
**Rationale :** Réutilise card-tile, grille et filtres déjà éprouvés en phase 5. Surfaces plus petites, faible risque.
**Délivre :** Deck builder avec stats en direct, validation de légalité ; replay et écran de fin de partie.

### Phase 7 : Plateau A — Restylage et interrupteur
**Rationale :** Premier bloc plateau, risque faible, réversible par `?ui=old`. Ne touche pas au JS existant, livre l'essentiel de l'amélioration perçue (chrome des cartes, HUD, lisibilité).
**Délivre :** `marvel.html` devenu coquille avec bascule ancien/nouveau ; CSS seul sur le DOM existant.
**Évite :** Pitfall 1 (big-bang plateau) en établissant le filet de sécurité (l'interrupteur) avant tout risque supplémentaire.

### Phase 8 : Plateau B — Modèle de layout et responsive réel
**Rationale :** Décision d'architecture explicite (scènes multiples par palier + layout en flux dédié mobile), jamais un ajustement CSS a posteriori. Le vrai saut de complexité mobile.
**Délivre :** `session.js` (anti-corruption), `model.js`, `layout.js` (table de zones par palier), `render.js` par diff, remplace l'homothétie 1920x1080.
**Évite :** Pitfall 4 (layout homothétique irresponsive).
**Recherche recommandée :** géométrie du plateau à 4 joueurs (focus exclusif vs vue condensée) — aucun précédent industrie solide trouvé pour cette configuration sur mobile.

### Phase 9 : Plateau C — Couche d'interaction tactile et asks
**Rationale :** Bloc le plus risqué (une erreur casse une partie), doit venir en dernier, bénéficie de tout le reste validé et de l'interrupteur comme filet.
**Délivre :** Machine à états de l'ask (carte → effet → cibles → coût → post), interactions tap-to-select/tap-to-target, séparation hover/tactile, `failure_reason` exposé.
**Évite :** Pitfall 6 (hover vers tactile), Pitfall 1 (dernier bloc du big-bang plateau, mais scindé).
**Recherche recommandée :** vocabulaire complet de `select_rule`/`ability_type`/`event_name` à inventorier depuis le moteur avant conception.

### Phase 10 : Performance/animations, puis nettoyage legacy
**Rationale :** Budget de performance mesuré sur fixtures de fin de partie, jamais avant que le layout et l'interaction ne soient stabilisés. Suppression du legacy seulement après parité constatée sur une partie complète.
**Délivre :** File d'animations bornée, `prefers-reduced-motion` câblé, suppression de `scene.html`/`cards.html`/`deck.html`/`css/legacy/`/`js/marvel/`.

### Raisonnement sur l'ordre des phases

- Le design system (tokens) vient avant tout car c'est le seul livrable à effet visible immédiat sur 100% des surfaces, legacy comme nouveau — le reporter revient à retoucher tout ce qui précède.
- Le lecteur de carte est délibérément placé tôt (Phase 2) car c'est le composant pivot dont dépendent galerie, decks, plateau ET inspection — trois des quatre recherches le désignent comme le meilleur premier livrable à fort impact et risque quasi nul.
- Le plateau est scindé en 3 sous-phases de risque strictement croissant (restylage → layout → interaction), jamais fusionné, conformément au consensus unanime des 4 recherches contre le big-bang plateau (précédent MTG Arena documenté).
- Aucune phase « Responsive et tactile » en fin de roadmap : le responsive est dans la Definition of Done de chaque phase d'écran hors-jeu ; seul le plateau mérite une phase de layout dédiée car c'est un changement de modèle, pas une adaptation.
- La Phase 0 est bloquante et précède toute autre phase : sans baselines ni fixtures, chaque phase suivante travaille sans filet et le coût de récupération d'une régression tardive est classé HIGH par PITFALLS.md.

### Signaux de recherche

Phases nécessitant probablement une recherche approfondie en cours de planification :
- **Phase 4 (Wizard) :** Le contrat `/new?data=` et le vocabulaire des `rules` (`mode_skirmish`, `v16_all`, etc.) ne sont pas documentés ; les journaux de campagne des 4 formats ont des clés différentes et une validation potentiellement incomplète.
- **Phase 8 (Plateau B, layout) :** La table de zones par palier est une décision de conception sans précédent dans le projet ; la géométrie mobile portrait à 4 joueurs n'a aucun précédent industrie solide identifié.
- **Phase 9 (Plateau C, interaction) :** Le vocabulaire complet de `select_rule`, `ability_type`, `event_name` doit être inventorié depuis le moteur avant conception — un cas non couvert bloquerait une partie.
- **Phase 5 (Galerie) :** Mesurer le volume réel de données avant de choisir la stratégie de virtualisation.

Phases à patterns standards (recherche-phase dispensable) :
- **Phases 0, 1, 3, 6, 7 :** Patterns établis (strangler fig, tokens CSS, réconciliation par clé, étranglement par nom de fichier HTML), déjà documentés en détail dans ARCHITECTURE.md et PITFALLS.md avec exemples de code directement applicables.

## Évaluation de la confiance

| Domaine | Confiance | Notes |
|---------|-----------|-------|
| Stack | HIGH sur versions/contraintes serveur (vérifiées code + registre npm), MEDIUM sur l'ergonomie tactile (peu de sources autoritaires spécifiques aux jeux de cartes) | STACK.md |
| Fonctionnalités | MEDIUM-HIGH — direction artistique Marvel Snap/LoR documentée par les designers eux-mêmes ; critiques concurrentes (LotR ACG, MTG Arena) en sources secondaires convergentes mais non arbitrées | FEATURES.md |
| Architecture | HIGH sur l'intégration au système existant (lu directement dans le code source), MEDIUM sur les patterns de domaine génériques (canvas vs DOM, seuils de lisibilité non mesurés sur appareil réel) | ARCHITECTURE.md |
| Pièges | HIGH sur les pièges spécifiques au codebase (vérifiés par lecture de source et mesures chiffrées), MEDIUM sur les pièges de méthode (littérature 2026 généraliste sur le dev solo et la modernisation) | PITFALLS.md |

**Confiance globale :** HIGH

### Écarts à traiter

- **Contrat `get_world`/`get_ask` non spécifié formellement** : reconstructible seulement par lecture de `descriptor.js`/`data.js`. À traiter comme prérequis de la Phase 8/9, pas maintenant.
- **Seuils exacts de lisibilité de carte (72px/110px)** : estimations dérivées du ratio de carte, non validées par test sur appareil réel. À vérifier avant de figer la table des paliers responsive en Phase 8.
- **Nombre réel de nœuds carte simultanés sur un plateau 4 joueurs** : estimé 40-120 par analogie, non mesuré en partie réelle. Mesurable simplement en comptant en cours de partie.
- **Ce que le descripteur moteur expose réellement (cibles légales, données de prévisualisation)** : non vérifié en code lors de cette recherche. Point de blocage potentiel pour deux features à forte valeur (surlignage des cibles, prévisualisation d'impact) — à instruire en priorité avant de committer ces features à une phase.
- **Géométrie du plateau coopératif 4 joueurs sur mobile** : aucune référence industrie solide trouvée. Proposition raisonnée (onglets de zone) mais non validée par un pattern existant — à prototyper tôt et tester en vrai en Phase 8.

## Sources

### Primaires (confiance HIGH)
- Code source du projet lu directement : `src/engine/network/web_server.py`, `src/engine/device/web/server/*`, `public/js/marvel/*`, `public/js/prepare/*`, `public/css/marvel/*`, `launch.json`, `data/cards.json` — voir listes complètes dans STACK.md, ARCHITECTURE.md, PITFALLS.md
- Mesures directes sur le codebase (2026-07-28) : distribution des dimensions d'images, comptage `!important`/`:hover`/`vh`, performance `/mnt/c` vs ext4, événements tactiles vs souris
- react.dev/blog/2025/10/01/react-19-2, vite.dev/blog/announcing-vite8, devblogs.microsoft.com/typescript (TS 7 sans API compilateur)
- css-tricks.com/css-cascade-layers (ordre inversé `!important`), smashingmagazine.com (cascade layers sur projet existant)

### Secondaires (confiance MEDIUM)
- tiffanysmart.com (designer UI Marvel Snap), ryanodon.com (étude de cas Legends of Runeterra)
- gdkeys.com (analyse UI jeux de cartes, échec pan/zoom), medium.com (études de cas Marvel Snap, LotR ACG)
- securityboulevard.com / docs.aws.amazon.com (strangler fig pattern, taux d'échec modernisation)
- marvelcdb.com, dragncards.com (référence outils communautaires LCG)

### Tertiaires (confiance LOW, à valider)
- Retours de forum non arbitrés (Gwent Homecoming lisibilité, ResetEra sur MTG Arena mobile)
- Littérature généraliste « DOM vs canvas » et « dev solo perfectionnisme » — signal directionnel utile, non spécifique au domaine LCG

---
*Recherche terminée le : 2026-07-28*
*Prêt pour la roadmap : oui*
