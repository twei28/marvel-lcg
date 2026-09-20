# Plan d'exécution : la pause manuelle en pleine partie

> **Pour un agent d'exécution :** SOUS-SKILL REQUISE : utiliser
> `superpowers:subagent-driven-development` (recommandé) ou
> `superpowers:executing-plans` pour dérouler ce plan tâche par tâche. Les
> étapes sont en cases à cocher (`- [ ]`).

**But :** pouvoir arrêter le moteur en pleine partie ORDINAIRE, corriger la
table à la main, et reprendre là où on en était. C'est ce qui permet à un
joueur de contourner un bug du moteur et de finir sa partie, au lieu de la
perdre.

**Architecture :** aucune boucle nouvelle. Le moteur est déjà garé dans
`DoGetInput` quand il attend une réponse, et c'est déjà là que les commandes
manuelles s'exécutent. La pause ne fait donc que poser `world.manuel_actif` à
vrai, réveiller l'attente, et laisser l'appelant reposer sa question. La reprise
fait l'inverse.

**Pile technique :** moteur Python 3.10 (`Fusion/marvel-lcg-src/src`), plateau
React + TypeScript + Vitest (`ui-app`), bout en bout Playwright (`ui-check`).

**Spec :** `docs/superpowers/specs/2026-09-18-mode-manuel-design.md`, avenant du
18/09/2026, plus la décision du 20/09 sur le multijoueur.

## Ce qui est déjà livré, et sur quoi ce plan s'appuie

Le **mode manuel déclaré** est fini, revu et fusionnable (63 commits sur la
branche `mode-manuel`). Il fournit tout le vocabulaire :

- `world.manuel_actif` : l'ÉTAT « le moteur s'est tu ». Il ferme la porte des
  déclenchements (`EventManager.BroadcastMessage`) et celle de la défaite
  (`ModelOnEvent.Defeated`). Il est publié dans la trame.
- `world.rule.mode_manuel` : la RÈGLE « cette partie est manuelle ». Elle ne
  sert qu'à ce qui décrit la nature de la partie.
- Côté plateau, `leMoteurSeTait(world)` masque les couches du moteur et arme les
  gestes manuels. `estModeManuel(world)` ne sert qu'aux trois usages de nature.
- Tous les gestes de l'API `Puzzle`, le menu au clic droit, le clavier, le
  glisser libre, la recherche catalogue, l'annulation, et la file du journal qui
  n'annonce jamais un succès sur un geste refusé.

**Ce plan ne construit donc presque rien de neuf.** Il rend `manuel_actif`
basculable, et traite ce que cette bascule implique.

## Décisions déjà prises

| Question | Décision |
|---|---|
| Forme | Pause sur place : le moteur reste garé sur sa question |
| Si la question elle-même est fautive | Un bouton « passer cette question » |
| Pendant la pause | La porte du silence se ferme, comme en mode déclaré |
| Reprise | Le moteur repose sa question, options recalculées |
| Qui peut mettre en pause en ligne | N'importe qui à la table, et tout le monde le voit |
| Traces | Gestes au journal à leur place chronologique, marqués ; et la liste reprise à part dans le rapport de bug |
| Hauts faits | Sans objet, leur bannière est débranchée |
| La partie | Continue de compter, marquée « corrigée à la main » |

## Contraintes globales

- **Une seule copie vivante du moteur** : `Fusion/marvel-lcg-src/`.
- **Interpréteur** : `~/marvel-work/python/bin/python3.10`. Jamais celui du
  système.
- **Jamais `.game` ni `.game-src`** : le harnais tourne sur un dossier jetable,
  créé puis supprimé. Une exécution au premier plan, `timeout` de 600000 ms.
