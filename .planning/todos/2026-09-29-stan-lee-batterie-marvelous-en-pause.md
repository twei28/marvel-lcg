# Stan Lee : batterie « Marvelous » en pause (29/09/2026)

**CLOS le 21/10/2026, arrêté à la demande de l'utilisateur** (« ça demande trop d'effort pour un perso »).

Reprise le 21/10 : la liste de cas avait grandi (3 076 cas, 1 538 cartes), les 1 614 manquants ont été
rejoués (variable `MARVELOUS_SAUF`). Bilan sur 1 538 cartes : **VERT 1 163, ÉCART 21, NON CONCLUANT 354**.

**12 écarts corrigés** (vérifiés un par un, 2/2) :
- 23008, 23010, 23011 (War Machine) : Stan Lee reçoit l'aptitude « Locked and Loaded » (5 jetons `ammo`),
  `APTITUDES_PRETEES` dans `stanlee/stan_lee/__init__.py` ;
- iw008, iw009 (Invisible Woman), ok012, ok013, ok015, ok016 (Okoye), 13006 Wasp Sting (côté TINY) : Stan Lee
  reçoit les TRAITS des identités empruntées (`TraitsAPreter`) ;
- ze006 Wrath of Olympus et 40003 Mind Scan : artefacts du CAS, pas du moteur (`generer_cas.py` : exigence
  de couleur, menace sur le complot posée APRÈS le remplacement de la main).

**9 écarts documentés, NON corrigés** : cartes qui dépendent de la MISE EN PLACE propre à leur héros, que
Stan Lee n'a pas (jetons / cartes mises de côté) : 09005 Master of the Mystic Arts (deck d'Invocation, Doctor
Strange), 26011 Phase Disruption (amélioration « Intangible », Vision), 32009 Bulletproof Protector (carte
Tenace, Colossus), 34013 Phoenix Firebird (Phoenix Force), 36009 Weather Goddess (deck météo, Storm), 38007
Energy Transfer (amélioration « Touched », Rogue), 46009 Arctic Attack (Frostbite, Iceman), as004 Burst It! et
as007 Sell It! (Spider Armor, Armored Spidey). Les corriger = équiper le deck de Stan Lee des cartes mises de
côté de chaque héros prêté, héros par héros, avec des conflits possibles quand deux héros partagent un deck
additionnel. Pas fait : la carte dit « si ça semble devoir marcher, ça marche ». Wasp Sting côté GIANT reste
impossible (transformation).

**Non fait** : les 354 cas NON CONCLUANTS (témoin rouge : cible absente, coût spécial) à écrire à la main.
La batterie complète rejouée après ces corrections a été arrêtée à ~1 060 cas sur 3 076 : 0 cas Stan Lee passé de
vert à rouge ; 80 passés de rouge à vert (dont des témoins, grâce à la menace posée). 6 témoins de cartes de dos
de face (ex. 34002b Phoenix Force) « ne sont pas en main » : la vérification `AssertJouable`, absente de la
passe de septembre, les rejette ; ce n'est pas une régression du moteur.

Ancien état (29/09), conservé pour mémoire :

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
