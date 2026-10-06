# Plan d'exécution : le mode manuel joué comme sur OCTGN

> **Pour un agent d'exécution :** SOUS-SKILL REQUISE : utiliser
> `superpowers:subagent-driven-development` (recommandé) ou
> `superpowers:executing-plans` pour dérouler ce plan lot par lot. Les
> étapes sont en cases à cocher (`- [ ]`). Chaque test est lancé **rouge
> d'abord** (`superpowers:test-driven-development`), message rouge noté, puis
> vert.

**But :** qu'on puisse jouer une partie entière à la main comme sur OCTGN, en
commençant par le défaut signalé le 06/10 : poser une carte de sa main en la
glissant sur la table.

**Spec :** `docs/superpowers/specs/2026-10-06-mode-manuel-comme-octgn-design.md`
(les renvois « §B.3 », « D.3 »… pointent vers elle).
**Fiche et questions :** `.planning/todos/2026-10-06-mode-manuel-comme-octgn.md`.
**Statut :** PLANIFIÉ, RIEN CODÉ (06/10/2026).

**Questions tranchées le 06/10/2026** (détail dans la fiche) : 1 A, 2 A,
4 A, 5 A, 6 A, 7 A, 10 A, 11 A, 12 A, 13 A. Quatre réponses s'écartent de la
recommandation et priment sur toute mention « si question X = A » plus bas :
- **3** : une amélioration lâchée sur la table ouvre une fenêtre qui propose
  les cartes en jeu pouvant la recevoir ; une seule cible possible (l'identité)
  = attache directe, sans fenêtre.
- **8** : le double-clic en main ne retourne plus la carte en secret ET la
  pose en jeu selon son type (même fonction que le glisser, `poser-en-jeu.ts`).
- **9** : aucune aide au paiement, aucun coût dans l'étiquette du glisser.
- **14** : comme OCTGN, chacun ne bouge que ses propres cartes ; les cartes
  Rencontre sont à tous.

**Modèle conseillé :** Opus pour les lots 1, 2, 4 et 5 (moteur, logique de
geste, multijoueur). Sonnet suffit pour les lots 0, 3, 6 et 7.

## Règles communes à tous les lots

### Avant de commencer
- [ ] Lire la spec, la fiche (questions tranchées) et `.twei/SPEC.md` s'il
  existe.
- [ ] `git stash list` : deux sessions partagent l'arbre. Au 06/10,
  `stash@{0}` sur `mode-manuel` contient des témoins d'annulation
  (`dc11eb3e`) : ne pas le perdre, ne pas le réappliquer sans accord.
- [ ] Travailler sur la branche `mode-manuel`. Un commit atomique par lot,
  **seulement sur demande**.

### Règles du projet qui s'appliquent
- **TypeScript strict, aucun `any`.** Réutiliser `emettreGeste`,
  `libellePile`, `useAppuiLong`, et le patron des fonctions pures comme
  `interpreterTouche` (`board/manuel/clavier.ts`).
- **Mots-clés** (CLAUDE.md) : avant d'écrire du code qui touche Uses, Tenace,
  Permanent ou Victoire, ouvrir `docs/reference/mots-cles/uses.md`,
  `toughness.md`, `permanent.md`, `victory.md` (lots 2 et 6).
- **PROCESSUS-CARTE ne s'applique pas** : aucune carte n'est créée ni
  modifiée. Seule son étape 8 bis (« tester ce que le plateau dessine ») est
  reprise dans chaque lot.
- **Pas de repli générique** : un cas imprévu est un refus nommé (gate).

### Tests du plateau
- `cd ui-app && npx vitest run <fichiers>`, puis la suite complète.
- `npm run typecheck` (exigé par `deployer.sh`).
- Les tests du glisser Auto (`board/glisser/*.test.ts`) restent verts **sans
  modification**.

### Tests du moteur
- `~/marvel-work/python/bin/python3.10 tools/test_mode_manuel.py <game_dir> <port> [cas]`
  depuis `Fusion/marvel-lcg-src/` (`test_mode_manuel.py:3-5`).
- `<game_dir>` est un worktree ou une copie `cp -rL` : les `.game-src*` sont
  des **liens** vers `src`, écrire dedans écrase le vrai code.
- Jamais en root (les fichiers du jeu passeraient à root).
- **Moteur partagé** (`puzzle.py`, `game_session.py`, `engine/device/manager/base.py`…) :
  batterie complète `tools/test_capacites.py <game_dir> <port> rapport.json`
  (`test_capacites.py:19-21`) sur le code modifié **et** sur un worktree de
  HEAD, puis comparer les deux rapports cas par cas. Seuil : aucun cas vert
  sur HEAD ne devient rouge. Une avalanche de rouges vient de la copie gelée :
  rejouer chaque cas seul avant de conclure. Durée : non mesurée, prévoir la
  batterie en fond. Ne pas confondre avec la batterie Stan Lee, en pause
  jusqu'à la semaine du 05/10 et à ne pas relancer.

### E2E et navigateur : la recette complète
L'e2e vise par défaut le **vrai** serveur (`ui-check/playwright.config.ts:18`,
`http://127.0.0.1:2345`) et lance une **nouvelle partie**
(`mode-manuel.spec.ts:33-35`) : lancé sans réglage, il détruit la partie en
cours. Toujours :
1. Copier `Fusion/marvel-lcg-src/launcher_fast.py` en
   `launcher_fast_essai_manuel.py`, en changeant seulement la ligne `GAME`
   (`:36`) vers `.game-essai-manuel`.
