# Mode manuel joué comme sur OCTGN : poser une carte, et le reste (06/10/2026)

> **Mise à jour du 07/10/2026 (audit du backlog)** : L'en-tête « PLANIFIÉ, RIEN CODÉ » est PÉRIMÉ : les lots 0 à 7 sont faits, commités (`59759beb`, `7907eb5b`) et déployés le 06/10 (`56349b00`). RESTE : table éclatée et carte à deux faces non vérifiées en vraie partie ; l'amélioration à cibler ne propose pas les ennemis (question en suspens) ; glisser le dessus d'une pile (écart 32) ; volet d'aide à 1024 et 390 px qui couvre la main.

**Statut : PLANIFIÉ, RIEN CODÉ.**

Demande de l'utilisateur : « pour le mode manuel, ça va pas vraiment, comment
on fait pour poser une carte ? je peux pas la drag n drop. Comment ça se joue
sur OCTGN ? Vérifie tout, planifie tout, mais ne code pas. »

- Spec (guide OCTGN, état actuel, cause, écarts, conception) :
  `docs/superpowers/specs/2026-10-06-mode-manuel-comme-octgn-design.md`
- Plan (lots 0 à 7) : `docs/superpowers/plans/2026-10-06-mode-manuel-comme-octgn.md`
- Complète : `.planning/todos/2026-10-05-facon-de-jouer-manuel-octgn.md` et
  la demande « Finir le mode manuel » de la file d'attente.

## En bref

- **OCTGN** : on glisse la carte de sa main et on la lâche n'importe où sur la
  table ; on paie soi-même (Suppr sur une carte de la main, double-clic pour
  incliner). Source : plugin Ouroboros009 0.0.3.97.
- **Chez nous, la cause** : la table n'est pas une cible du glisser manuel.
  `PILE_PAR_ZONE` (`ui-app/src/board/manuel/glisser-manuel.ts:67-89`) ne
  contient ni `terrain-soutien` ni `terrain-combat`, donc `onDepot` renvoie
  « Lâche la carte sur une pile » (`:157`). Retrait décidé par l'agent de la
  tâche 5 du 18/09, jamais par l'utilisateur.
