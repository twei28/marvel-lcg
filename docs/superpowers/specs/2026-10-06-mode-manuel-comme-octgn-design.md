# Spec : le mode manuel joué comme sur OCTGN

**Date :** 06/10/2026
**Demande :** « pour le mode manuel, ça va pas vraiment, comment on fait pour
poser une carte ? je peux pas la drag n drop. Comment ça se joue sur OCTGN ?
Vérifie tout, planifie tout, mais ne code pas. »
**Statut :** PLANIFIÉ, RIEN CODÉ. Les 14 questions de la fiche
`.planning/todos/2026-10-06-mode-manuel-comme-octgn.md` sont tranchées
(06/10/2026). Là où une option « recommandée » de cette spec diffère d'une
réponse, la réponse fait foi : 3 (amélioration sur la table = fenêtre de choix
de la carte qui la reçoit, attache directe si une seule cible), 8 (double-clic
en main = poser en jeu, plus de retournement secret), 9 (aucune aide au
paiement, pas de coût affiché), 14 (chacun ne bouge que ses cartes, Rencontre à
tous).
**Complète :** `2026-09-18-mode-manuel-design.md` (et son avenant) et les
décisions du 05/10 (`.planning/todos/2026-10-05-facon-de-jouer-manuel-octgn.md`).
Elle ne les remplace pas.
**Plan :** `docs/superpowers/plans/2026-10-06-mode-manuel-comme-octgn.md`.

## Conventions

- **PROUVÉ** : vérifié dans le code à la ligne citée, ou observé dans un
  navigateur (moteur d'essai, Spider-Man contre Rhino, graine 4321, 06/10).
- **SUPPOSÉ** : déduit, jamais observé.
- **[P]** : plugin OCTGN Marvel Champions **0.0.3.97** (30/08/2026),
  https://github.com/Ouroboros009/OCTGN-Marvel-Champions/tree/master/055c536f-adba-4bc2-acbf-9aefb9756046.
  C'est la version distribuée par le fil OCTGN (MyGet `octgngamedirectory`).
  Version lue dans `definition.xml:6`, renvoi vers les issues de ce fork dans
  `scripts/constantsGlobal.py:31`. L'ancien dépôt `twistedsistem` (0.0.3.10,
  avril 2022) est périmé.
- **[O]** : client OCTGN, https://github.com/octgn/OCTGN au commit `eb8bb590`
  (chemins sous `octgnFX/Octgn.JodsEngine/Play/`).
- Chemins du plateau relatifs à `ui-app/src/`, chemins du moteur relatifs à
  `Fusion/marvel-lcg-src/src/`.
- Les captures citées (`manuel-NN-*.png`) ont été prises le 06/10 dans un
  dossier temporaire. Pour les garder, les copier dans
  `.planning/captures-manuel-2026-10-06/` (non fait à ce jour).

## Réponse courte

- **Sur OCTGN**, on pose une carte en la **glissant de sa main et en la
  lâchant n'importe où sur la table**. On paie soi-même : on défausse des
  cartes de sa main (survol puis Suppr) ou on incline une carte en jeu
  (double-clic). Il n'y a ni menu « Jouer », ni double-clic en main. PROUVÉ
  (§A).
- **Chez nous**, ce même glisser est refusé avec la bulle « Lâche la carte sur
  une pile » : la table n'est pas une cible du glisser manuel
  (`board/manuel/glisser-manuel.ts:67-89`, refus en `:157`). Le seul chemin qui
  marche aujourd'hui : **clic droit sur la carte, « Déplacer vers… », puis
  « Alliés » ou « Soutiens »**. PROUVÉ dans un navigateur (§B).
- **Proposition** : lâcher une carte sur la table la met en jeu, rangée selon
  son type (§D). 14 questions restent à trancher une à une (fiche).

---

## A. Comment on joue sur OCTGN (guide pour joueur)

> Lu dans le code de [P] et de [O]. OCTGN n'a pas été lancé.

### A.1 Avant de commencer

- **La table est une surface libre.** Aucune zone n'y est dessinée : le fond
  est une illustration ([P] `definition.xml:170`, `background/playmat2.png`).
  Chacun pose ses cartes dans **sa colonne** (la largeur est partagée entre
  les joueurs), le méchant est en haut ([P] `loadHero.py:179-188`,
  `constantsGlobal.py:34-43`).
- **L'écran.** Ta main est dans le bandeau du bas, dans ton onglet ([O]
  `PlayWindow.xaml:419-420`). Survoler une carte l'affiche en grand ([O]
  `PlayWindow.xaml.cs:754-805`).
- **Trois gestes font presque tout** : glisser, double-cliquer, une touche
  pendant qu'on survole une carte. Le clic droit donne le reste.
- **Le plugin ne vérifie aucune règle et ne paie rien à ta place.**

### A.2 Mise en place

1. **Écran d'accueil** : charger un scénario ou un héros. Le chargement de
   deck standard d'OCTGN est désactivé ([P] `actions.py:292-304`,
   `welcomeScreen.py:8-70`).
2. **Scénario** : l'hôte le charge (méchant, difficultés, modulaires) ([P]
   `loadVillain.py:15-111`).
3. **Héros** : chacun charge le sien, posé dans sa colonne avec ses cartes
   « Setup » ([P] `loadHero.py:285-314`).
4. **Démarrage automatique** quand tout est chargé ([P] `actions.py:427-436`) :
   jeton premier joueur, decks mélangés, mains piochées, obligations ajoutées
   au deck Rencontre.
