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

## 5. Petits restes
- Une commande de console inconnue fait planter le moteur (NameError).
- Compteurs de combat des stats de fin de partie vérifiés au harnais seulement, pas en partie réelle.
- Éventail des manigances annexes jamais vu à l'écran.
- Tests rouges anciens (preparation-v2 360/390/480, fanmade-createurs, modale-heros Storm) ; clé « Accueil » inutilisée.
- Nettoyage : copie `/mnt/c/Users/arnau/Desktop/MarvelLCG-build` (retirer les jonctions avec `cmd.exe /c rmdir`
  AVANT de supprimer), `launcher_essai_fin.py` et `config-essai-fin.json`, specs jetables `ui-check/tests/zz-*`.
