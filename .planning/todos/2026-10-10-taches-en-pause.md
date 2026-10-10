# BACKLOG au 10/10/2026 (mis à jour en fin de session, à la demande de l'utilisateur)

Règles : UNE tâche à la fois, un point d'avancement régulier, on travaille sur « Étape par étape Bis ». Rien ne se
déploie sans « déploie » (annonce de 10 min dans l'admin, puis `bash deploiement/deployer-tout.sh`).

## 1. Déploiement en attente (tout est commité sur `mode-manuel`, rien n'est en ligne depuis 76e23ddc)
Bis de Codex (2a50ea4d), mise en place dans l'ordre du livret (960c8765, ee161d42, 396c0054), choix à plusieurs effets
(6878489f, d8efcd22), liserés nets sans halo (f4c3adf4, 114d3d3c), ombre et lueur des cartes (deb66b13, 636fb69e,
d21d904a), manigances principales côte à côte (960eab9f), statistiques de fin de partie (69c7d0b2), écran du méchant
(df6bda41), Échap/croix (9aa79adc, 5a7d4e28), relecture du bilan (31ea4933), aide tactile (fe3edb46), zone 3 téléphone,
mention légale, « Pour débuter » et exploits retirés, Curseurs, titres des manigances à gauche, refonte essai (82ca79f6).
Avant : vérifier les entrées nouveautés, puis déployer depuis une COPIE PROPRE du commit (worktree, jonctions
node_modules et assets/pics, `_a_supprimer/` à créer pour la sauvegarde du code qui a échoué le 10/10).

## 2. Code en pause, NON commité sur mode-manuel : sauvegardé sur la branche `en-pause/2026-10-10`
(le dossier de travail le contient toujours ; la branche n'est qu'une copie de sûreté)
- Finitions du téléphone : phase du méchant en feuille basse (cartouche-essai-tel.css, deroule-essai-telephone.test),
  paysage lisible (Board.tsx, board.css, echelle-paysage.test), languette Journal sur la main (VoletJournal.css), appui
  long = jouer dans la main (MainPortrait), aide (VoletAideAuto), 4 tests menus-mobile périmés, telephone-finitions.spec.
- Salon invité (fiche 2026-10-09-salon-invite.md) : salon/app.js, salon.html, salon.css, server_get.py,
  server_new_game.py, test_authentification.py, hunk publierEquipeHote de prepare/app.js, entrées dico-en.js et
  nouveautes.js.

## 3. Décisions à prendre
- Phase du méchant : on garde le Bis. Supprimer ou non ma version « essai » (cartouche-essai, interrupteur par compte
  dans /admin, prévu pour Yarro) ?
- Mode sobre : le liseré de camp est caché sous l'anneau noir (2 px sous 3 px), à régler comme le normal ?

## 4. Fiches en attente
- Connexion / inscription PC (2026-10-09-connexion-inscription-site.md).
- Pages orphelines : Replay, Report, Crédits, Sandbox, Rejoindre.
- Choix du héros, plus de héros visibles (2026-10-09-choix-du-heros-plus-de-heros.md) : vérifier ce qui reste.

## 5. Petits restes (traités le 10/10/2026 après-midi, NON commité, NON déployé)
- ✅ Console : une commande inconnue (`/debug?xyz`) levait une NameError jusqu'à la boucle du jeu. `Console.Execute`
  la rattrape, la journalise et la signale au plateau (`ErrorOccurred`), et la relève en test. Témoin :
  `tools/test_console_inconnue.py` (inconnue signalée, valide toujours exécutée), rouge avant, vert après ;
  `test_mode_manuel` 81/81.
- ✅ Stats de fin : 3 vraies parties au pilote (Rhino graine 3, Klaw graines 7 et 11), comparées au journal.
  Deux trous corrigés : un allié vaincu par le coup qu'il défendait perdait sa défense et ses dégâts subis
  (plus de contrôleur), et le coup fatal sur le dernier héros n'était jamais compté (la partie finit avant
  `AfterFaceDealDamage`). `degats_subis` se compte désormais dans `CanHealth.TakeDamageWithOverkillTarget`, avant
  la défaite ; l'excédent reporté sur la cible du débordement est compté à cette cible. `JoueurDe` retombe sur le
  propriétaire. Une attaque annulée (Backflip) ne compte plus 1 dégât subi. Le compteur historique
  `total_damage_taken` n'est pas touché (mêmes trous, à décider). Cas « Stats de partie » du harnais vert.