- **Comment attendre la batterie, qui dure plus longtemps que l'outil.**
  Elle prend une quinzaine de minutes, et l'outil d'exécution coupe à dix :
  au-delà, le harnais bascule tout seul la commande en tâche de fond. Si tu
  attends alors sa notification de fin, tu attends quelqu'un qui n'existe pas
  et ta tâche se fige jusqu'à ce qu'un humain la débloque. C'est arrivé cinq
  fois sur ce chantier, et j'ai longtemps cru à de la désobéissance : c'est
  l'outillage. La bonne manière est d'attendre par tranches bornées, au
  premier plan :

  ```bash
  # lancer en écrivant dans un journal, puis relever le PID
  nohup ~/marvel-work/python/bin/python3.10 tools/test_mode_manuel.py \
      .game-src-<le tien> <port> > /tmp/batterie.log 2>&1 &
  echo $!
  # puis, autant de fois qu'il faut, chacune rendant la main avant le plafond
  timeout 560 tail --pid=<PID> -f /dev/null
  ```

  Ensuite tu lis le journal. Si un processus traîne d'un essai précédent,
  tue-le par son PID.
- **TypeScript strict, zéro `any`.** Aucun texte en dur : tout par `t()` avec sa
  contrepartie dans `ui-app/src/board/dico-en.ts`, jamais de `t()` au niveau
  d'un module.
- **Le mode ordinaire ne doit RIEN perdre.** C'est l'exigence la plus lourde :
  cette fois, le mode ordinaire est le mode dans lequel la pause vit.
- **N'utilise JAMAIS `git stash`** : le dépôt est partagé avec des sessions
  vivantes.
- **Aucun déploiement.** Le test de bout en bout se lance en LOCAL.
- Un échec de `npm run typecheck` préexiste sur la branche
  (`src/board/halo-heros-accord.test.ts`), étranger à ce chantier, et il
  **bloque la construction du plateau** : le contourner temporairement pour
  construire, puis restaurer le fichier, comme documenté dans
  `.superpowers/sdd/2026-09-18-mode-manuel-plateau/task-8-report.md`.

## Le piège principal, nommé d'avance

`manuel_actif` n'a **jamais été remis à faux** jusqu'ici. Le mode déclaré le
pose et ne l'enlève pas, puisqu'une partie manuelle ne redevient jamais
automatique. Tout ce que le plateau masque n'a donc jamais eu à réapparaître.

Le jour où quelque chose l'éteint, tout revient d'un coup : bandeau de phase,
déroulé, assistant, demande centrale, barre d'actions, sélecteur de héros, et
les gestes manuels doivent se désarmer au même instant. **C'est le cœur de ce
plan, et le premier cas de test doit le prouver**, pas le supposer.

---

### Tâche 1 : la pause s'allume et s'éteint, côté moteur

**Fichiers :**
- Modifier : `Fusion/marvel-lcg-src/src/game/world/world.py`
- Modifier : `Fusion/marvel-lcg-src/src/engine/device/web/server/server_get.py`
- Modifier : `Fusion/marvel-lcg-src/tools/test_mode_manuel.py`

**Interfaces :**
- Produit : `World.BasculerPauseManuelle(actif: bool) -> bool`, qui pose
  `manuel_actif` et réveille l'attente d'entrée.
- Produit : la route `POST /manuel_pause`, corps `{"actif": true|false}`,
  qui rend `{"result": "en pause"}` ou `{"result": "repris"}`.

⚠ **Ne crée aucune boucle.** Le moteur est déjà garé dans `DoGetInput` : il
suffit de réveiller `notify.input`, comme le fait `QueueSandboxCommands`. Le fil
du jeu se réveille, ne trouve aucune entrée, rend la main, et l'appelant repose
sa question, ce qui produit un rendu portant le nouvel état.

⚠ **La bascule vient du fil HTTP.** Poser un booléen y est sans danger, mais
**ne touche à rien d'autre du monde depuis ce fil** : c'est explicitement
interdit par le commentaire de `engine/device/manager/base.py`.

- [ ] **Étape 1 : écrire les cas rouges**

Dans `tools/test_mode_manuel.py`, sur une partie ORDINAIRE (sans la règle) :