5. **Mulligan** : clic droit sur la main, « Mulligan Hand » ([P]
   `actions.py:1182-1196`).

### A.3 Jouer une carte de sa main

Exemple : un allié qui coûte 2.

1. **Lire** : survole la carte dans ta main.
2. **Payer** : c'est toi qui comptes. Le plugin ne lit jamais le coût (aucune
   occurrence de `Cost` ni de `Resource_` dans ses scripts, PROUVÉ).
   - une carte de ta main : survole-la puis **Suppr**, elle part dans ta
     défausse ([P] `definition.xml:256`, `actions.py:978-1075`). Ou glisse-la
     sur ta défausse ;
   - une carte en jeu qui produit une ressource : double-clic ou **F7** pour
     l'incliner ([P] `actions.py:325-336`).
3. **Poser** : glisse la carte de ta main et lâche-la sur la table, près de ton
   héros. Elle arrive face visible au point du lâcher, alignée sur une grille
   de 10 ([O] `TableControl.xaml.cs:379-381` ; [P] `actions.py:367-376`).
   Maj enfoncée **pendant** le glisser (après l'avoir commencé) : elle arrive
   face cachée ([O] `CardControl.xaml.cs:911`). Maj enfoncée dès l'appui lance
   le mode « cible », qui n'agit que sur une carte de la table (`:570`, `:662`).
4. **Le plugin complète la carte** si elle vient d'une pile (la main en est
   une), seule, face visible et sous ton contrôle ([P] `actions.py:1510-1520`) :
   compteurs « Uses », statut Tenace, menace d'une manigance, PV d'une
   identité, d'un méchant ou d'un chef.
5. **Le chat** écrit « X moves 'Nom' to Table » ([O] `Move.cs:153-158`).

| Type de carte | Sur OCTGN |
|---|---|
| Allié, soutien | Glissé sur la table près du héros. Les dégâts d'un allié se comptent avec Haut et Bas. |
| Amélioration | Glissée pour chevaucher la carte visée, puis **PgDn** la passe dessous. Aucune notion d'attache ([O] `CardControl.xaml.cs:1104-1111` ; [P] `setup.py:16-34`). |
| Événement | Rien d'automatique : on applique son effet, puis Suppr. L'habitude de le montrer d'abord sur la table est SUPPOSÉE. |
| Ressource | Ne se joue pas : on la défausse pour payer. |

**Ce qui ne pose pas une carte :**
- le double-clic en main ne fait rien : il n'agit que si
  `args.card.group == table` ([P] `actions.py:327`) ;
- la main n'a pas d'action « Jouer » : seulement « Random Discard »,
  « Mulligan Hand », « Switch Card with top Deck Card » et « Discard Card »
  ([P] `definition.xml:252-257`) ;
- un lâcher sur la table n'est **jamais refusé** :
  `e.Handled = e.CanDrop = true` ([O] `TableControl.xaml.cs:381`).

### A.4 Le reste de la phase des héros

- **Attaquer, contrecarrer** ([P] `actions.py:743-793`) : incline ton héros ou
  ton allié (double-clic ou F7), puis survole la cible et appuie sur **Bas**
  autant de fois que de dégâts. Bas retire 1 PV à une identité ou un méchant,
  1 menace à une manigance. Sur un allié ou un sbire, Bas retire 1 dégât et
  **Haut** en ajoute 1.
- **Changer de forme** : **Ctrl+F** sur l'identité ([P] `actions.py:946-956`).
- **Piocher** : **Ctrl+D** ou double-clic sur le deck ; **Ctrl+Maj+D** pioche
  N cartes. Deck vide : la défausse est remélangée seule, sans carte Rencontre
  de pénalité ([P] `actions.py:1101-1127`).
- **Chercher une carte** : double-clic sur une défausse, ou clic droit puis
  « Look at » (Top X, All, Bottom X), puis glisser la carte trouvée ([O]
  `PileBaseControl.cs:15-30`, `GroupWindow.xaml.cs:94-160`).
- **Statuts** : **Alt+S/C/T** posent Sonné, Désorienté, Tenace ;
  **Ctrl+Alt** plus la même lettre les retire ([P] `definition.xml:224-229`).
- **Cibler** : Maj+clic sur une carte ; Maj+glisser d'une carte vers une autre
  trace une flèche ([O] `CardControl.xaml.cs:570`, `:662-669`).

### A.5 Fin de la phase des héros : F12

Pour **chaque joueur** ([P] `actions.py:479-500`, `:510-515`) : cibles
effacées, cartes redressées (sauf Rencontre, méchant, manigances), pioche
jusqu'à la taille de main, fenêtre pour défausser l'excédent. Puis la phase du
méchant commence.

### A.6 Phase du méchant

1. **Menace** : survole la manigance principale, **F5** ou **Haut**. F12 n'en
   pose pas ([P] `actions.py:456-477`).
2. **Activations** : double-clic sur le méchant ou **Alt+Entrée** pose la carte
   du dessus du deck Rencontre face cachée à côté de lui ([P]
   `actions.py:325-336`, `:675-711`). Double-clic pour la retourner, on
   applique, puis Suppr. Les dégâts subis se notent avec Bas sur l'identité.
3. **Cartes Rencontre** : survole le deck Rencontre, **Ctrl+U** : la carte
   arrive face cachée au centre ([P] `definition.xml:315`,
   `actions.py:1156-1169`). Place-la devant le joueur, double-clic pour la
   révéler : menace, compteurs, Tenace et PV se posent seuls ([P]
   `actions.py:946-976`). Une traîtrise se résout à la main puis Suppr : elle
   part en défausse Rencontre, ou en pile Victoire si elle porte « Victory »
   ([P] `actions.py:1025-1049`).