- **Contournement aujourd'hui** : clic droit sur la carte, « Déplacer vers… »,
  « Alliés » ou « Soutiens ». Une amélioration : la lâcher sur la carte du
  héros (l'étiquette rouge ment, le geste réussit).

## Arbitrage remonté d'un rapport hors git

`.superpowers/sdd/2026-09-18-mode-manuel-plateau/task-5-report.md:165-180`
(ignoré par git) : l'agent a retiré le terrain des cibles du glisser parce que
ces emplacements « mélangent des cartes posées d'origines différentes » et
qu'il craignait de viser le mauvais joueur. Ce plan revient sur ce choix,
d'où les questions 1, 6 et 13.

## Questions ouvertes

Une à la fois, en multichoix, « Autre (précise) » en dernier. Ordre : règles
d'abord. Les questions marquées « lot 2 » bloquent le cœur du travail ; le
lot 1 n'attend que la question 8.

1. **(lot 2) Tu lâches une carte de ta main sur la table, pas sur une pile. Où va-t-elle ?**
   - A (Recommandé) Selon son type, où que tu la lâches. Ex. : Héliporteur lâché n'importe où entre Rhino et ta main arrive dans « Héros et soutiens ».
   - B Selon la zone visée : « Alliés… » donne un allié, « Héros et soutiens » un soutien, ailleurs refus.
   - C Tout va dans Soutiens, tu ranges ensuite avec « Déplacer vers ».
   - Autre (précise)
2. **(lot 2) Une carte lâchée sur une autre carte en jeu :**
   - A (Recommandé) Elle s'attache seulement si c'est une amélioration ou un attachement ; sinon elle se pose selon son type. Ex. : un allié lâché sur Peter Parker va dans Alliés.
   - B Elle s'attache toujours (actuel). Ex. : un allié se glisse sous Peter Parker.
   - C Jamais d'attache par glisser, l'attache passe par le menu.
   - Autre (précise)
3. **(lot 2) Une amélioration lâchée sur la table, pas sur une carte :**
   - A (Recommandé) Elle s'attache à ton identité. Ex. : Lance-Toile lâché n'importe où se glisse sous Peter Parker.
   - B Elle se pose à plat dans Soutiens.
   - C Refus : « Lâche-la sur la carte qu'elle améliore ».
   - Autre (précise)
4. **(lot 2) Un événement lâché sur la table :**
   - A (Recommandé) Il se pose à côté de ton héros, en cours de résolution ; tu appliques l'effet, puis Suppr (comme sur OCTGN). Petit ajout moteur, batterie complète.
   - B Il part directement dans ta défausse.
   - C Il va dans la zone de résolution du méchant, derrière Rhino (comme le catalogue).
   - Autre (précise)
5. **(lot 2) Une carte qui arrive en jeu à la main : le moteur pose-t-il seul ses marquages imprimés ?** Aujourd'hui il pose déjà Uses et Tenace (Lance-Toile arrive avec 3 jetons Toile).
   - A (Recommandé) Oui, comme OCTGN : on garde, on ajoute la menace de départ d'une manigance annexe et les PV, et on l'écrit dans la spec.
   - B On garde seulement Uses et Tenace.
   - C Silence total : on retire aussi Uses et Tenace (tu poses 3 jetons avec →).
   - Autre (précise)
6. **(lot 5) Plusieurs héros : chez qui va une carte posée ?**
   - A (Recommandé) Chez le héros du groupe où tu la lâches ; dans le vide, chez le héros d'où elle vient. Ex. : l'allié de Captain Marvel glissé depuis sa main arrive chez elle.
   - B Toujours chez le héros affiché par le sélecteur.
   - Autre (précise)
7. **(lot 5) F12 et Ctrl+Q avec plusieurs héros :**
   - A (Recommandé) Pour tous les héros, comme OCTGN. Ex. : à deux héros, F12 redresse et fait piocher les deux.
   - B Pour le héros affiché seulement (actuel).
   - Autre (précise)
8. **(lot 1) Double-clic sur une carte de ta main :**
   - A (Recommandé) Rien, comme OCTGN. Aujourd'hui la carte est retournée en secret dans le moteur.
   - B Il pose la carte en jeu (raccourci maison). Ex. : double-clic sur Héliporteur, il va dans Soutiens.
   - Autre (précise)
9. **(lot 2) Aide au paiement :**
   - A (Recommandé) Rien d'automatique, mais l'étiquette rappelle le coût. Ex. : « Poser en jeu : Héliporteur (Soutiens), coût 3 ».
   - B Rien du tout, comme OCTGN.
   - C Une fenêtre « Payer » où l'on coche les cartes à défausser (contraire à la spec du 18/09, ligne 38).
   - Autre (précise)
10. **(lot 6) Touches maison F, Q, R et chiffres.** Le 05/10 tu as décidé qu'elles s'ajoutaient à OCTGN ; le commit `5b88d9a2` les a retirées sans décision tracée.
    - A (Recommandé) Les remettre en plus d'OCTGN, comme décidé. Ex. : Q incline, F retourne, R mélange, 3 sur un sbire pose 3 dégâts.
    - B Les laisser retirées et corriger la fiche du 05/10.
    - Autre (précise)
11. **(lot 4) Au doigt (tablette, téléphone) :**
    - A (Recommandé) Glisser au doigt comme à la souris, appui long pour le menu du clic droit. Ex. : sur iPad, maintenir le doigt sur Héliporteur ouvre « Poser en jeu / Déplacer vers… ».
    - B Appui long pour le menu seulement, pas de glisser au doigt.
    - C Plus tard : la souris seulement pour l'instant.
    - Autre (précise)
12. **(lot 2) Pendant le glisser, qu'est-ce qu'on entoure ?**
    - A (Recommandé) Tout ce qui acceptera la carte : la table d'un seul cadre, le deck, la défausse.
    - B Rien, comme OCTGN (intention d'origine du code).
    - C Garder tel quel (main et manigance seulement).
    - Autre (précise)
13. **(lot 2) Tu reprends une carte déjà en jeu et tu la relâches ailleurs sur la table :**
    - A (Recommandé) Rien ne se passe (aucun geste, rien au journal), sauf sur une pile ou chez un autre héros. Ex. : je glisse le sbire de Spider-Man vers Captain Marvel, il passe chez elle.
    - B Elle est re-rangée selon son type (un geste au journal, même si elle ne bouge pas).
    - C Refus : « Cette carte est déjà en jeu ».
    - Autre (précise)
14. **(lot 5) En ligne, un joueur peut-il bouger les cartes d'un autre ?**
    - A Oui, table libre pour tous (actuel).
    - B Non, comme OCTGN : seulement ses propres cartes.
    - C Oui pour les cartes Rencontre, non pour les cartes d'un autre joueur.
    - Autre (précise)

Pas de recommandation pour la question 14 : la table libre (A) suit nos
décisions du 05/10, la règle d'OCTGN (B) suit « que ça match à 100 % ».

## Réponses

Toutes données le 06/10/2026, une à une.

1. Carte lâchée sur la table : **A, selon son type**, où qu'on la lâche.
2. Lâchée sur une carte en jeu : **A, attache seulement une amélioration ou un attachement** ; sinon pose selon le type.
3. Amélioration lâchée sur la table : **Autre** : « propose sur qui on veut l'attacher, si c'est possible de l'attacher sur quelque chose d'autre ». Donc : une fenêtre propose les cartes en jeu qui peuvent la recevoir ; s'il n'y a qu'une cible possible (l'identité), elle s'y attache directement.
4. Événement : **A, posé à côté du héros en cours de résolution**, puis Suppr l'envoie en défausse (ajout moteur, batterie complète).
5. Marquages à l'arrivée : **A, comme OCTGN** (Uses, Tenace, plus menace de départ d'une manigance annexe et PV).
6. Plusieurs héros : **A, chez le héros du groupe visé** ; dans le vide, chez le héros d'où vient la carte.
7. F12 et Ctrl+Q : **A, pour tous les héros**.
8. Double-clic en main : **A ET B** : on supprime le retournement secret actuel, et le double-clic POSE la carte en jeu selon son type (raccourci maison, en plus d'OCTGN).
9. Paiement : **B, rien du tout**, comme OCTGN (pas de rappel du coût dans l'étiquette).
10. Touches maison F, Q, R et chiffres : **A, on les garde en plus de celles d'OCTGN**.
11. Tactile : **A, glisser au doigt et appui long** pour le menu.
12. Surbrillance pendant le glisser : **A, tout ce qui accepte la carte**.
13. Carte déjà en jeu relâchée sur la table : **A, rien**, sauf sur une pile ou chez un autre héros.
14. Multijoueur : **B, comme OCTGN** : chacun ne bouge que ses propres cartes ; les cartes Rencontre sont à tous.

⚠ Les réponses 3, 8, 9 et 14 s'écartent de la recommandation écrite dans la spec et le plan : ce sont ELLES qui font foi (sections alignées le 06/10/2026).

## Avancement

- 06/10/2026 : audit (code, navigateur, docs, plugin OCTGN), spec, plan et
  cette fiche écrits. Docs existantes annotées. **Aucune ligne de code
  modifiée, rien commité, rien déployé.**
- Captures du navigateur : dans un dossier temporaire de la session ; à copier
  dans `.planning/captures-manuel-2026-10-06/` si on veut les garder (non fait).
- 06/10/2026 : les 14 questions sont tranchées (section « Réponses ») ; la spec
  et le plan sont alignés sur les réponses 3, 8, 9 et 14.
- 06/10/2026 (matin) : **lots 0 et 1 FAITS, non commités.**
  - Lot 0 : `ui-check/tests/mode-manuel.spec.ts` étape 5 passe de « 3 » à une
    flèche Bas (1 PV exactement). Rouge sur HEAD : « le vilain n'a pas
    visiblement encaissé les dégâts ». Vert : 2 tests, 39 s. Commande :
    `export UI_CHECK_BASE=http://127.0.0.1:2361 WSLENV=UI_CHECK_BASE` puis
    `cd ui-check && npx playwright test tests/mode-manuel.spec.ts --project=pc`
    (moteur d'essai sur 2361, cache `.game-essai-312`, supprimés ensuite).
  - Lot 1 : table basculée en Manuel = plus de bouton « Fin du tour »
    flottant, E muet, aucune carte surlignée, « ↶ Annuler » et U défont le
    dernier geste (`/manuel_undo`), double-clic en main sans effet, glisser
    refusé au spectateur. Moteur : Ctrl+Z sur une partie basculée garde
    Manuel (la cause était une trame non republiée, pas la garde
    `mise_en_place_finie`) ; `/post` refuse une réponse (409) pendant la pause.
  - Vérifié : vitest 2629/2629, tsc propre, `test_mode_manuel.py` 57/57,
    e2e manuel vert, essai navigateur du lot 1 vert (captures
    `lot1-basculee.png`, `lot1-apres-annuler.png` dans le scratchpad).
  - **Batterie `test_capacites` complète REPORTÉE** à la fin de tous les lots
    moteur (décision de l'utilisateur du 06/10) : elle a été lancée puis
    arrêtée. Fichiers moteur partagés touchés à couvrir alors :
    `game/game_run/game_session.py`, `engine/device/web/server/server_sync.py`.
  - ⚠ Le moteur d'essai a écrit `Fusion/marvel-lcg-src/replays/save_auto.json`
    (10:04) : même dossier que le jeu local, la sauvegarde automatique de la
    partie locale a été remplacée.
- 06/10/2026 (après-midi) : **lot 2 FAIT, non commité, non déployé.** On pose
  une carte de la main en la lâchant n'importe où sur la table, comme sur OCTGN.
  - Moteur (`puzzle.py`) : `siege=` sur `MoveTo`/`Shuffle`/`Engage` (rang dans
    l'ordre des SIÈGES, stable, au lieu du premier joueur du moment) et zone
    `PlayerProcessingArea` (événement posé à côté de son héros).
  - Plateau : `manuel/poser-en-jeu.ts` (table D.3, une gate : tout type inconnu
    refusé), `glisser-manuel.ts` réécrit (ordre D.2), `surLaTable` dans
    `useGlisser`, `accepte`/`accueilleLaTable` dans `Board`, fenêtre
    `ChoixCibleAmelioration` (question 3), double-clic en main = pose
    (question 8), cadres sur la table entière et les piles (question 12).
  - Vérifié : `test_mode_manuel.py` 65/65 (8 cas nouveaux, rouges sur le
    `puzzle.py` de HEAD), vitest 2692/2692, tsc propre, e2e `mode-manuel.spec.ts`
    2/2 (rouge sur l'ancien build : « Poser en jeu » absent). Navigateur à 1280
    et 1920, partie déclarée ET partie basculée : allié, soutien, amélioration
    (seule cible : attache directe ; deux cibles : fenêtre), événement,
    ressource refusée, double-clic, carte déjà en jeu immobile, dessus du deck
    refusé. Délai lâcher → carte posée : 54 à 282 ms en solo. Captures
    `lot2-*.png` du scratchpad.
  - Trouvé et corrigé en route : la bulle de refus sortait de l'écran près d'un
    bord ; le cadre de table (`outline`) était peint SOUS la scène ; le dessus
    du deck, face cachée, trahissait son type (« Une ressource… ») ; une carte
    EN MAIN passait pour « face cachée » (la trame marque `is_face_up: false`
    les cartes en main).
  - ⚠ **ÉCART MOTEUR PROUVÉ, NON CORRIGÉ** (à trancher par l'utilisateur) :
    une amélioration attachée en manuel ne compte pas après la reprise en Auto
    (Captain Marvel's Helmet : DEF 1 au lieu de 2). Cause : les capacités
    constantes s'arment sur `WhenCardEnterPlay`, que la porte du silence ferme
    (`event/manager.py`, `BroadcastMessage`) ; rien ne les réarme à la reprise.
    Touche aussi les cartes posées pendant une pause basculée. Témoin rouge :
    `test_mode_manuel.py ... amelioration_posee_modifie_apres_reprise` (hors
    suite par défaut).
  - Non vérifié : carte à deux faces (face d'arrivée), table éclatée (briques),
    tactile (attendu en échec jusqu'au lot 4). À 1280 px, le volet d'aide
    ouvert couvre la fin de la main (constat, lot 3).
  - Batterie `test_capacites` toujours REPORTÉE ; à couvrir alors aussi
    `game/puzzle/puzzle.py`.
- 06/10/2026 (fin d'après-midi) : **écart moteur CORRIGÉ, lot 3 FAIT**, non
  commités, non déployés.
  - Moteur : `EventManager.ReconcilierApresSilence` (`game/event/manager.py`).
    La porte du silence note qu'elle a jeté des messages ; au premier message
    qui la repasse rouverte (fil du jeu, jamais le fil HTTP), les capacités
    `arme_en_jeu` (`WhileValid`, `WhenEvent`, marquées dans `on_while.py`)
    sont remises d'accord avec la table : armées si leur carte est en jeu sans
    l'être, désarmées si elle est sortie ou retournée, recalculées sinon.
    AUCUN `WhenCardEnterPlay` n'est envoyé : les effets d'entrée en jeu ne
    repartent pas. Champs ajoutés : `Ability.arme_en_jeu`,
    `Effect.en_jeu_arme/en_jeu_desarmer/en_jeu_rafraichir`.
  - Tests moteur : `amelioration_posee_modifie_apres_reprise` réintégré à la
    suite par défaut (rouge « DEF 1 avant, 1 apres reprise », puis vert) ;
    témoin `entree_en_jeu_pas_relancee_a_la_reprise` (Hawkeye 01066 garde ses
    2 flèches posées à la main ; rouge par substitution « 6 trouvees » si la
    réconciliation relançait l'entrée en jeu). `test_mode_manuel.py` 67/67
    (un artefact de port, `port=42050` occupé, rejoué vert sur un autre port).
  - Lot 3 : « Poser en jeu » en tête du menu d'une carte EN MAIN (même geste
    que le glisser et le double-clic), titre du menu en français
    (`nomAffiche`), aide « Jouer une carte » en tête (texte D.12 adapté aux
    réponses 3, 8, 9), statuts renommés Sonné, Désorienté, Tenace (aide et
    journal du clavier), clic droit sur la table complet ; anglais ajouté dans
    `dico-en.ts`. 4 tests ajoutés, vus rouges puis verts.
  - Vitest 2695/2696 : le seul rouge (`boutons-bd.test.ts`, « ne touche QUE
    les panneaux de question ») vient d'un AUTRE travail : `boutons-bd.css`
    modifié à 12 h 16 (`zoom: 1.5` dans un `@media`), à trancher par son
    auteur. ⚠ Il s'ajoute au bloc « tout 1,5 fois » de `board.css` : les
    boutons de fin de tour risquent d'être agrandis deux fois (x2,25).
  - Reporté au passage navigateur final : main à 720 px, défilement du
    sous-menu « Déplacer vers » (le menu a déjà `overflow-y: auto`).
  - Batterie `test_capacites` toujours REPORTÉE ; fichiers moteur partagés à
    couvrir alors : `game/event/manager.py`, `game/ability/factory/on_while.py`,
    `game/ability/ability.py`, `game/effect/effect.py`, en plus de ceux des lots
    1 et 2.
- 06/10/2026, lot 4 (tactile) FAIT, non commité : appui long au doigt = menu
  du clic droit (minuterie dans `CoucheTriche.tsx`, décision pure
  `manuel/appui-tactile.ts`, un déplacement de 6 px l'annule et devient un
  glisser) ; `touch-action: none` sur les cartes en manuel
  (`data-glisser-doigt`, `glisser.css`) ; le portrait n'agit plus à l'appui
  long en manuel. `boutons-bd.test.ts` réglé par le parent (test du `@media`) ;
  le x2,25 n'existe plus (bloc bouton de `board.css` retiré). Vitest 2712/2712,
  tsc propre. Navigateur reporté (voir la liste du passage final).
- 06/10/2026, lot 5 (plusieurs héros et multijoueur) FAIT, non commité :
  - `manuel/proprietaire.ts` : à qui est une carte (zones de cartes de
    joueur ; Rencontre à tous), sièges tenus par l'écran (tous à une même
    table, le sien en ligne).
  - Chaque groupe porte `data-joueur` (ligne de combat comprise,
    `zones.ts`) ; la carte lâchée va chez le héros du groupe visé, dans le vide
    chez son propriétaire (question 6). Piles de joueur visées par siège
    (glisser et « Déplacer vers »).
  - Pioche (chiffres, Ctrl+D, pile ouverte, F12) en manuel par
    `MoveTo(..., 'HandsArea', siege)` : `Gain` donnait au joueur courant
    (cas moteur `piocher_chez_le_proprietaire`, rouge avec Gain).
  - F12 et Ctrl+Q pour tous les héros de l'écran (question 7).
  - Question 14 : en ligne, glisser, menu, touches et double-clic refusés sur
    la carte d'un autre joueur.
  - Vitest 2732/2732, tsc propre. Aucun fichier moteur modifié (seul
    `tools/test_mode_manuel.py` gagne un cas).
- 06/10/2026, lot 6 (gestes OCTGN restants) FAIT, non commité :
  - Moteur (`puzzle.py`) : `MoveTo(face_cachee=)`, `ShuffleDiscardIntoDeck`,
    `SwapWithDeckTop`, `Mulligan`, `DrawUpToHandSize`, `EndRound`, refus en
    manuel de `Damage`/`Heal`/`Counter`/`Token` sans effet. 8 cas ajoutés à
    `tools/test_mode_manuel.py`, chacun vu rouge (sauf le témoin manigance).
  - Plateau : touches maison remises (F, Q, R, chiffres), double-clic sur une
    manigance, Ctrl+F et Ctrl+U sur une pile, Maj en glissant = face cachée,
    F1 / Maj+F1, touche Menu et Maj+F10, mulligan, défausse au hasard,
    échange avec le dessus du deck, F12 complet (fenêtre d'excédent), « Fin
    du round », remélange en une commande, mélange par siège, bulle de refus
    annoncée, aide et anglais à jour.
  - Non porté, volontaire : Ctrl+I, sélection multiple.
  - Vitest 2759/2759, tsc propre. Batterie `test_capacites` toujours
    REPORTÉE (`puzzle.py` encore modifié).
- Prochaine étape : passage navigateur final et batterie, puis lot 7.
- 06/10/2026 (hors plan, demande de l'utilisateur) : fenêtre de fin de tour et
  mulligan agrandies x1,5 (`board.css`), boutons de toutes les fenêtres du
  centre x1,5 (`zoom` dans `boutons-bd.css`, pas sous 561 px). Vérifié au
  navigateur à 1280 et 1920 (captures `boutons15-*`) : rien ne déborde. Seul
  défaut : à 1280x720 la question « Sens d'Araignée » (655 px) montait sous la
  barre ; corrigé en centrant la phase sous la barre (`cartouche-phase.css`,
  fin de fichier). **À revoir au passage navigateur final.** Constaté hors
  mission : un `/sandbox_command` qui ouvre une question pendant le mulligan
  fige la partie (Maria Hill, `ChangeForm`), outil de test seulement.
- 06/10/2026 (lot 7, batterie) : `test_capacites` complète **2662/2667**. Les
  5 échecs sont les préexistants connus : sg006, sg007, sg009, sg013 (Squirrel
  Girl, mêmes messages que sur HEAD le matin même) et « statistiques »
  (`statistics.json` cumulé ; vert seul avec un fichier propre). Aucune
  régression des lots 0 à 6. Jouée sur un dossier dédié `.game-src-l7` (les
  `.game-src-parN` étaient pris par une autre session), supprimé ensuite.
- 06/10/2026, lot 7, PASSAGE NAVIGATEUR FINAL fait (moteur d'essai isolé,
  port 2310, sauvegardes redirigées : `save_auto.json`, `statistics.json` et
  `launch.json` intacts). Captures `lot7-*.png` et `mesures.json` dans le
  scratchpad de la session (dossier `lot7/`), non versionnées.
  - Vu marcher : souris 1280x720 et 1920x1080 (poser allié, soutien par
    double-clic, amélioration sur la table avec fenêtre de choix et sur une
    carte, événement puis Suppr, carte déjà en jeu sans geste, refus, face
    cachée, Ctrl+D, Ctrl+U, Ctrl+Q, Annuler/U/Ctrl+Z sans repasser en Auto,
    F12 avec fenêtre « Main trop grande », Fin du round, Mulligan, aide qui
    défile) ; deux héros (carte posée chez le héros visé, Ctrl+Q et F12 pour
    les deux) ; en ligne (carte de l'autre siège ni glissable ni menu,
    spectateur sans glisser) ; tactile 1024x768 (poser au doigt, appui long
    carte et table) et 390x844 (tiroir « Ta main », appui long, Poser en
    jeu) ; reprise en Auto : le casque posé à la main donne DEF +1 ; fin de
    tour et boutons x1,5 dans l'écran ; Sens d'Araignée à 1280x720 sous la
    barre (y 56 à 711, barre 0 à 47).
  - **Round complet joué à la main** (critère du lot 7), 12 gestes, moteur
    muet du début à la fin : Suppr sur une ressource (payer), glisser un
    allié, F7 sur le héros, Bas x2 sur le méchant, fenêtre « Main trop
    grande », F12, F5 sur la manigance, Alt+Entrée (amplification), Bas sur
    le héros, Ctrl+D sur le deck Rencontre (carte en résolution), Suppr sur
    la carte Rencontre, clic droit sur la table puis Fin du round.
  - DÉFAUTS TROUVÉS ET CORRIGÉS (rouge puis vert, tsc propre, vitest
    2764/2764, rejoués au navigateur) :
    1. Appui long au doigt : au lever, le clic de compatibilité tombait sur
       l'entrée du menu sous le doigt (« Défausser ») : tenir une carte la
       défaussait. `CoucheTriche.tsx` avale le lever qui suit (touchend
       annulé, filet sur click). `appui-long-menu.test.tsx` +2 cas.
    2. Menu de la table : hauteur devinée (340 px), sortait de l'écran à 720
       px (« Mulligan », « Terminer la partie » inatteignables). Mesurée comme
       MenuTriche (`MenuTable.tsx`). `MenuTable.test.tsx` +1 cas.
    3. « Déplacer vers » : « Sous la pile » prenait toute la largeur
       (spécificité CSS), noms des piles sur trois lignes (`board.css`).
       `menu-triche-sous.test.ts`.
    4. Barre : « Round 1 Init Finished » (phase brute) en manuel ;
       `libellePhase` muet quand le moteur se tait (spec du 18/09).
       `etat-partie.test.ts` +1 cas.
  - CONSTATÉS, NON CORRIGÉS (à trancher) :
    - Compteur de rounds décalé d'un en partie DÉCLARÉE manuelle : le moteur
      se tait à « Init Finished » (round 0), donc rien n'est affiché pendant
      le premier round et « Fin du round » affiche « Round 1 » au début du
      deuxième (le portrait affiche « Mise en place »). `round_id` y compte
      les rounds FINIS, et `start_round` l'incrémente encore à la reprise :
      le corriger touche la reprise (`world.py:1110`) et le rejeu des gestes.
    - Fenêtre de choix d'une amélioration (question 3) : ne propose que
      l'identité et les alliés, jamais un ennemi (Pris dans la Toile,
      Spider-Traceur). Lâcher la carte SUR l'ennemi marche. Ajouter les
      ennemis ouvrirait la fenêtre pour toute amélioration (le méchant est
      toujours là), casque compris : question pour l'utilisateur.
    - Écart 32 de la spec : la carte du dessus d'une pile ne se glisse pas
      (une pile est un bouton, `useGlisser.ts:92`) ; chemin actuel : survol +
      Ctrl+D ou un chiffre (en résolution pour une pile Rencontre).
    - Volet d'aide ouvert d'office en manuel : à 1024 px il couvre le tiers
      droit, main comprise (un doigt posé dessus défile au lieu de glisser) ;
      à 390 px il couvre tout l'écran et « Chercher une carte » se dessine
      par-dessus son en-tête.
    - Au téléphone, après la mise en place, une carte ouverte « Utiliser
      cette carte / Fermer » recouvre la table (non investigué).
    - Outil de test seulement : `Puzzle.ChangeForm('01001a')` crée une
      seconde Spider-Man sans propriétaire dans les cartes mises de côté ; le
      rendu lève `AssertionError` (`card_face.py:1039`) et le moteur
      s'arrête (journal gardé dans le scratchpad, `lot7-crash-moteur.log`).
  - Aucun fichier moteur modifié par ce passage : la batterie en cours reste
    valable.
- 06/10/2026, RESTES CORRIGÉS (« Tu corriges tout ») ; rien commité, rien
  déployé. Vu au navigateur (moteur d'essai port 2310, sauvegardes
  redirigées ; captures `restes/` du scratchpad) :
  1. Rounds en partie déclarée manuelle : « Round 1 » dès la fin de la mise
     en place, « Round 2 » après « Fin du round » ; une reprise en phase héros
     ou méchant joue le round en cours sans en compter un de plus
     (`world.py`, `OnGameLoop`). Cas `round_partie_declaree` et
     `round_reprise_nouveau_tour`, rouges avant (« round_id=0, attendu 1 ») ;
     quatre anciennes preuves `round_id == 0` remplacées par l'état de phase
     « Init Finished ». `test_mode_manuel.py` 78/78.
  2. Choix de la cible d'une amélioration : le méchant et les sbires engagés
     sont proposés (vu : « Peter Parker », « Rhino », attache sous Rhino).
  3. Glisser une pile (écart 32) : marchait déjà vers la main et vers une
     autre pile (le constat du lot 7 était faux) ; le dessus du deck
     Rencontre lâché sur la table était refusé quand c'était une pièce jointe :
     elle va maintenant en résolution, comme après Ctrl+D (vu : Charge en
     résolution, deck 31 puis 30).
  4. Aide : ne s'ouvre seule que sur PC, critère
     `(max-width: 1099px), (pointer: coarse)` (vu : ouverte à 1280, fermée à
     1024 au doigt, languette présente).
  5. Téléphone : CAUSE, une carte touchée pendant le mulligan s'ouvre avec
     l'action du mulligan, « Garder ma main » reste touchable au-dessus, et la
     carte restait ouverte ensuite avec un bouton vers une question close.
     Correctif : la carte ouverte relit son action à chaque rendu et se
     referme quand l'action pour laquelle elle s'était ouverte disparaît
     (`PlateauPortrait.tsx`). Reproduit puis vu corrigé au navigateur.
  Vitest 2772/2772, tsc propre.
  Batterie `test_capacites` complète (`world.py` est partagé) : 2662/2667,
  les 5 échecs connus (sg006, sg007, sg009, sg013 ; « statistiques » vert
  rejoué seul avec un fichier propre). `statistics.json`, `save_auto.json` et
  `launch.json` identiques (md5) à leur état d'avant.