1. `cas_pause_ferme_la_porte` : le moteur tourne normalement, on met en pause,
   et un geste qui déclencherait une capacité ne déclenche plus rien. Réutilise
   le témoin déjà écrit pour le mode déclaré.
2. `cas_reprise_rouvre_la_porte` : après reprise, le même geste déclenche de
   nouveau. **C'est LE cas du plan** : il prouve que la porte se rouvre, ce que
   rien n'a jamais vérifié.
3. `cas_pause_publiee` : la trame publie `manuel_actif` à vrai pendant la pause,
   à faux après la reprise.

- [ ] **Étape 2 : les voir rouges, écrire le code, les voir verts**

- [ ] **Étape 3 : relancer la batterie complète du harnais, puis commiter**

---

### Tâche 2 : la marque « corrigée à la main », qui survit

**Fichiers :**
- Modifier : `Fusion/marvel-lcg-src/src/game/scene/scene.py`
- Modifier : `Fusion/marvel-lcg-src/src/game/world/world.py`
- Modifier : `Fusion/marvel-lcg-src/src/game/render/descriptor/world.py`
- Modifier : `Fusion/marvel-lcg-src/src/game/render/to_descriptor.py`
- Modifier : `Fusion/marvel-lcg-src/tools/test_mode_manuel.py`

**Interfaces :**
- Produit : `Scene.corrigee_a_la_main: bool`, à défaut faux, posé à la première
  pause et **jamais remis à faux**.
- Produit : le champ correspondant dans la trame.

⚠ **Un champ à défaut faux** : les sauvegardes existantes se rechargent sans
changer de sens. C'est la même précaution que pour `manuel_commands`.

⚠ **Il ne s'éteint pas à la reprise.** Une partie qu'on a corrigée à la main
l'a été, même si on a repris ensuite. C'est une marque, pas un état.

- [ ] **Étape 1 : le cas rouge** — une partie ordinaire porte la marque à faux ;
  après une pause elle la porte à vrai ; après la reprise elle la porte encore.
- [ ] **Étape 2 : poser le champ, le voir vert**
- [ ] **Étape 3 : commiter**

---

### Tâche 3 : le bandeau de pause, et la reprise

**Fichiers :**
- Créer : `ui-app/src/board/manuel/BandeauPause.tsx` et son test
- Modifier : `ui-app/src/board/triche.ts` (la bascule)
- Modifier : `ui-app/src/board.tsx`

**Interfaces :**
- Produit : `triche.basculerPause(actif: boolean)`.
- Produit : `<BandeauPause enPause={...} onReprendre={...} onPasser={...} />`.

**Ce que le bandeau doit dire**, et c'est le cœur de la tâche : qui a mis en
pause, et depuis quand. Sur une table en ligne, les autres joueurs voient leur
partie s'arrêter : sans cette phrase, ils croient à une panne.

⚠ **Le bouton qui met en pause doit exister quelque part en mode ORDINAIRE.**
Le plateau ordinaire n'a pas de menu de table : trouve l'endroit juste, et
dis-le dans ton rapport. Ce n'est pas un réglage caché, c'est ce qu'on cherche
quand le jeu vient de faire quelque chose d'absurde.

- [ ] **Étape 1 : le cas rouge** — le bandeau ne s'affiche pas hors pause,
  s'affiche en pause, nomme qui a mis en pause, et appelle `onReprendre`.
- [ ] **Étape 2 : écrire, voir vert, commiter**

---

### Tâche 4 : tout revient à la reprise

**Fichiers :**
- Modifier : `ui-app/src/board/manuel/plateau-muet.test.tsx` ou un fichier voisin
- Modifier : les appelants si un manque apparaît

**C'est la tâche la plus importante du plan, et elle est presque entièrement
faite de tests.**

Le mode déclaré n'a jamais eu à faire réapparaître quoi que ce soit. Il faut
donc prouver, couche par couche, que tout ce qui a été masqué revient.

- [ ] **Étape 1 : le cas rouge**

