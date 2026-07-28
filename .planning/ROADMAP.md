# Roadmap : Refonte Design / UI / UX Marvel LCG

## Vue d'ensemble

La refonte se fait **surface par surface, en étranglement**, sans jamais toucher au moteur Python ni au runtime `public/js/marvel/` (sources perdues, même statut de code généré). On commence par poser un filet de sécurité (captures de référence, fixtures, bascule `?ui=old`), puis les fondations partagées (stack React/TS/Vite servie par le serveur existant + design system tokenisé qui améliore aussi l'ancien), puis on forge le composant pivot (la Carte) sur deux écrans pilotes réels (coquille/menu). La préparation de partie suit. Le plateau, où l'utilisateur passe 95 % de son temps, est découpé en **trois phases de risque strictement croissant** (restylage → modèle de layout responsive/tactile → interactions et asks) : jamais en bloc, jamais en dernière minute, chaque étape réversible d'un clic.

**Hors périmètre v1 :** galerie de cartes, deck builder et replay restent sur leurs écrans actuels (fonctionnels) et sont différés en v1.x. Le responsive n'est pas une phase finale : il est dans la definition of done de chaque écran ; seul le plateau mérite une phase de layout dédiée car c'est un changement de modèle, pas une adaptation CSS.

## Phases

**Numérotation :**
- Phases entières (1, 2, 3) : travail planifié du jalon
- Phases décimales (2.1, 2.2) : insertions urgentes (marquées INSERTED)

- [x] **Phase 1 : Filet de sécurité et boucle de dev** (BLOQUANTE, terminée le 2026-07-28 — 6/6 plans) - Rien ne bouge visuellement avant d'avoir de quoi détecter une régression
- [ ] **Phase 2 : Fondations — stack et design system tokenisé** - React/TS/Vite servi par le serveur existant + tokens partagés ancien/nouveau
- [ ] **Phase 3 : Pilotes — composant Carte et coquille/menu** - Le composant pivot forgé sur deux écrans réels, primitives extraites derrière
- [ ] **Phase 4 : Préparation de partie** - Wizard 6 étapes, validation explicite, aide sur les campaign logs
- [ ] **Phase 5 : Plateau A — restylage et lisibilité** - Tuiles lisibles, zones étiquetées, HUD, inspection non modale (risque faible)
- [ ] **Phase 6 : Plateau B — modèle de layout, responsive et tactile** - Fin de l'homothétie 1920x1080, navigation par zone, tactile (risque moyen)
- [ ] **Phase 7 : Plateau C — interactions, asks et animations** - Barre d'ask fixe, jouer au tap, undo, animations réglables (risque élevé)

## Détail des phases

### Phase 1 : Filet de sécurité et boucle de dev
**Objectif** : Disposer d'un moyen objectif de détecter toute régression visuelle ou fonctionnelle avant la première ligne de refonte.
**Dépend de** : Rien (première phase, bloquante pour toutes les autres)
**Requirements** : FOUND-01
**Critères de succès** (ce qui doit être VRAI) :
  1. Une commande unique capture les écrans actuels (6 écrans × 3 gabarits PC/tablette/mobile) et, à la relance, signale toute différence visuelle.
  2. 20 à 40 fixtures `get_world` issues de l'autoplay sont rejouables hors partie : on peut afficher un état de plateau sans lancer une partie réelle.
  3. Sur toute page en cours de migration, l'utilisateur revient à l'ancienne version par `?ui=old` et le jeu reste jouable de bout en bout.
  4. Un test automatisé vérifie qu'une partie se lance depuis l'écran de préparation actuel et atteint le plateau (contrat `/new?data=` gelé avant d'y toucher).
**Note** : la contrainte d'intouchabilité du moteur est étendue explicitement au runtime `public/js/marvel/` dans PROJECT.md. Le nouveau code est une fonction pure de `get_world`, écrit à côté, sans lire le JS existant.
**Plans** : 6 plans

Plans:
- [x] 01-01-PLAN.md — Contraintes actées, harnais Playwright installé, 18 images de référence figées (terminé le 2026-07-28)
- [x] 01-02-PLAN.md — Page de comparaison avant/après en français et validation explicite des références (terminé le 2026-07-28)
- [x] 01-03-PLAN.md — 34 fixtures `get_world` issues de 5 parties autoplay + `/fixtures.html` (terminé le 2026-07-28)
- [x] 01-04-PLAN.md — Bascule `?ui=old` mémorisée, démontrée sur l'écran de préparation (terminé le 2026-07-28)
- [x] 01-05-PLAN.md — Contrat `/new?data=` gelé (8 clés typées) et arrivée au plateau vérifiée automatiquement (terminé le 2026-07-28)
- [x] 01-06-PLAN.md — Livraison (re-zip `Fusion/`, autoplay 0 traceback) et vérification d'ensemble validée par l'utilisateur (terminé le 2026-07-28)

### Phase 2 : Fondations — stack et design system tokenisé
**Objectif** : Une base technique et visuelle unique alimente simultanément les écrans anciens et les nouveaux, pour un coût payé une seule fois.
**Dépend de** : Phase 1
**Requirements** : FOUND-02, FOUND-03, ACC-01, ACC-02
**Critères de succès** (ce qui doit être VRAI) :
  1. Une page construite en React 19 + TS + Vite, buildée dans `public/app/`, s'affiche via le serveur Python **sans aucune modification du backend**, à côté des pages actuelles toujours fonctionnelles.
  2. Modifier un token (couleur, typo, espacement) change l'apparence des écrans anciens ET nouveaux en même temps.
  3. Le thème sombre s'active par bascule de tokens, sans retoucher un seul composant.
  4. Chaque aspect (justice / leadership / agression / protection) reste identifiable sans la couleur (icône + libellé), et les contrastes du texte de règles et des compteurs passent le seuil défini par les tokens.
  5. Un simple rechargement sert toujours la dernière version des assets : plus de `?v=N` à incrémenter à la main.
**Séquence obligatoire** (piège documenté) : captures de référence → purge des `!important` de `wizard.css` → `@layer` → tokens. Poser `@layer` avant la purge inverse l'ordre des couches et aggrave la situation. Contrainte serveur : routage par extension en liste blanche stricte, tout asset de build doit s'y conformer sous peine d'échec silencieux.
**Plans** : 10 plans

Plans:
- [x] 02-01-PLAN.md — Filet étendu aux 3 panneaux cachés du wizard (9 références de plus) — terminé le 2026-07-28
- [x] 02-02-PLAN.md — Projet Vite 8 + React 19 + TS 6, vitrine minimale, garde-fou d'extensions — terminé le 2026-07-28
- [x] 02-03-PLAN.md — Déploiement vers le jeu, service prouvé par le serveur Python, fin des `?v=N` — terminé le 2026-07-28
- [x] 02-04-PLAN.md — Purge des 105 `!important` de `wizard.css`, styles en ligne extraits — terminé le 2026-07-28 (2 exceptions documentées, 0 différence de style calculé)
- [ ] 02-05-PLAN.md — `@layer` posé, `tokens.css` lié en premier, tout l'existant dans `legacy`
- [ ] 02-06-PLAN.md — `tokens.css` complet (2 thèmes, aspects), contrôle de contraste, `menu/style.css` tokenisé
- [ ] 02-07-PLAN.md — `wizard.css` et `prepare.css` tokenisés, critère 2 mesuré
- [ ] 02-08-PLAN.md — Aspects partagés (icône + libellé), palette unique, ACC-01
- [ ] 02-09-PLAN.md — Vitrine finale, bascule de thème, vitrine sous surveillance, axe contraste
- [ ] 02-10-PLAN.md — Livraison (re-zip `Fusion/`, autoplay 0 traceback) et vérification d'ensemble

### Phase 3 : Pilotes — composant Carte et coquille/menu
**Objectif** : Le composant le plus important du projet est forgé sur deux écrans réels, et l'utilisateur entre dans l'app par un hub clair.
**Dépend de** : Phase 2
**Requirements** : FOUND-04, SHELL-01, SHELL-02, SHELL-03
**Critères de succès** (ce qui doit être VRAI) :
  1. L'utilisateur lit le nom, le coût, les stats, les icônes et les statuts d'une carte **sans ouvrir le scan** (tuile lisible, art recadré).
  2. L'utilisateur inspecte le texte réel de la carte (rendu en HTML depuis `cards.json`) et son scan complet au survol (PC), à l'appui long (tactile) ou au clavier, **sans que la carte concernée soit masquée**.
  3. À l'ouverture de l'app, l'utilisateur voit un hub avec une action primaire évidente (Reprendre / Nouvelle partie).
  4. L'utilisateur navigue via une navigation persistante à libellés texte (latérale sur PC, basse sur mobile) et revient en arrière depuis n'importe quel écran sans rien perdre.
  5. Les primitives réutilisées par ces deux écrans (boutons, panneaux, dialogues, onglets) existent comme composants du design system — aucun composant créé sans deux usages réels.
**Rationale d'ordre** : le menu est la surface pilote de l'étranglement (la plus simple), la Carte le composant pivot (le plus dense). Les deux ensemble évitent le double piège « design-system-first paralysant » et « screens-first qui dérive ». Zoomer le scan ne peut pas résoudre la lisibilité : 65 % des scans font 300x435.
**Plans** : TBD

### Phase 4 : Préparation de partie
**Objectif** : L'utilisateur configure et lance une partie sans jamais se demander quoi remplir ni pourquoi le bouton est grisé.
**Dépend de** : Phase 3
**Requirements** : PREP-01, PREP-02, PREP-03, PREP-04, PREP-05, PREP-06
**Critères de succès** (ce qui doit être VRAI) :
  1. L'utilisateur configure et lance une partie de bout en bout via 6 étapes (Mode → Héros → Decks → Scénario → Difficulté → Récapitulatif), avec stepper visible, retour arrière sans perte de saisie, récapitulatif de ses choix visible en permanence, et arrivée au plateau identique à l'ancien écran.
  2. Quand le lancement est bloqué, le bouton final affiche la raison exacte du blocage.
  3. L'utilisateur choisit son héros dans une galerie visuelle (art, aspect) et son deck parmi deck de départ / deck perso / import MarvelCDB.
  4. Depuis l'accueil, l'utilisateur relance sa dernière configuration en un geste et reprend une sauvegarde.
  5. Chaque champ des campaign logs des 4 formats (MTS / MG / NeXt / AoA) affiche une aide expliquant quoi y mettre.
**Recherche approfondie recommandée** : contrat `/new?data=` et vocabulaire des `rules` (`mode_skirmish`, `v16_all`…) non documentés ; clés et validation des campaign logs différentes selon les 4 formats. Base de travail existante : `Fusion/PREPARE-UI-PLAN.md`.
**Plans** : TBD

### Phase 5 : Plateau A — restylage et lisibilité
**Objectif** : En partie, l'utilisateur lit le plateau d'un coup d'œil — sans que rien du comportement de jeu n'ait changé.
**Dépend de** : Phase 3 (composant Carte), Phase 1 (bascule `?ui=old`)
**Requirements** : BOARD-01, BOARD-02, BOARD-03, BOARD-04, BOARD-13
**Critères de succès** (ce qui doit être VRAI) :
  1. Chaque carte du plateau est une tuile lisible (nom, coût, stats, icônes, statuts) sans zoom ni panoramique.
  2. L'utilisateur inspecte le scan complet et le texte d'une carte du plateau au survol, à l'appui long ou au clavier, sans occlusion de la carte concernée et sans modale bloquante.
  3. Les zones (vilain, schémas, rencontre, et par joueur : identité, alliés, améliorations, main, decks, ressources) sont visuellement délimitées et étiquetées.
  4. Les compteurs (dégâts, menace, statuts, ressources) sont lisibles directement sur les tuiles, en fort contraste.
  5. Un indicateur permanent montre la phase, le tour et l'action attendue ; le survol ou l'appui sur un mot-clé (Retaliate, Guard, Confused…) affiche son rappel de règle.
**Definition of done** : une partie complète se joue sans traceback (autoplay 0 traceback), `?ui=old` reste à un clic, aucune ligne du runtime existant n'est modifiée.
**Plans** : TBD

### Phase 6 : Plateau B — modèle de layout, responsive et tactile
**Objectif** : Le plateau devient réellement jouable sur tablette et mobile, par changement de modèle de layout et non par retouche CSS.
**Dépend de** : Phase 5
**Requirements** : BOARD-11, BOARD-12, MOB-01, MOB-02, MOB-03
**Critères de succès** (ce qui doit être VRAI) :
  1. Sur petit écran, l'utilisateur passe d'une zone du plateau à l'autre (onglets / carrousel / focus) au lieu de subir un plateau compressé illisible.
  2. Toutes les cibles tactiles font au moins 44 px, chaque survol a son équivalent appui long, les zones sûres sont respectées et les actions principales sont atteignables au pouce.
  3. La partie invite à passer en paysage sans jamais bloquer ; les menus restent utilisables en portrait.
  4. En solo multi-héros, l'aire du joueur actif s'affiche en grand et les autres en bandeaux repliés montrant leurs compteurs clés.
  5. L'utilisateur obtient une vue d'ensemble du plateau par dézoom **sémantique** (moins d'information, tuiles condensées), jamais par réduction optique.
**Piège adressé** : l'homothétie unique `scale = min(vw/1920, vh/1080)` rend tout `@media` inopérant (cartes à 26 px, texte à 5 px en portrait). Il s'agit d'une table de zones par palier de viewport, décidée en amont.
**Recherche approfondie recommandée** : géométrie du plateau coopératif à 4 joueurs sur mobile (focus exclusif vs vue condensée) — aucun précédent industrie solide ; seuils de lisibilité de carte à vérifier sur appareil réel avant de figer les paliers.
**Plans** : TBD

### Phase 7 : Plateau C — interactions, asks et animations
**Objectif** : L'utilisateur joue toute la partie depuis la nouvelle interface, au clic comme au doigt, sans jamais être surpris par une modale ni perdre le fil.
**Dépend de** : Phase 6
**Requirements** : BOARD-05, BOARD-06, BOARD-07, BOARD-08, BOARD-09, BOARD-10, ACC-03
**Critères de succès** (ce qui doit être VRAI) :
  1. Toute demande du moteur s'affiche dans une barre fixe (intitulé, options, annuler / passer) — jamais en modale surgissante.
  2. L'utilisateur joue une carte au clic ou au tap (sélection → effet → cibles → coût), sans drag obligatoire ; la main s'affiche en rangée, se déplie au survol/focus, et les cartes jouables sont visuellement distinguées.
  3. Seules les actions irréversibles demandent confirmation, et l'annulation (undo) est visible en permanence depuis le plateau.
  4. Les animations montrent l'origine, la destination et la cible des dégâts ; leur vitesse est réglable, elles sont interruptibles et `prefers-reduced-motion` les neutralise.
  5. L'utilisateur consulte un journal de partie qui répond à « que vient-il de se passer ? ».
**Definition of done** : une partie complète jouée de bout en bout dans la nouvelle UI, sur PC et sur mobile, avant de retirer quoi que ce soit de l'ancien.
**Recherche approfondie recommandée** : inventorier depuis le moteur le vocabulaire complet de `select_rule`, `ability_type`, `event_name` avant conception — un cas non couvert bloquerait une partie.
**Plans** : TBD

## Couverture des requirements

| Requirement | Phase |
|-------------|-------|
| FOUND-01 | Phase 1 |
| FOUND-02 | Phase 2 |
| FOUND-03 | Phase 2 |
| ACC-01 | Phase 2 |
| ACC-02 | Phase 2 |
| FOUND-04 | Phase 3 |
| SHELL-01 | Phase 3 |
| SHELL-02 | Phase 3 |
| SHELL-03 | Phase 3 |
| PREP-01 | Phase 4 |
| PREP-02 | Phase 4 |
| PREP-03 | Phase 4 |
| PREP-04 | Phase 4 |
| PREP-05 | Phase 4 |
| PREP-06 | Phase 4 |
| BOARD-01 | Phase 5 |
| BOARD-02 | Phase 5 |
| BOARD-03 | Phase 5 |
| BOARD-04 | Phase 5 |
| BOARD-13 | Phase 5 |
| BOARD-11 | Phase 6 |
| BOARD-12 | Phase 6 |
| MOB-01 | Phase 6 |
| MOB-02 | Phase 6 |
| MOB-03 | Phase 6 |
| BOARD-05 | Phase 7 |
| BOARD-06 | Phase 7 |
| BOARD-07 | Phase 7 |
| BOARD-08 | Phase 7 |
| BOARD-09 | Phase 7 |
| BOARD-10 | Phase 7 |
| ACC-03 | Phase 7 |

**32 / 32 requirements v1 mappés — aucun orphelin, aucun doublon.**

## Progression

**Ordre d'exécution :** les phases s'exécutent dans l'ordre numérique : 1 → 2 → 3 → 4 → 5 → 6 → 7

| Phase | Plans terminés | Statut | Terminée le |
|-------|----------------|--------|-------------|
| 1. Filet de sécurité | 6/6 | Complete | 2026-07-28 |
| 2. Fondations (stack + design system) | 0/10 | Not started | - |
| 3. Pilotes (Carte + coquille) | 0/TBD | Not started | - |
| 4. Préparation de partie | 0/TBD | Not started | - |
| 5. Plateau A — restylage | 0/TBD | Not started | - |
| 6. Plateau B — layout/tactile | 0/TBD | Not started | - |
| 7. Plateau C — interactions | 0/TBD | Not started | - |