4. **Sbire engagé** : une simple carte posée dans la colonne du joueur, entre
   le méchant et le héros. Une convention, pas une zone ([P] `setup.py:297`,
   `:314`).

### A.7 Fin du round : F12 une seconde fois

Jeton premier joueur au suivant, phase « Héros », compteur Round +1,
sauvegarde automatique de la table ([P] `actions.py:466-475`).

### A.8 Manigances, stades, fin de partie

- Retourner une manigance : double-clic, sa menace se pose si elle était à 0
  ([P] `actions.py:328-329`).
- Accélération : **F4** en ajoute, **Maj+F4** en retire.
- Stade suivant de la manigance : Suppr sur la manigance principale, ou « Next
  Scheme » ([P] `actions.py:1020-1021`, `:1408-1429`).
- Stade suivant du méchant : Suppr sur le méchant, ou « Next Villain » ([P]
  `actions.py:1018-1019`, `:1432-1454`).
- Cartes Permanent : elles refusent Suppr ([P] `actions.py:1013-1015`).

### A.9 À plusieurs

- Une seule table. **Seul le contrôleur d'une carte peut la glisser** ([O]
  `CardControl.xaml.cs:643`). Prendre la main : clic droit, « Take control »,
  ou **F8** sur les cartes ciblées ([O] `GroupControl.cs:346` ; [P]
  `actions.py:502-508`).
- Défausser la carte d'un autre : elle part dans **sa** défausse ([P]
  `actions.py:1064-1075`).
- Mains déclarées visibles de tous en 0.0.3.97 ([P] `definition.xml:252`),
  non observé.

### A.10 Ce qu'OCTGN ne fait jamais

Payer ; découper la table en zones ; attacher une carte ; distribuer les cartes
Rencontre ; poser la menace de la phase du méchant ; annuler un geste
(SUPPOSÉ : seule échappatoire connue, « Restore last Auto Save »).

### A.11 Non confirmé

Qui a le droit d'appuyer sur F12 ; glisser une pile entière ; usage des pions
Physique, Énergie, Mental, Joker ; face de départ du héros ; conflit de F9 avec
les statistiques du client ; visibilité réelle des mains. Le fil BGG renvoie
403, octgngames.com a expiré.

### A.12 Le même round chez nous, aujourd'hui

| Étape | Geste chez nous aujourd'hui | Statut |
|---|---|---|
| Payer en défaussant de la main | Suppr au survol, ou glisser sur la défausse | Marche (`manuel-62`, `manuel-13`) |
| Payer en inclinant | F7 ou double-clic | Marche (`manuel-60`, `manuel-31`) |
| Poser un allié ou un soutien | Clic droit, « Déplacer vers… », « Alliés » ou « Soutiens ». Le glisser sur la table est refusé | Contourné (`manuel-70`) ; glisser après le lot 2 du plan |
| Poser une amélioration | Glisser sur la carte du héros (étiquette rouge à tort) | Marche (`manuel-12`) |
| Événement | Clic droit, « Déplacer vers… », « En cours de résolution » puis Suppr | SUPPOSÉ, non rejoué |
| Attaquer | F7 sur le héros, puis Bas sur le méchant | Marche (`manuel-63`) |
| Piocher | Ctrl+D sur le deck | Marche en solo (`manuel-61`) |
| Fin de phase des héros | F12 : redresse et pioche pour le **héros affiché** seulement | PROUVÉ par lecture (`CoucheTriche.tsx:569-603`) |
| Menace de la phase du méchant | F5 ou Haut sur la manigance principale | PROUVÉ par lecture (`manuel/clavier.ts`) |
| Activation du méchant | Alt+Entrée ou double-clic sur le méchant | PROUVÉ par lecture (`clavier.ts:88-94`) |
| Carte Rencontre | Clic droit sur le deck Rencontre, « Révéler » | PROUVÉ par lecture (`CoucheTriche.tsx:101-125`) |
| Fin du round | Aucun geste (ni premier joueur, ni compteur) | Absent |
| Stade suivant | Suppr sur le méchant ou la manigance principale | PROUVÉ par lecture (`clavier.ts:152-156`) |

Aucun round complet n'a été joué à la main dans un navigateur : c'est le
critère de fin global du plan.

---

## B. État actuel chez nous

### B.1 La cause exacte de « je ne peux pas poser une carte » (PROUVÉ)

1. **Ce que le pointeur voit.** `cibleSousLePoint`
   (`board/glisser/useGlisser.ts:165-207`) cherche d'abord une pile fine, puis
   le `data-zone` de l'emplacement. Sur le terrain, il trouve
   `terrain-soutien` ou `terrain-combat` (`Board.tsx:436`, `zones.ts:848`,
   `:998`). Sur la table vide hors des zones, rien.
2. **Les zones acceptées.** `PILE_PAR_ZONE` (`glisser-manuel.ts:67-89`) ne
   contient aucune des deux zones de terrain.
3. **Le refus.** `onDepot` (`glisser-manuel.ts:121-158`) ne trouve ni secteur,
   ni pile, ni carte, et renvoie `t('Lâche la carte sur une pile')` (`:157`),
   affiché en bulle 2,6 s (`Board.tsx:1035-1047`).