Un seul cas, mais qui les couvre toutes : en partie ordinaire, avec
`manuel_actif` à vrai puis à faux, vérifier que **chacune** des couches du
moteur est absente puis présente : bandeau de phase, déroulé, assistant
d'action, demande centrale, récapitulatif, barre des actions, et le sélecteur
de héros.

Et le pendant sur les gestes : le clic droit et le clavier répondent pendant la
pause, et ne répondent plus après la reprise.

- [ ] **Étape 2 : corriger ce qui ne revient pas**

Il y aura des surprises : un composant qui garde un état interne, un minuteur
qui ne repart pas, une animation qui reste figée. Traite-les, et **décris
chacune dans ton rapport** : ce sont elles qui diront si la pause est fiable.

- [ ] **Étape 3 : commiter**

---

### Tâche 5 : passer la question fautive

**Fichiers :**
- Modifier : `Fusion/marvel-lcg-src/src/engine/device/web/server/server_get.py`
- Modifier : `Fusion/marvel-lcg-src/src/engine/device/manager/base.py`
- Modifier : `ui-app/src/board/manuel/BandeauPause.tsx`
- Modifier : `Fusion/marvel-lcg-src/tools/test_mode_manuel.py`

C'est l'échappatoire : quand c'est la QUESTION du moteur qui est fautive, la
pause seule n'en libère pas, puisqu'il la reposera à la reprise.

