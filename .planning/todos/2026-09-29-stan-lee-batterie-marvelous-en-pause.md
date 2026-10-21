# Stan Lee : batterie « Marvelous » en pause (29/09/2026)

**REPRISE le 21/10/2026** (demande de l'utilisateur). La liste de cas a grandi depuis : **3 076 cas**
(1 538 cartes) au lieu de 2 808, des héros ayant été insérés au milieu (les index ne désignent plus les
mêmes cartes). Les 1 462 cas du rapport partiel sont tous encore dans la liste ; il en restait **1 614**.
Nouvelle variable `MARVELOUS_SAUF=<rapport.json>` (`batterie_test_capacites.py`) : ne rejoue que les cas dont le
NOM n'est pas dans ce rapport. Lancée en arrière-plan : harnais gelé dans `/tmp/marvelous-frozen/`, dossier de jeu
`.game-src-stanlee`, `PARALLELES=3`, `nice 19`, rapport `/tmp/marvelous-suite.json`, journal
`/tmp/marvelous-suite.log`. À analyser ensuite avec `analyser.py` en fusionnant les deux rapports
(`.planning/stan-lee/marvelous-partiel-0-1461.json` + celui-ci).

Arrêtée à la demande de l'utilisateur (trop de consommation). Reprise prévue la
semaine du 05/10/2026.

## Où on en est

- Batterie de 2 808 cas (1 404 cartes signature x 2 : témoin + Stan Lee).
  **Cas 0 à 1461 passés**, aucun trou dans cette plage. Reste 1462 à 2807.
- Rapport partiel sauvegardé : `.planning/stan-lee/marvelous-partiel-0-1461.json`
  (format `{"cas": [...]}`, lisible par `analyser.py`).
- Résultat de l'analyse sur les 731 cartes appariées : **VERT 557, ÉCART 12,
  NON CONCLUANT 162**, INCOMPLET 0.

## Les 12 écarts déjà connus (témoin vert, Stan Lee rouge)

11 sont « injouable » (`CanPlayBy` faux pour Stan Lee), 1 reste en main :
09005 Master of the Mystic Arts, 13006 Wasp Sting, 23008 Repulsor Beam,
23010 Scorched Earth, 23011 Full Auto, 26011 Phase Disruption, 32009 Bulletproof
Protector, 34013 Phoenix Firebird, 36009 Weather Goddess, 40003 Mind Scan,
46009 Arctic Attack, et **38007 Energy Transfer** (événement resté en main).

Cause pas encore cherchée : à ouvrir avec `CanPlayBy` de ces cartes (souvent une
condition sur le héros nommé ou sur le trait/l'identité). Corriger le MOTEUR
(extension de `consider_as` dans `stanlee/stan_lee/__init__.py`), pas l'écart.

## Les 162 non concluants

Le témoin est déjà rouge (cible absente, coût spécial) : 148 « injouable »,
11 « jamais arrivée en main », 2 « événement reste en main », 1 « jouée mais pas
en jeu ». Ce sont des cas à écrire à la main, un par un, comme le dit le README
de `tools/generateurs-marvelous/`.

## Pour reprendre

1. Recréer la copie gelée et le dossier de jeu dédié (jamais `.game`) :
   `cp -a .game-src .game-src-marvelous` ; la copie gelée `/tmp/marvelous-frozen/`
   a disparu si la machine a redémarré. Elle contient `test_capacites.py`,
   `decks-de-test.json` (de `tools/`) et le dossier `generateurs-marvelous/` :
   la refaire par `mkdir /tmp/marvelous-frozen && cp tools/test_capacites.py
   tools/decks-de-test.json /tmp/marvelous-frozen/ && cp -a
   tools/generateurs-marvelous /tmp/marvelous-frozen/` (le but : que des
   retouches du harnais en cours de route ne changent pas la batterie).
2. Lancer **seulement les cas 1462 à 2807** : le harnais n'a pas d'option de
   départ, donc soit rejouer `CAS_INDEX=<n>` en boucle, soit ajouter une variable
   `MARVELOUS_DEBUT` dans `batterie_test_capacites.py` (à faire d'abord, c'est
   petit). Ne pas relancer les 2 808 : ce serait refaire ce qui est fait.
3. Avant de conclure sur un rouge : le rejouer seul (`CAS_INDEX=<n>`), les rouges
   en masse en parallèle sont des artefacts (voir mémoire
   `batterie-rouges-en-masse-artefact`).
4. Après les corrections moteur : batterie complète de cartes (PROCESSUS-CARTE
   §6bis) à cause des retouches partagées (`CanBeInstead` de
   `WhenMinionWouldEngagePlayer`, `Fleeting`, `Alias`), jamais en même temps.

## Ce qui attend aussi (rien n'est commité ni déployé)

Correctifs de règles MC4DB (10 cartes officielles, Multiverse, 5 mots-clés),
Fleeting/Alias, fiches de mots-clés, titres français de l'écran de prépa (déjà
en prod par 6 fichiers), scripts d'import d'images. Déploiement complet
`deployer.ps1 -Code` seulement sur le « déploie » de l'utilisateur, après avoir
vérifié qu'aucune table n'est active.

## Après Stan Lee

Passage en français de tout ce qui reste en anglais quand on joue en français,
à faire avec Sonnet (annoncer le choix de modèle avant de commencer).