4. **L'origine.** Le plan prévoyait les deux zones
   (`plans/2026-09-18-mode-manuel-plateau.md:876-877`). L'agent de la tâche 5
   les a retirées ; ce choix n'est écrit que dans
   `.superpowers/sdd/2026-09-18-mode-manuel-plateau/task-5-report.md:165-180`,
   fichier ignoré par git (`.gitignore:159`). Rien n'indique que l'utilisateur
   l'ait tranché. La spec promettait « vers la pile **ou la zone visée** »
   (`specs/2026-09-18-mode-manuel-design.md:121`).
5. **Ce qui aggrave.** Un groupe vide n'est pas dessiné (`zones.ts:670-678`,
   `table-rendu.ts:40-41`) : le **premier allié ou le premier sbire** n'a aucune
   cible. La zone « Héros et soutiens » existe toujours, puisqu'elle contient
   `area_hero` (`zones.ts:966`), mais elle est refusée. L'aide n'en parle pas
   (`board/manuel/VoletAideManuel.tsx:6-39`).

Preuves dans le navigateur : `manuel-10-*` (lâcher dans « Héros et
soutiens »), `manuel-11-*` (table vide), `manuel-83/84-declaree-*` (même refus
sur une partie déclarée manuelle).

Précédent : en mode Auto, la même plainte a été corrigée le 15/09 en ouvrant le
terrain aux cartes sans cible (`board.tsx:2742-2745`).

### B.2 Ce qui marche (PROUVÉ dans un navigateur, 06/10)

| Geste | Résultat | Capture |
|---|---|---|
| Clic droit, « Déplacer vers… », « Soutiens » | Héliporteur passe dans `supports[0]` et se dessine | `manuel-70` |
| Lâcher sur la carte Peter Parker | Attachée (`area_hero[1]`) | `manuel-12` |
| Lâcher sur la défausse ou le deck | Déplacée | `manuel-13`, `manuel-14` |
| Suppr sur une carte en main | Défaussée | `manuel-62` |
| F7, double-clic sur le héros | Incliné | `manuel-60`, `manuel-31` |
| Ctrl+D sur le deck | Main de 2 à 3 cartes | `manuel-61` |
| Bas sur le méchant | 14/14 devient 13/14 | `manuel-63` |
| Ctrl+Z sur une partie déclarée manuelle | Retour à 14/14, la table reste en Manuel | `manuel-85` |

### B.3 Ce qui ne marche pas ou trompe le joueur

| Constat | Statut | Source |
|---|---|---|
| Lâcher sur la table ou une zone de terrain : refusé | PROUVÉ | B.1 |
| Étiquette rouge sur une pile pleine ou une attache, alors que le geste réussit | PROUVÉ (`manuel-12`, `-14`) | `glisser-manuel.ts:108` (cibles légales vides), `Board.tsx:1103-1110` |
| Pendant le glisser, la main et la manigance sont entourées, pas le deck ni la défausse | PROUVÉ (`manuel-10-pendant`) | `Board.tsx:1137` compare `piles-joueur` à `joueur-deck` ; contredit le commentaire `glisser-manuel.ts:6-8` |
| Une carte de main lâchée sur la manigance principale y est rangée | PROUVÉ (`manuel-15`) | `PILE_PAR_ZONE['complot-principal']` |
| Un allié lâché sur le héros s'y attache | PROUVÉ par lecture | `glisser-manuel.ts:147-155` |
| Un sbire déjà engagé relâché sur son secteur se **désengage** (`Engage` bascule) | PROUVÉ par lecture | `glisser-manuel.ts:127-130`, `puzzle.py:898-906` |
| Toute carte est glissable, même en jeu ou chez un autre héros | PROUVÉ par lecture | `glisser-manuel.ts:105` (`estSource: () => true`) |
| Double-clic en main : la carte est retournée dans le moteur sans rien montrer | PROUVÉ (`manuel-30`, `is_face_up` false puis true) | `clavier.ts:90`, `CoucheTriche.tsx:729-738` |
| Tablette en émulation : aucun glisser au doigt, appui long sans effet | PROUVÉ en émulation (`manuel-22` à `-28`), SUPPOSÉ sur appareil | pas de `touch-action: none` sur les cartes (`board.css:91`, `:1144`) |
| Téléphone : pas de glisser, appui long sans effet en manuel | PROUVÉ par lecture | `mobile/PlateauPortrait.tsx:148-154` |
| Ctrl+Z sur une partie **basculée** : la table repasse en Auto | PROUVÉ (`manuel-80/81`), cause inconnue | voir B.5 |
| Bouton flottant « Fin du tour » : le moteur avance en manuel basculé | PROUVÉ (`manuel-75/76`) | `board.tsx:4574`, sans garde `manuel` |
| Touche E : répond à la question garée du moteur en manuel basculé | PROUVÉ par lecture, non rejoué | `board.tsx:3460-3461`, `:3764-3766` |
| Cartes « jouables » encore surlignées en manuel basculé | Constaté sur capture `manuel-01`, classes non conservées | `board.tsx:2114-2117` |
| Bouton « ↶ Annuler » et touche U appellent `/debug?/undo auto`, pas `/manuel_undo` | PROUVÉ par lecture | `board.tsx:3486-3490`, `:3468-3469` |
| Le spectateur peut lancer le glisser manuel (403 au serveur) | PROUVÉ par lecture | `board.tsx:2708-2711` |
| Libellés du glisser sans nom de carte | PROUVÉ par lecture | `glisser-manuel.ts:128`, `:136`, `:154` |
| L'aide ne dit rien du glisser, de « Déplacer vers » ni du paiement | PROUVÉ | `VoletAideManuel.tsx:6-39` |
| L'aide dit Étourdi, Confus, Coriace ; le menu dit sonné, désorienté, tenace | PROUVÉ | `VoletAideManuel.tsx:17-22`, `MenuTriche.tsx:283-288` |
| Titre du menu en anglais (« Spider-Tracer ») | PROUVÉ (`manuel-40`) | `CoucheTriche.tsx:373` |
| Sous-menu « Déplacer vers » : 6 entrées visibles sur 25 à 720 px | PROUVÉ (`manuel-41`) | `MenuTriche.tsx:32-82` |
| À 1280x720, la main est coupée en bas | Constaté sur capture `manuel-01`, mesure non conservée | |
| F12 et Ctrl+Q n'agissent que pour le héros affiché | PROUVÉ par lecture | `CoucheTriche.tsx:569-603`, `joueurId = joueurActif` (`board.tsx:1860`, `:2464`) |
| F12 avec le sélecteur sur le héros 2 : les cartes de son deck iraient dans la main du joueur **courant** | SUPPOSÉ (déduit) | `CoucheTriche.tsx:571`, `:588-590`, `triche.ts:74` (`Puzzle.Gain`), `puzzle.py:256-261` |
| Ctrl+D sur le deck du héros 2 : même risque (`Gain` donne au joueur courant) | SUPPOSÉ | `puzzle.py:256-261`, `world_action.py:33-45` |
| « Remélanger la défausse » : une ligne de journal pour N+1 commandes ; un Ctrl+Z ne défait que la dernière | PROUVÉ par lecture | `triche.ts:106-107`, `CoucheTriche.tsx:899-908`, `engine/device/manager/base.py:251-265`, `game/scene/scene.py:191`, `:199` |
| Non-opérations journalisées comme réussies (ex. « Soigner 3 » sur un événement) | PROUVÉ par lecture | `puzzle.py:297-309`, `:413`, `:424` |
| Test e2e périmé : son étape 5 tape « 3 », touche retirée par `5b88d9a2` | PROUVÉ par lecture, non exécuté | `ui-check/tests/mode-manuel.spec.ts:265-281`, `clavier.ts:119` |