⚠ **N'invente jamais une réponse que le moteur n'a pas offerte.** Regarde ce que
la question propose (elle porte un drapeau d'annulation) et n'utilise que ça. Si
la question courante n'offre aucune sortie, **dis-le au joueur** plutôt que de
fabriquer une entrée : une réponse inventée corromprait la partie bien plus
sûrement que le bug qu'il essayait de contourner.

- [ ] **Étape 1 : le cas rouge** — une question qui offre une annulation est
  passée ; une question qui n'en offre pas est refusée, avec un motif lisible.
- [ ] **Étape 2 : écrire, voir vert, commiter**

---

### Tâche 6 : les traces, et le rapport de bug

**Fichiers :**
- Modifier : `ui-app/src/board/rapport-bug.ts` et son test
- Modifier : `ui-app/src/board/HistoriquePartie.tsx` si besoin

Les gestes manuels entrent déjà au journal à leur place chronologique, marqués
« Geste manuel ». Il manque deux choses :

1. Le rapport de bug reprend **la liste seule** des gestes manuels, en fin de
   document, pour qu'on l'audite d'un coup d'œil sans relire toute la partie.
2. Il porte la marque « corrigée à la main » de la tâche 2.

C'est ce qui permet de trancher, en lisant un rapport, entre un défaut du moteur
et une erreur de jeu.

- [ ] **Étape 1 : le cas rouge, écrire, voir vert, commiter**

---

### Tâche 7 : la preuve à l'écran

**Fichiers :**
- Modifier : `ui-check/tests/mode-manuel.spec.ts`

⚠ En LOCAL, jamais sur la production, jamais sur `.game`. Le montage est décrit
dans `.superpowers/sdd/2026-09-18-mode-manuel-plateau/task-8-report.md`.

Ajoute un second scénario au fichier existant, sur une partie **ORDINAIRE** :
jouer un tour normalement, mettre en pause, constater que le plateau s'est tu,
faire un geste à la main, reprendre, et constater que le moteur repose sa
question et que la partie continue.

C'est le seul test qui prouve la chaîne entière, et c'est celui qui dira si
l'idée tient vraiment.

- [ ] **Étape 1 : écrire, lancer, obtenir le vert, commiter**

---

### Tâche 8 : que la pause se voie aussi pendant une question

**Ajoutée le 20/09/2026, après le diagnostic qui a suivi la tâche 7.**

**Fichiers :**
- Modifier : `Fusion/marvel-lcg-src/src/engine/controller/controller.py`
- Modifier : `Fusion/marvel-lcg-src/tools/test_mode_manuel.py` (le cas rouge
  `pause_publiee_pendant_question_ouverte` existe déjà, il doit passer au vert)
- Modifier : `ui-check/tests/mode-manuel.spec.ts`

**Le défaut, établi et reproduit.** Mettre la table en pause pendant une
question déjà ouverte ne rend pas le plateau muet, sauf si cette question est
une question de tour de héros. Mesuré : sur le mulligan, la trame reste à
`(30, manuel_actif=False)` alors que `world.manuel_actif` est déjà vrai ; sur
une fenêtre d'interruption, `(82, False)` ne bouge pas non plus ; le témoin de
contraste, une question de tour de héros, passe bien de `(35, False)` à
`(36, True)`.

**La cause.** `DoGetInput` rend bien `None` (la tâche 1 est correcte) et
`ChoiceOne` re-pose la même question. Mais le seul rendu de ce chemin est
`SenderPlayer.PlayerOnEvent_Text` (`src/game/message/sender/sender_player.py`),
qui n'appelle `Present` que pour un message `WhenPlayerInTurn`. Sans `Present`,
pas de `ToDescriptor.World`, et `/get_world` continue de servir la trame
précédente.

**Pourquoi les cas verts ne l'ont pas vu.** `cas_reveil_dogetinput` ne ment
pas, il prouve moins : il monte un `DeviceManager` nu, sans monde ni rendu, et
s'arrête exactement là où le défaut commence. `cas_pause_publiee` s'appuie, son
docstring le dit, sur la partie automatique qui continue et rend d'elle-même.

- [ ] **Étape 1 : le cas rouge est déjà écrit**, et déjà constaté rouge.
- [ ] **Étape 2 : forcer le rendu**, dans `Controller.ChoiceOne`, sur le
  `if user_input == None`. Le mode manuel déclaré fait déjà exactement ça :
  `World.ManualLoop` force `self.render.PresentForceNoWait()` juste après avoir
  posé `manuel_actif = True`. La tâche 1 a repris le réveil et oublié ce rendu.

  ⚠ Deux gardes : distinguer la CAUSE du `None` (une bascule ou un geste
  drainé, jamais une expiration de minuterie), et se garder du
  `assert skip == False` de `PresentForceNoWait`.

  ⚠ **Ne pas corriger dans `PlayerOnEvent_Text`** : cela changerait le rendu de
  toutes les questions du moteur.
- [ ] **Étape 3 : la batterie entière**, au premier plan, sur un dossier
  jetable. Le témoin de contraste doit rester vert : c'est lui qui prouve qu'on
  n'a pas simplement rendu le cas insensible.
- [ ] **Étape 4 : déplacer la pause du scénario de bout en bout** au moment où
  un joueur la déclencherait vraiment, c'est-à-dire pendant une question qui le
  bloque, et non dans le calme du début de tour. Corriger au passage le
  commentaire qui se contredit (« aucune question n'attend » puis « une vraie
  question reste ouverte »).
- [ ] **Étape 5 : commiter.**

---

### Tâche 9 : que les corrections survivent (constat C1 de la revue finale)

**Le défaut, et il dément la promesse du chantier.** Les corrections faites
pendant une pause de partie ORDINAIRE disparaissent sans un mot par trois
chemins d'un seul clic : « Annuler », « Sauver », un rechargement.

La sauvegarde n'est pas un instantané de la table : `Scene` porte `seed`,
`rules`, `players`, `inputs`, et `GameSetup` REJOUE. Les gestes d'une partie
DÉCLARÉE survivent parce que `ManualLoop` les enregistre
(`self.scene.manuel_commands += appliquees`, `world.py:913`) et que `GameSetup`
les rejoue — mais **seulement sous `if self.world.rule.mode_manuel`**
(`game_run/game_session.py:135-160`). La branche de drainage de `DoGetInput`,
celle qu'emprunte une pause de partie ordinaire, jette son retour.

⚠ **« Annuler » est le pire des trois** : `GameSession.Undo` rejoue les ENTRÉES,
donc TOUTES les corrections s'évaporent, pas seulement la dernière. Et comme il
reconstruit le `World`, `manuel_actif` retombe à faux : le clic **reprend aussi
la partie en silence**, bandeau compris. Le joueur revient exactement dans le
bug qu'il venait de contourner.

- [ ] **Étape 1 : les cas rouges.** Un geste fait pendant une pause de partie
  ordinaire survit à une sauvegarde puis un rechargement ; et « Annuler » ne
  fait pas disparaître les corrections ni reprendre la partie.
- [ ] **Étape 2 : le correctif.** Enregistrer les gestes drainés dans
  `scene.manuel_commands` sur le chemin `DoGetInput`, comme `ManualLoop` le
  fait déjà, et faire que le rejeu au montage ne dépende plus de la RÈGLE
  `mode_manuel` mais de la présence de gestes à rejouer.
- [ ] **Étape 3 : le plancher, si et seulement si l'étape 2 se révèle trop
  risquée.** Griser « Annuler » et « Sauver » dès que `corrigee_a_la_main` est
  vrai, ou les faire passer par une confirmation qui NOMME la perte. Une limite
  dite vaut mieux qu'une limite muette. Si tu prends ce chemin, dis pourquoi.
- [ ] **Étape 4 : batterie entière + commit.**

---

### Tâche 10 : les trois mensonges par omission (I1, I2, I3 de la revue finale)

- [x] **I1, une ligne, et c'est le plus rentable du chantier.**
  `ui-app/src/board/HistoriquePartie.tsx:506` fait
  `type: estModeManuel(monde) ? 'manuel' : 'triche'` : la RÈGLE lue là où
  l'ÉTAT était voulu. En pause de partie ordinaire, chaque geste entre au
  journal en `'triche'`, or `rapport-bug.ts:389` filtre sur `'manuel'` : la
  section « GESTES MANUELS » **n'apparaît jamais**, ce qui vide la tâche 6 de
  son objet. Et le rapport affiche `[triche]` sous un en-tête qui crie
  « PARTIE CORRIGÉE À LA MAIN ». Ce n'est pas théorique : la fiche Echo du
  20/09 montre l'auteur lisant `[triche] Discard` et concluant « pas un défaut
  du moteur ». Correctif : `leMoteurSeTait(monde) || estModeManuel(monde)`.
  Un cas doit lier le producteur au consommateur, sinon rien ne le garde.

- [x] **I2, autorisation.** `AddPostSecurity` ne vérifie que `IsAuthenticate` :
  ni `SpectateurPeutLire`, ni `get_player_ids` que `/post` applique. Et
  `BandeauPause` est monté HORS de `.board-actions`, la seule chose que la CSS
  spectateur masque. Un spectateur peut donc cliquer « Reprendre » et « Passer
  la question » à la place d'un joueur assis. C'est le défaut pour lequel
  `SpectateurPeutLire` a été inversé le 15/09. Ferme les deux routes ET le
  plateau. Même chose pour `CoucheTriche`, qui s'arme sur `leMoteurSeTait` sans
  garde spectateur et donne le clic droit et le clavier au spectateur.

- [x] **I3, dire la vérité.** Le journal est local au navigateur : le rapport
  ne contient aucun geste des autres joueurs, tout en annonçant « pour audit
  rapide ». N'AGRÈGE PAS entre clients, c'est une autre affaire. Dis-le dans le
  document, comme `gestesManuelsIncomplets` le fait déjà pour le tampon.

- [x] **Les mineurs**, si le temps le permet : `motifRefus` jamais remis à plat
  entre deux pauses ; `pause_a` affiché en heure serveur au format
  `2026-09-20 17-12`, illisible comme durée ; `/manuel_pause` sans la garde
  symétrique de `/manuel_passer` (un `actif: false` sur une partie DÉCLARÉE la
  rendrait bavarde sans moyen de revenir) ; la docstring de
  `BasculerPauseManuelle` qui dit encore « CE SEUL booléen » alors qu'elle en
  écrit quatre.