2. Construire et démarrer ce cache séparé sur un port libre (ex. 2346), sur le
   modèle de `ui-check/scripts/serveur-dev.py`, avec
   `~/marvel-work/python/bin/python3.10`. Jamais `.game`, jamais le port 2345,
   jamais `launch.json`.
3. Construire le plateau : `bash ui-app/deployer.sh` (depuis WSL) construit
   l'UI et la dépose dans `Fusion/marvel-lcg-src`, le jeu local, sans rien
   envoyer en prod (`deployer.sh:2`). Vérifier que le serveur d'essai sert le
   même hash de bundle.
4. Depuis WSL : `export UI_CHECK_BASE=http://127.0.0.1:2346 WSLENV=UI_CHECK_BASE`
   puis `cd ui-check && npx playwright test tests/mode-manuel.spec.ts --project=pc`
   (Playwright tourne sous Windows, `WSLENV` est obligatoire).
5. Nettoyer : arrêter le moteur, supprimer `launcher_fast_essai_manuel.py` et
   `.game-essai-manuel/` (retirer les liens d'abord), effacer les profils
   Chrome du harnais (`--user-data-dir`), vérifier que `git status` n'a
   changé que par vos fichiers.

Ce que prouve chaque source :
- `/get_world` prouve la pile où se trouve une carte et son `is_face_up` ;
- les PV, la menace et les jetons se prouvent **à l'écran** (`.jauge-texte`),
  `info.health` est vide en manuel (`mode-manuel.spec.ts:24-31`) ;
- captures pendant le glisser, au lâcher et après.

### Déploiement
Seulement sur « déploie » : `bash ui-app/deployer.sh`, puis
`deployer.ps1 -Code`, puis vérifier le hash du bundle en prod, puis mettre à
jour `.planning/todos/2026-09-19-file-d-attente-et-deploiement.md` aussitôt.

---

## Lot 0 : remettre le filet en état

**Objectif :** l'e2e du mode manuel conforme aux touches actuelles, avant tout
changement.
**Fichier :** `ui-check/tests/mode-manuel.spec.ts`.

- [x] Lancer l'e2e sur HEAD (recette ci-dessus). Rouge attendu à l'étape 5
  (`:265-281`) : « le vilain n'a pas visiblement encaissé les dégâts » (la
  touche « 3 » a été retirée par `5b88d9a2`, `clavier.ts:119`). Noter le
  message exact.
- [x] Étape 5 : remplacer « 3 » par **une** pression sur Bas au survol du
  méchant, et attendre 1 dégât. L'étape 6 (`:283-287`) fait un seul Ctrl+Z et
  exige le retour à la vie d'avant : trois Bas demanderaient trois Ctrl+Z.
- [x] Relancer : vert. L'étape 4 (refus sur la table) reste telle quelle
  jusqu'au lot 2.
- [x] Noter la commande exacte et la durée dans la fiche.

**Fin :** e2e vert sur HEAD.

## Lot 1 : le moteur se tait vraiment à l'écran (P2, avant tout le reste)