### B.4 Ce que le moteur fait déjà sans le dire

- La porte du silence ferme `BroadcastMessage` (`game/event/manager.py:685`),
  `BroadcastStackMessage` (`:648`) et la défaite automatique
  (`game/card/face/model/face_on_event.py:428`).
- Les crochets `OnWhenCardEnterPlay` passent à côté
  (`face_on_event.py:372-378`). Une carte qui entre en jeu par `MoveTo` reçoit
  donc ses compteurs « Uses » (`has_uses.py:20-28`) et son statut Tenace
  (`has_toughness.py:14-20`).
- Uses : PROUVÉ et observé (« 3 TOILE » sur Lance-Toile, `manuel-40`,
  `manuel-41`). Tenace : PROUVÉ par lecture seulement. Menace de départ d'une
  manigance annexe et PV : non vérifiés.
- C'est l'équivalent partiel de l'`autoCharges` d'OCTGN, contraire à la lettre
  du « silence total » (`specs/2026-09-18-mode-manuel-design.md:37`). La
  décision revient à l'utilisateur (question 5).

### B.5 Points du moteur qui pèsent sur la conception

1. **« Joueur 0 » n'est pas le siège 0.** `MoveTo`, `Engage` et `Shuffle`
   visent `world.const_players[player]` (`puzzle.py:850`, `:902`), qui vaut
   `world.players[:]` (`game/world/world_action.py:22-24`), liste qui **tourne**
   à chaque fin de round (`game/world/world.py:1069`). Le plateau numérote par
   siège fixe (`const_seat_order_players`, `game/render/to_descriptor.py:96`).
   Envoyer le numéro de siège du plateau dans `player=` serait faux après le
   round 1. PROUVÉ par lecture. Le commentaire `zones.ts:868-873` (« joueur
   COURANT ») est inexact.
2. **Un geste égale une commande.** Un geste fait de N commandes compte pour N
   (`base.py:251-265`, `scene.py:191`) et Ctrl+Z n'en retire qu'un
   (`scene.py:199`).
3. **Ctrl+Z qui repasse en Auto.** `FinirLeRejeuDesGestes` remet
   `manuel_actif` si `scene.pause_en_cours`
   (`game/game_run/game_session.py:258-281`), ce qui contredit le symptôme.
   Le relevé montre `mode_manuel=false` et `restants: 0` après l'annulation.
   Piste : la garde `not self.mise_en_place_finie` (`game_session.py:277`).
   Cause non établie.
4. **Face visible à l'arrivée.** `game/deck/deck.py:138-139` ne force la face
   de la zone que si `card.back_faces == []`. Garantie pour une carte à une
   face ; une carte à deux faces garde la sienne.
5. **`player.area_processing` existe** (`player.py:90`) et le plateau la
   dessine près du héros (`zones.ts:967-970`). Le moteur Auto la lit pour
   résoudre ses propres événements (`game/operate/faces.py:123`).
6. **Le coût est déjà publié** : `cost: number` (`board/world.ts:37`). Le cas
   d'un coût absent ou variable (X) est à vérifier dans le descripteur
   (SUPPOSÉ).

---

## C. Tableau d'écart geste par geste

Priorités : **P1** indispensable pour poser et payer ; **P2** défaut qui trompe
ou bloque ailleurs ; **P3** confort, fidélité complète. La colonne « Lot »
renvoie au plan.