- ✅ Éventail des annexes vu à l'écran (Tower Defense, 1 à 7 annexes, 1920 et 1366 ;
  `.planning/captures-eventail/`) : les cases rétrécissent, chaque titre reste lisible, le survol ouvre la carte.
  Défaut trouvé et corrigé : rangée pleine, la dernière annexe passait sous la languette fixe « Aide », qui en
  cachait la menace. `bande-manigances.css` lui réserve 30 px. Plateau local reconstruit (`deployer.sh`,
  bundle `board-ZKC8CJBP.css`) puis remesuré sans injection : 1880 < 1893 en 1920, 1338 < 1339 en 1366.
- ✅ Tests rouges anciens, tous en `--project=pc` (leur périmètre déclaré) : preparation-v2 5/5 (le test « V1 par
  défaut » décrit maintenant le mode téléphone ; la V2 rend 44 px à la langue et à l'affichage, que
  `icones-entete.js` forçait à 34 px), modale-heros 3/3 (Storm a un art alternatif : témoin « sans option » =
  Agatha Harkness), fanmade-createurs 3/3 (modale de Storm validée, « Set de base » accepté).
- ✅ Clé « Accueil du jeu » retirée de `tel-pages.js` (jamais lue ; prepare/app.js a la sienne).
- ✅ `test_capacites` nv001, 60079 (et une centaine d'autres, d'où les 116 rouges de la batterie du 10/10 02h49) :
  RÉGRESSION DU HARNAIS, pas du moteur. da82e232 (09/10) avait tenté d'échanger `01001a`/`01001b` dans les cas
  existants via le nom provisoire « Peter Parker », sans la dernière étape : `Exhaust('Peter Parker')` visait une
  forme absente et fabriquait un doublon détaché, qui fait tomber le rendu. Trouvé par bissection (arbre complet
  bon à ca43692a, mauvais à da82e232 ; moteur du 09/10 + harnais du 08/10 = vert). 107 lignes de cas rétablies
  telles qu'au 08/10, repérées par leur position.
- ✅ Compteurs historiques (`total_damage_taken/dealt`, maxima, par siège) et `degats_mechant/sbires` : le comptage
  passe d'aptitudes sur `AfterFaceDealDamage` à un appel direct `CompterDegats` depuis CanHealth, avant l'envoi.
  Le coup qui gagne la partie (dernier stade du méchant) n'était compté nulle part : nouveau cas « Stats de partie
  — le coup qui GAGNE la partie », rouge avant, vert après. Partie réelle Rhino graine 3 : historique des dégâts
  subis 10 → 16 (Black Cat et le coup fatal), onglet Stats inchangé. Sémantique conservée (dégâts « infligés »
  avant prévention), seuls les trous sont bouchés.
- ✅ Nettoyage : moteur d'essai du port 2331 arrêté par son PID ; worktree `MarvelLCG-build` (propre, commit
  636fb69e) retiré par `git worktree remove` APRÈS `cmd.exe /c rmdir` de ses deux jonctions (pics 6892 et
  node_modules intacts) ; `launcher_essai_fin.py`, `config-essai-fin.json` et `.game-essai-fin` supprimés ;
  14 specs `zz-*` supprimées, dont `zz-gagner` et `zz-relecture-fidele` qui étaient commitées (`git rm`, en
  attente de commit). Aucun fichier suivi d'autre perdu.

## 6. Ajouté le 10/10/2026 après-midi
- ✅ Luke Cage (rapports n73, n74, n75 + audit du pack) : branche `luke-cage-correctifs`, fiche
  `2026-10-10-luke-cage-audit.md`. À FUSIONNER dans `mode-manuel` puis déployer ; réponses aux joueurs prêtes.
- ✅ « Étape par étape Bis » devient « Étape par étape », l'ancienne présentation retirée (décision utilisateur) :
  branche `phase-mechant-etape-par-etape` (46237b44), worktree `C:\Users\arnau\Desktop\MarvelLCG-bis`. À FUSIONNER :
  ⚠ touche `DeroulePhase.tsx` et `dico-en.ts`, que le code EN PAUSE modifie aussi (stash ou fusion à la main).
  ⚠ Le worktree porte deux JONCTIONS (`ui-app\node_modules`, `Fusion\marvel-lcg-src\assets\pics`) : les retirer avec
  `cmd.exe /c rmdir` AVANT `git worktree remove`.
- ⏳ Aperçus de la fenêtre « Choisis ta phase du méchant » (`public/img/phase-modes/etape-1..4.jpg`, 05/10) : ils
  montrent l'ANCIENNE présentation. À refaire avec le nouveau cartouche (décision : plus tard).
- ⏳ Nouveautés fr + en à écrire avant le déploiement (Luke Cage, Étape par étape unique, stats de fin, console).