Placé en tête parce que le bouton « Fin du tour » et la touche E font avancer
le moteur pendant le manuel et corrompent une partie basculée.

**Préalable :** question 8.

**Fichiers :**
- `board.tsx:4574` (bouton flottant) et `:3460-3461`, `:3764-3766` (touche E) :
  garde `!manuel` ;
- `board.tsx:2114-2117` : `interactifs` vides en manuel ;
- `board.tsx:3486-3490` (« ↶ Annuler ») et `:3468-3469` (U) : en manuel,
  `lancerAnnulation` (`CoucheTriche.tsx:628-637`), à exposer depuis `useTriche` ;
- `board.tsx:2708-2711` : garde `!spectateur` sur le glisser manuel ;
- `CoucheTriche.tsx:729-738` : le double-clic sur une carte en main ne la
  retourne plus (question 8). La pose en jeu par double-clic vient au lot 2,
  une fois `poser-en-jeu.ts` écrit.

**Ctrl+Z qui repasse en Auto** (`superpowers:systematic-debugging`, cause
d'abord) :
- [x] Cas rouge `cas_annulation_geste_garde_la_pause` dans
  `tools/test_mode_manuel.py` : partie ordinaire en pause, un geste, puis
  `AnnulerDernierGeste`. Attendu : `manuel_actif is True`. Le cas existant
  `cas_annulation` couvre une partie déclarée, pas une partie basculée.
- [x] Piste : la garde `not self.mise_en_place_finie`
  (`game_session.py:277`). Corriger selon la cause établie. Moteur partagé :
  batterie.
  **Cause établie le 06/10/2026 (piste fausse) :** le moteur reposait bien
  `manuel_actif` après le Ctrl+Z, mais sans republier la table : `/get_world`
  servait la trame du rejeu (`manuel_actif=false`) et le plateau affichait
  Auto. Preuve : un second `/manuel_undo` répondait « rien a annuler » (porte
  ouverte seulement si `manuel_actif`), pas « pas une partie manuelle ». Le cas
  lit donc la trame PUBLIÉE ; correctif : `FinirLeRejeuDesGestes` force un rendu
  quand il repose le silence.

**Option recommandée « corriger le moteur »** : le moteur refuse une réponse à
sa question garée tant que `manuel_actif` est vrai.
- [x] Cas rouge `cas_reponse_refusee_pendant_la_pause`. Touche
  `engine/device/manager/base.py` : batterie.
  **Écart :** le refus est posé dans la route `/post`
  (`engine/device/web/server/server_sync.py`), pas dans `base.py` :
  `/manuel_passer` répond par `PasserQuestionCourante` → `WhenInput`, et doit
  rester possible pendant la pause. Refuser dans `WhenInput` l'aurait fermé.

**Tests plateau (rouge d'abord) :**
- [x] `plateau-muet.test.tsx` : en manuel, bouton flottant absent, E sans
  effet, aucune carte surlignée ;
- [x] `clavier-wiring.test.tsx` : double-clic sur une carte en main, aucun
  `Puzzle.Flip` (rouge sur HEAD : la carte est retournée) ;
- [x] « Annuler » et U appellent `/manuel_undo` en manuel ;
- [x] un spectateur ne lance pas le glisser.

**Navigateur :** sur une partie basculée, ni le bouton ni E ne font avancer la
phase (`/get_world`) ; « Annuler » défait le dernier geste et la table reste en
Manuel.

**Fin :** `manuel-75/76` et `manuel-80/81` ne se reproduisent plus.

## Lot 2 : poser une carte de la main à la souris (P1)

**Préalables :** questions 1, 2, 3, 4, 5, 9, 12, 13.

### 2a. Moteur (additif, un seul passage de batterie)
**Fichier :** `Fusion/marvel-lcg-src/src/game/puzzle/puzzle.py`.
- [x] Ajouter `siege: int|None=None` à `_ZoneParNom` (`:841`), `MoveTo`
  (`:853`), `Shuffle` (`:887`), `Engage` (`:898`). Avec `siege`, viser
  `world.const_seat_order_players[siege]`. Préciser dans la docstring ce que
  vise `player`.
- [x] Si question 4 = A : `'PlayerProcessingArea': lambda j: j.area_processing`
  dans `ZONES_JOUEUR` (`:794-820`).
- [x] Si question 5 = A : compléter la menace de départ d'une manigance annexe
  et les PV à l'entrée en jeu manuelle (fiches mots-clés d'abord).

**Tests moteur (rouge d'abord) dans `tools/test_mode_manuel.py` :**
- [x] Étendre `monter_le_moteur` (`:39`) à plusieurs héros (liste `[hero]` en
  `:144`).
- [x] `cas_poser_depuis_la_main` : un allié et un soutien de la main, `MoveTo`,
  arrivent face visible, `manuel_commands` +1, aucune capacité déclenchée ;
  témoin Uses et Tenace (question 5). Rouge par substitution : viser
  `HandsArea` doit faire échouer le cas.
- [x] `cas_moveto_par_siege` : deux héros, ordre tourné, `MoveTo(..., siege=1)`
  vise le siège 1. Rouge sur HEAD : `TypeError: MoveTo() got an unexpected
  keyword argument 'siege'`.
- [x] `cas_rejeu_geste_avec_siege` : geste avec `siege=1`, annulation d'un
  autre geste ; le rejeu replace la carte chez le siège 1 après la rotation.
- [x] Si question 4 = A : `cas_evenement_en_resolution_du_joueur` (rouge :
  zone inconnue).
- [x] `cas_allie_pose_agit_apres_reprise` : allié posé à la main,
  `/manuel_reprise heros`, une option d'attaque de cet allié existe.
- [x] `cas_amelioration_posee_modifie_apres_reprise` (rouge jusqu'au correctif `EventManager.ReconcilierApresSilence` du 06/10/2026, puis vert) : `Attach` d'une
  amélioration +1 ATQ, reprise, l'attaque vaut +1.
- [x] `cas_reprise_avec_evenement_en_resolution` : décide entre gate et
  avertissement avant de garder l'option A de la question 4.
- [x] `cas_deux_gestes_meme_carte` : deux `MoveTo` de la même carte vers deux
  zones ; établir lequel gagne.
- [x] `test_mode_manuel.py` complet (65/65). Batterie comparée à HEAD : REPORTÉE à la fin des lots moteur (décision du 06/10).

### 2b. Plateau
**Fichiers :**
- nouveau `ui-app/src/board/manuel/poser-en-jeu.ts` : fonction pure (type,
  identité, siège) vers une commande ou un refus nommé (table D.3) ;
- `board/manuel/glisser-manuel.ts` : ordre D.2 (règle 0 incluse), `accepte`,
  libellés nommés, sbire engagé par `MoveTo`, commentaire `:1-8` corrigé ;
- `board/glisser/useGlisser.ts:165-207` : champ `surLaTable` ;
- `board/Board.tsx` : `ReglagesGlisser.accepte` (`:886-900`), `depotRefuse`
  (`:1103-1110`), cadre (`:1137`) selon la question 12 ;
- `board.tsx:2708-2711` : passer le monde, le nom français, le siège d'origine ;
- `board/triche.ts:99-117` : paramètre `siege` optionnel ;
- commentaire `zones.ts:868-873` (« joueur COURANT » devient « premier joueur
  du moment, ordre qui tourne »).

**Tests (rouge d'abord) :**
- [x] `poser-en-jeu.test.ts` : une ligne par type de D.3, **tous** les types
  de `game/card/face/card_type/` nommés ; cas d'erreur : type inconnu = refus ;
  cas limite : amélioration sans identité en jeu = refus.
- [x] `glisser-manuel.test.ts` :
  - allié lâché sur `terrain-soutien`, `terrain-combat` ou `surLaTable` :
    `MoveTo(..., 'AlliesArea', ...)`. Rouge sur HEAD : « Lâche la carte sur une
    pile » ;
  - la pile gagne toujours ; Maj sur une pile donne `Bottom` ;
  - événement lâché sur la manigance principale : pas `MainSchemesArea` ;
  - sbire engagé relâché sur son secteur : aucune commande, ou `MoveTo`
    idempotent, jamais `Engage` ;
  - carte en jeu relâchée sur la table : selon la question 13 ;
  - propriété : `libelle` défini si et seulement si `onDepot` accepte, sur une
    matrice de cibles ;
  - lâcher hors du plateau : refus ;
  - amélioration lâchée sur la table (question 3) : une seule cible possible
    (l'identité) donne `Attach` direct ; plusieurs cibles ouvrent la fenêtre de
    choix, et un choix donne `Attach` sur la carte choisie ; fermer la fenêtre
    n'envoie rien ;
  - étiquette du glisser : aucun coût affiché (question 9).
- [x] Fenêtre de choix de cible (question 3) : réutiliser le patron d'une
  fenêtre de choix existante du plateau ; test du nominal, de la fermeture sans
  choix, et de la liste des cibles (cartes en jeu du joueur qui peuvent porter
  une amélioration).
- [x] Double-clic sur une carte en main (question 8) : même résultat que le
  glisser sur la table, via `poser-en-jeu.ts` ; test rouge puis vert dans
  `clavier-wiring.test.tsx`.
- [x] Test du `Board` : en manuel, pas de rouge sur une pile pleine ; cadres
  selon la question 12.
- [x] Vérifier que `card_type` du descripteur porte bien les noms de classes
  (sinon table de correspondance, testée).

**E2E :**
- [x] Réécrire l'étape 4 (`mode-manuel.spec.ts:245-262`) : la carte lâchée sur
  la table quitte la main et apparaît dans « Héros et soutiens ». Rouge sur
  HEAD.
- [x] Ajouter un lâcher hors du plateau, refusé.

**Navigateur, souris** (1280x720 et 1920x1080 ; partie déclarée manuelle **et**
partie basculée) :
- [x] poser un allié, un soutien, une amélioration, un événement, et une
  ressource (refus). La graine 4321 n'a pas d'allié en main : en faire
  apparaître un avec C, le glisser de la résolution vers la main, puis de la
  main vers la table ;
- [x] glisser la carte du dessus du deck ou de la défausse vers la table
  (vérifier si c'est possible) ;
- [ ] une carte à deux faces : noter la face d'arrivée ;
- [ ] même essai sur une table éclatée (briques), jamais vérifiée
  (`file-d-attente:1652`) ;
- [x] mesurer le délai entre le lâcher et l'apparition de la carte, en solo ;
  le noter dans la fiche (pas de seuil connu à ce jour) ;
- [x] captures et `/get_world` à chaque geste.

**Navigateur, tactile :** non-régression seulement, le doigt reste attendu en
échec jusqu'au lot 4.

**Risques :** le mode Auto ne doit pas changer (`surLaTable` ignoré hors
manuel) ; sur une table éclatée, les groupes portent le `data-zone` de leur
origine (`Board.tsx:453`) ; la limite d'alliés n'est plus contrôlée (voulu) ;
`minion.py:104-110` à l'entrée chez les engagés est SUPPOSÉ sans effet
(messages fermés).

**Fin :** les cinq types de cartes joueur se posent à la souris dans une vraie
partie, captures à l'appui ; journal nommé ; vitest, typecheck, e2e verts ;
batterie sans nouvel échec.

## Lot 3 : le dire au joueur (P1)

**Fichiers :**
- `board/manuel/VoletAideManuel.tsx` : texte D.12, statuts Sonné, Désorienté,
  Tenace, ligne du clic droit sur la table ;
- `board/MenuTriche.tsx` : entrée « Poser en jeu » branchée sur
  `poser-en-jeu.ts`, titre en français, défilement du sous-menu
  « Déplacer vers » ;
- `CoucheTriche.tsx:497-503` : libellés des statuts ;
- mise en page de la main à 720 px (mesurer la boîte face à son contenu, pas
  seulement le débordement).

**Tests (rouge d'abord) :**
- [x] `VoletAideManuel.test.tsx` trouve « Paie », « Glisse la carte de ta
  main », « Lâche sur une carte », « Clic droit sur une carte » ;
- [x] `menu-manuel.test.tsx` : « Poser en jeu » présent sur une carte en main,
  absent sur une carte en jeu ;
- [x] le titre du menu est le nom français.
- [ ] Mise en page de la main à 720 px et défilement du sous-menu « Déplacer
  vers » : REPORTÉS au passage navigateur final (décision du 06/10 : plus de
  navigateur par lot ; le menu a déjà `max-height` + `overflow-y: auto`,
  `board.css:7128`, seule une mesure dira s'il manque quelque chose).

**Navigateur :** captures de l'aide et du menu à 720 et 1080 px ; le
sous-menu atteint sa dernière entrée.

**Fin :** les tests ci-dessus verts ; capture de l'aide à 720 px sans texte
coupé.

## Lot 4 : tactile (P2)

**Préalable :** question 11.

**Fichiers :**
- `board/glisser/glisser.css` et la classe du cadre en manuel :
  `touch-action: none` sur `.scan-card` seulement ;
- `CoucheTriche.tsx` : appui long qui ouvre le menu (`APPUI_LONG_MS`,
  `mobile/useAppuiLong.ts:23`). Un déplacement de plus de `SEUIL_GLISSER`
  (6 px, `useGlisser.ts`) annule l'appui et devient un glisser ;
- `mobile/PlateauPortrait.tsx` : appui long qui ouvre le menu en manuel.

**Tests :**
- [x] unitaire de la décision « appui long ou glisser » (fonction pure) ; `manuel/appui-tactile.test.ts` + câblage `manuel/appui-long-menu.test.tsx` (rouge : « Unable to find … Incliner »), cadre `data-glisser-doigt` (`glisser/geste.test.tsx`) ;
- [x] `PlateauPortrait.test.tsx` en manuel (rouge : « spy … called 1 times » : le portrait agissait aussi) ;
- [ ] e2e en émulation `hasTouch` à 1024x768 puis 390x844 (REPORTÉ au passage navigateur final, décision du 06/10).

**Navigateur :** gestes du lot 2 au doigt. Résultat sur un vrai appareil :
SUPPOSÉ, à faire vérifier par l'utilisateur.

**Risques :** défilement horizontal de la main bloqué ; pas de `contextmenu`
sur iPad (couvert par la minuterie) ; zoom au double tap ; conflit avec
l'aperçu au survol.

**Fin :** `manuel-22` à `manuel-28` rejoués en émulation donnent le résultat
attendu.

## Lot 5 : plusieurs héros et multijoueur (P2)

**Préalables :** questions 6, 7, 14.

**Fichiers :**
- `zones.ts` (`proprietaires` pour `terrain-combat` aussi) et
  `Board.tsx:441-456` : `data-joueur` sur `.plateau-groupe` ;
- `useGlisser.ts` : lire ce `data-joueur` ;
- `MenuTriche.tsx` : « Déplacer vers » avec `siege` ;
- `CoucheTriche.tsx:428-491` : en manuel, piocher par
  `MoveTo(..., 'HandsArea', siege)` au lieu de `Gain` ;
- `CoucheTriche.tsx:569-603` : F12 et Ctrl+Q pour tous les héros si la
  question 7 donne A, cartes dans la main de leur propriétaire ;
- `glisser-manuel.ts` : `estSource` selon la question 14.

**Moteur :** rien de plus que le lot 2a.

**Tests :**
- [x] cas moteur `cas_piocher_chez_le_proprietaire` : hypothèse CONFIRMÉE, rouge avec `PIOCHE_COMMANDE=gain` (« la carte piochee n'est pas arrivee dans la main du siege 1 »), vert avec `MoveTo(..., 'HandsArea', siege=1)` ;
- [x] vitest : un lâcher sur un groupe `data-joueur=1` donne `siege=1` (`glisser/useGlisser.test.ts`, `glisser/geste.test.tsx`, `zones-proprietaires-combat.test.ts`, `manuel/glisser-manuel.test.ts`) ;
- [x] F12 avec deux héros : lignes et cartes pour les deux (`manuel/plusieurs-heros.test.tsx`, rouge : « [Array(2)] » au lieu de quatre commandes) ;
- [x] une carte face cachée ou piochée chez un autre n'est jamais nommée au
  journal : en ligne, la question 14 interdit toute pioche dans la pile d'un autre (menu, touche, double-clic refusés, `plusieurs-heros.test.tsx`) ; à une même table, tous les héros sont au même joueur.

**Navigateur :**
- [ ] solo à deux héros, sélecteur sur le héros 2 : poser, Suppr, Ctrl+D, F12
  arrivent chez le héros 2 ;
- [ ] en ligne : deux contextes sur deux sièges (patron de
  `ui-check/tests/bascule-salon.spec.ts`) plus un spectateur ; mesurer en
  combien de temps l'autre joueur voit le geste (mécanisme de rafraîchissement
  à identifier, SUPPOSÉ).

**Fin :** aucune carte n'arrive chez le mauvais héros, même après rotation du
premier joueur.

## Lot 6 : gestes OCTGN restants (P3)

**Préalable :** question 10. Un sous-lot par geste, chacun rouge puis vert :
- [x] Maj pendant le glisser sur la table : face cachée (`MoveTo(..., face_cachee=True)`, cas `poser_face_cachee`, rouge : carte jamais arrivée) ;
- [x] double-clic sur une manigance (retourne ; le moteur repose déjà la menace, cas témoin `manigance_retournee_pose_sa_menace`) ;
- [x] Ctrl+U et Ctrl+Maj+U (face cachée, à côté du héros ou en résolution Rencontre) ; Ctrl+F sur une pile (retourne le dessus) ;
- [x] F1 (menu de la carte) et Maj+F1 (efface le marqueur naturel) ; Ctrl+I NON PORTÉ : l'aperçu au survol montre déjà la carte ;
- [x] mulligan (`Puzzle.Mulligan`, une commande) et défausse au hasard (menu de la table) ; échange avec le dessus du deck (`Puzzle.SwapWithDeckTop`, menu d'une carte en main) ;
- [x] F12 complet : excédent (fenêtre), `Puzzle.DrawUpToHandSize` (remélange si deck vide), « Fin du round » au menu de la table (`Puzzle.EndRound`) ;
- [x] sélection multiple : NON PORTÉ, volontaire (aucune demande, gestes déjà un par carte) ;
- [x] touche Menu ou Maj+F10 pour le menu d'une carte, bulle de refus annoncée (`role="status"`, couche plus `aria-hidden`) ;
- [x] touches maison F, Q, R, chiffres (question 10 = A) ; un chiffre BLESSE aussi héros et méchant, et Maj n'y change rien (AZERTY) ;
- [x] « Remélanger la défausse » en une seule commande moteur (`Puzzle.ShuffleDiscardIntoDeck`, par siège) ;
- [x] refus moteur pour `Heal`, `Damage`, `Counter`, `Token` sur une carte
  incompatible, en manuel seulement (cas `refus_jetons_carte_incompatible`). Suppr sur Permanent/Victoire : NON TRAITÉ (batterie reportée).

**Fin :** la liste « non porté » de la mémoire `raccourcis-octgn-source.md`
est vide, ou chaque entrée restante est marquée « non applicable ».

## Lot 7 : critère global, documentation, déploiement

- [x] **Un round complet joué à la main** dans un navigateur (phase des héros,
  F12, phase du méchant, carte Rencontre, F12 de fin de round), sans aucun
  geste qui fasse avancer le moteur. Noter la liste des gestes utilisés dans
  la fiche, captures à l'appui.
- [ ] Mettre à jour la spec du 18/09 et les fiches (annotations du 06/10
  devenues fausses).
- [ ] Entrée « nouveautés ».
- [ ] Déployer sur « déploie » seulement, puis file d'attente.

### Restes du passage navigateur final (« Tu corriges tout », 06/10/2026)
- [x] Compteur de rounds en partie DÉCLARÉE manuelle : `round_id` compte le
  round en cours dès la fin de la mise en place (1), « Fin du round » le fait
  avancer, et une reprise en phase héros ou méchant joue CE round sans en
  compter un de plus (`world.py`, `OnGameLoop`). Cas `round_partie_declaree`
  et `round_reprise_nouveau_tour` (rouges : « round_id=0, attendu 1 »).
- [x] Fenêtre de choix d'une amélioration : propose aussi le méchant et les
  sbires engagés (`poser-en-jeu.ts`, `contexteDePose`). Le méchant étant
  toujours là, elle s'ouvre pour toute amélioration lâchée sur la table.
- [x] Glisser une pile (écart 32) : vu marcher au navigateur ; une pièce
  jointe (Attachment) lâchée sans hôte va en résolution au lieu d'un refus.
- [x] Volet d'aide : ne s'ouvre seul que sur PC (`ECRAN_SANS_AIDE_AUTO` =
  `(max-width: 1099px), (pointer: coarse)`, `VoletAideManuel.tsx`).
- [x] Téléphone : une carte ouverte pour une action se referme quand l'action
  disparaît (`PlateauPortrait.tsx`), plus de « Utiliser cette carte » périmé
  après le mulligan.