| # | Geste | OCTGN | Chez nous | À faire | Prio | Lot |
|---|---|---|---|---|---|---|
| 1 | Glisser de la main vers la table | Posée face visible au point du lâcher | Refus | Mettre en jeu selon le type (D.3) | P1 | 2 |
| 2 | Glisser vers une zone de terrain | Pareil | Refus | Pareil | P1 | 2 |
| 3 | Lâcher sur une carte en jeu | Chevauchement, aucune attache | Attache quel que soit le type | Question 2 | P1 | 2 |
| 4 | Lâcher sur une pile | Dessus de la pile ([O] `PileControl:151-188`) | Marche, étiquette rouge à tort | Étiquette juste | P1 | 2 |
| 5 | Premier allié, premier sbire | Lâché n'importe où | Aucune cible | Règle de la table (D.2) | P1 | 2 |
| 6 | Cadres pendant le glisser | Aucun | Main et manigance seulement | Question 12 | P2 | 2 |
| 7 | Payer en défaussant | Suppr, ou glisser sur la défausse | Marche | Le dire dans l'aide | P1 | 3 |
| 8 | Payer en inclinant | Double-clic ou F7 | Marche | Le dire dans l'aide | P1 | 3 |
| 9 | Clic droit sur une carte en main | Discard, Switch with top deck, Move to | Pas de « Poser en jeu » | Ajouter « Poser en jeu » | P1 | 3 |
| 10 | Aide à l'écran | Écran d'accueil, Ctrl+I | Rien sur la pose | Section « Jouer une carte » | P1 | 3 |
| 11 | Journal du glisser | « moves 'Nom' to Table » | Sans nom de carte | Nommer la carte | P1 | 2 |
| 12 | Carte déjà en jeu relâchée sur la table | Déplacée sur la table | `MoveTo` vers sa propre zone (geste inutile) | Question 13 | P1 | 2 |
| 13 | Sbire engagé relâché sur son secteur | Rien | Désengagé (`Engage` bascule) | `MoveTo` vers les engagés | P1 | 2 |
| 14 | Double-clic en main | Rien | Retourne la carte en secret | Question 8 | P2 | 1 |
| 15 | Bouton « Fin du tour » flottant, touche E | Sans objet | Le moteur avance pendant le manuel | Les masquer en manuel | P2 | 1 |
| 16 | Surlignage des cartes jouables | Sans objet | Reste affiché en manuel basculé | Le masquer | P2 | 1 |
| 17 | Bouton « Annuler », touche U | Pas d'annulation | `/debug?/undo auto` | Brancher sur `/manuel_undo` | P2 | 1 |
| 18 | Ctrl+Z sur une partie basculée | Sans objet | La table repasse en Auto | Diagnostiquer puis corriger | P2 | 1 |
| 19 | Glisser au doigt | Sans objet | `pointercancel` | `touch-action` sur les cartes | P2 | 4 |
| 20 | Appui long, téléphone | Sans objet | Rien | Menu à l'appui long (question 11) | P2 | 4 |
| 21 | Poser chez un autre héros | Où on la lâche | `world.players[0]`, ordre qui tourne | Paramètre `siege` (D.6) | P2 | 2 (moteur) puis 5 |
| 22 | Ctrl+D, F12 sur le héros 2 | Chez lui | `Gain` donne au joueur courant (SUPPOSÉ) | Viser le propriétaire | P2 | 5 |
| 23 | F12 et Ctrl+Q | Tous les joueurs | Héros affiché seulement | Question 7 | P2 | 5 |
| 24 | Bouger la carte d'un autre joueur | Contrôleur seulement | Tout le monde | Question 14 | P2 | 5 |
| 25 | Glisser par un spectateur | Sans objet | Lancé côté interface, 403 | Garde spectateur | P2 | 1 |
| 26 | Compteurs à l'arrivée | Uses, Tenace, menace, PV | Uses et Tenace | Question 5 | P2 | 2 (témoin) |
| 27 | Maj au lâcher sur la table | Face cachée | Maj = dessous de pile | Face cachée sur la table, dessous sur une pile | P3 | 6 |
| 28 | Double-clic sur une manigance | Retourne, pose la menace | Rien (`clavier.ts:89`) | Porter | P3 | 6 |
| 29 | F12 complet | Excédent, remélange, fin de round | Ni l'un ni l'autre | Porter | P3 | 6 |
| 30 | Ctrl+U, Ctrl+Maj+U, Ctrl+F sur une pile, F1, Maj+F1, Ctrl+I, mulligan, défausse au hasard, échange avec le dessus du deck, PgUp/PgDn, ciblage | Existent | Absents | Un par un | P3 | 6 |
| 31 | Sélection multiple (lasso, Ctrl+clic) | Existe ([O] `TableControl.xaml.cs:548-554`, `:1067-1110`) | Absent | Porter ou noter « non porté, volontaire » | P3 | 6 |
| 32 | Glisser la carte du dessus d'une pile vers la table | Existe | FAIT et vu au navigateur le 06/10/2026 : saisir une pile prend sa carte du dessus ; dans la main = piochée, sur une autre pile = déplacée, sur la table = posée selon son type (une pièce jointe sans hôte attend en résolution, comme après Ctrl+D) | Fait | P3 | restes |
| 33 | Touches maison F, Q, R, chiffres | Sans objet | Retirées sans décision tracée | Question 10 | P3 | 6 |
| 34 | Clavier seul : ouvrir le menu d'une carte | Sans objet | Aucune touche (ni Menu ni Maj+F10) | Touche Menu, `aria-live` sur la bulle | P3 | 6 |
| 35 | Titre du menu, sous-menu coupé, main coupée à 720 px | Sans objet | Défauts d'affichage | Nom français, défilement, mesure | P3 | 3 |

---

## D. Conception proposée

### D.0 Décisions déjà prises, à respecter

- Mise en place automatique, mulligan compris ; ensuite le moteur se tait et
  aucune règle n'est vérifiée (`specs/2026-09-18-mode-manuel-design.md:35-40`).
- Ctrl+Z geste par geste (`spec:43`).
- Le glisser-déposer est « le cœur, pas la décoration »
  (`.planning/todos/2026-09-14-mode-manuel-sans-automatisation.md:83-85`).
- Une main à l'écran plus un sélecteur de héros
  (`plans/2026-09-18-mode-manuel-plateau.md:1283-1284`).
- 05/10 (`facon-de-jouer-manuel-octgn.md`) : interrupteur Auto/Manuel, fenêtre
  « On en est où ? », gestes OCTGN **en plus** des nôtres (`:17`), tout joueur
  bascule la table pour tous (`:23-24`), aide qui s'ouvre seule (`:25-27`).
- Zone vide invisible, place gardée (`2026-10-05-table-par-briques-decisions.md:23`).
- Mémoire : « que ça match à 100 % » (corriger le moteur avant d'accepter un
  écart) ; une gate plutôt qu'un repli générique ; tester ce que le plateau
  dessine.

### D.1 Le principe

Comme sur OCTGN, **lâcher une carte sur la table la met en jeu**. Notre moteur
ne connaît que des piles : le plateau traduit le lâcher en **une seule**
commande `Puzzle.*`, sans vérifier aucune règle (coût, limite, cible).
« Déplacer vers… » garde sa liberté totale.

### D.2 Ordre de décision au lâcher (la première règle qui s'applique gagne)

0. **Source déjà en jeu** (question 13) : recommandé, lâchée sur la table hors
   de toute pile et de tout autre joueur, **aucune commande, aucun geste**.
   Lâchée sur le groupe d'un autre joueur : changement de joueur (lot 5).
1. **Secteur des ennemis engagés** : `MoveTo(id, 'EngagedEnemiesArea', siege)`,
   au lieu de `Engage`, qui bascule (`puzzle.py:902-906`) : un sbire déjà
   engagé relâché sur son secteur ne doit plus se désengager.
2. **Pile fine** (deck, défausse, deck spécial, défausse spéciale) **ou
   zone-pile** (main, réserve, marée montante) : dessus, ou dessous avec Maj
   (inchangé).
3. **Zones de manigance** : n'acceptent plus que les manigances. Une autre carte
   suit les règles 4 et 5 (For Justice! lâché sur la manigance va en
   résolution, constat `manuel-15`).
4. **Sur une carte en jeu** (question 2) : recommandé, s'attache si c'est une
   amélioration (`Upgrade`) ou un attachement (`Attachment`) ; sinon règle 5.
5. **Ailleurs dans le cadre du plateau** (zone de terrain, vide entre les
   zones, zone vide invisible) : « poser en jeu » selon le type (D.3), chez le
   joueur visé (D.6).
6. **Hors du plateau** (journal, barre) : refus « Lâche la carte sur la table
   ou sur une pile ».

Pour la règle 5, on ajoute un champ `surLaTable` à `CibleSurvolee`, vrai si le
point est dans `.plateau-cadre` (`Board.tsx:1172`). Seul le mode manuel le lit :
le mode Auto reste intact.

### D.3 Table « poser en jeu » (à valider par les questions 1, 3, 4)

Noms des types : classes de `game/card/face/card_type/*.py` (liste obtenue par
`ls` et `grep class`, pas de mémoire). L'égalité avec `card_type` du
descripteur (`board/world.ts:36`) est à vérifier au lot 2 (SUPPOSÉE).

| Type | Destination | Commande (une seule) |
|---|---|---|
| `Ally` | Alliés du joueur | `MoveTo(id, 'AlliesArea', 'Top', siege=s)` |
| `Support` | Soutiens | `MoveTo(id, 'SupportsArea', 'Top', siege=s)` |
| `Upgrade` | Attachée à l'identité du joueur (question 3) | `Attach(id, <identité>)` |
| `Event` | Résolution du joueur, près de son héros (question 4), puis Suppr | `MoveTo(id, 'PlayerProcessingArea', 'Top', siege=s)` (zone à ajouter) |
| `Minion`, `PlayerMinion` | Engagé avec le joueur | `MoveTo(id, 'EngagedEnemiesArea', siege=s)` |
| `Environment` | Environnement | `MoveTo(id, 'EnvironmentArea')` |
| `Obligation` | Obligations du joueur | `MoveTo(id, 'ObligationsArea', siege=s)` |
| `PlayerSideScheme`, `EncounterSideScheme` | Manigances annexes | `MoveTo(id, 'SideSchemesArea')` |
| `Treachery` | Résolution du scénario | `MoveTo(id, 'ProcessingArea')` |
| `Resource` | Refus : « Une ressource se défausse pour payer : Suppr, ou glisse-la sur ta défausse » | Aucune |
| `Attachment` (rencontre), `Evidence` | Refus : « Lâche-la sur la carte qu'elle accompagne » | Aucune |
| `Hero`, `AlterEgo`, `EncounterVillain`, `Leader`, `MainScheme`, `StatusCard`, `Insert`, `Challenge`, type inconnu | Refus : « Cette carte ne se pose pas sur la table : glisse-la sur une pile ou fais Déplacer vers » | Aucune. Gate, pas repli |

Face : garantie visible pour une carte à une face (B.5 point 4). Une carte à
deux faces garde sa face d'arrivée (à vérifier au lot 2 sur une carte réelle).

### D.4 Pendant le glisser

- **Étiquette** : dit ce qui va se passer, avec le nom de la carte, par exemple
  « Poser en jeu : Héliporteur (Soutiens) ». Option A de la question 9 : elle
  ajoute le coût (`cost`, `world.ts:37`) ; coût absent ou X : rien affiché.
- **Couleur** : nouveau prédicat optionnel `accepte(source, cible)` dans
  `ReglagesGlisser` (`Board.tsx:886-900`). En manuel il vaut
  `libelle(...) !== undefined`. Le rouge (`Board.tsx:1103-1110`) ne s'affiche
  que si le lâcher sera vraiment refusé.
- **Cadres** : selon la question 12.

### D.5 Payer

Rien d'automatique, comme sur OCTGN ; aucun raccourci qui paie à la place du
joueur (`spec:38`). L'aide explique Suppr ou glisser vers la défausse, et F7 ou
double-clic pour incliner.

### D.6 Chez qui va la carte

- Règle recommandée (question 6) : le groupe sous le pointeur porte
  `data-joueur` : chez ce joueur ; sinon chez le joueur d'où vient la carte ;
  sinon chez le héros affiché.
- Moteur : paramètre `siege` ajouté à `MoveTo`, `Engage`, `Shuffle`, qui vise
  `world.const_seat_order_players[siege]`. Additif : `player=` reste valable.
- Rejeu : un geste ancien sans `siege` garde sa sémantique (« premier joueur au
  rang du geste ») ; un geste avec `siege` est déterministe.

### D.7 Alternatives au glisser

- **Menu** : nouvelle première entrée « Poser en jeu » sur une carte hors jeu
  (main, résolution), même table D.3, même module pur.
- **Double-clic en main** : rien (question 8, recommandé).
- **Clavier** : aucune touche « poser » (OCTGN n'en a pas). Accessibilité :
  touche Menu ou Maj+F10 pour ouvrir le menu de la carte survolée ou focalisée
  (P3).
- **Tactile** (question 11, recommandé) : `touch-action: none` sur les
  `.scan-card` en manuel ; appui long immobile de `APPUI_LONG_MS` (450 ms,
  `board/mobile/useAppuiLong.ts:23`) qui ouvre le menu du clic droit ; même
  chose sur téléphone (`PlateauPortrait`).

### D.8 Journal

- Une ligne par geste, nommée par la carte, au format du menu
  (`MenuTriche.tsx:299-311`), via `emettreGeste` (`CoucheTriche.tsx:246-256`).
- Un refus du plateau reste en bulle, non journalisé (rien n'est envoyé).
- Une carte face cachée n'est jamais nommée (journal ni étiquette) : « carte
  face cachée ». Même règle pour une carte piochée chez un autre joueur.
- Un geste égale une commande (B.5 point 2) : la pose face cachée attend le
  lot 6, avec un paramètre moteur `face_cachee`.

### D.9 Refus du moteur

Un lâcher accepté par le plateau peut être refusé par le moteur : l'avis
« (refusé) » existant s'affiche (`CoucheTriche.tsx:320-325`). Les
non-opérations silencieuses deviendront des refus au lot 6.

### D.10 Annulation

En manuel, Ctrl+Z, « ↶ Annuler » et U suivent le même chemin : `lancerAnnulation`
vers `/manuel_undo` (`CoucheTriche.tsx:628-637`). Une partie basculée reste en
Manuel après l'annulation.

### D.11 Reprise en Auto

Une carte posée par `MoveTo` n'a déclenché aucune capacité, et les
modificateurs étaient fermés (`spec:98-103`) ; `MoveTo` garde le propriétaire
comme contrôleur (`card_face.py:1022-1026`). À prouver au lot 2, c'est la
preuve réclamée par `facon:50-51` :
- un allié posé à la main peut attaquer après `/manuel_reprise` ;
- une amélioration attachée à la main modifie la statistique après la reprise
  (SUPPOSÉ incertain) ;
- un événement laissé dans `player.area_processing` ne perturbe pas l'Auto
  (`faces.py:123`) ; sinon gate ou avertissement dans « On en est où ? » ;
- une amélioration attachée survit au changement de forme (SUPPOSÉ).

### D.12 Texte proposé pour l'aide (`VoletAideManuel.tsx`), en tête

**Jouer une carte**
1. **Paie.** Survole une carte de ta main et appuie sur Suppr, ou glisse-la sur
   ta défausse. F7 ou un double-clic incline une carte en jeu.
2. **Pose.** Glisse la carte de ta main et lâche-la n'importe où sur la table :
   un allié va dans Alliés, un soutien dans Soutiens, une amélioration sous ton
   héros, un événement à côté de ton héros (résous-le, puis Suppr).
3. **Lâche sur une carte** pour y attacher une amélioration.
4. **Lâche sur une pile** pour la mettre dessus, ou dessous avec Maj.
5. **Clic droit sur une carte** : Poser en jeu, ou Déplacer vers…
6. **Au doigt** : maintiens le doigt sur une carte pour ouvrir le même menu.

Aussi : renommer les statuts en Sonné, Désorienté, Tenace ; compléter la ligne
du clic droit sur la table (Vaincre ce stade, Manigance terminée, Tout
redresser, Fin de phase des héros, Amplification ; `MenuTable.tsx:119-163`).
