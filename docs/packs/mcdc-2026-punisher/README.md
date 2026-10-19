# Campagne « La ville ne dort jamais » (MC/DC 2026, Punisher) : point de reprise

Fait le 19/10/2026. **Rien n'est codé dans le jeu** : tout ce dossier prépare le travail. Une nouvelle session doit lire ce fichier d'abord.

## Qu'est-ce que c'est

Campagne fan-made de 4 scénarios autour d'un trafic d'armes à New York (Punisher), créée par l'équipe **MC/DC** (événement du 16 au 18/10/2026
chez Huzzah Hobbies, Ashburn, Virginie). Titre français : **« La ville ne dort jamais »**. Elle utilise du contenu officiel de *Peur de Rien*
(Fear No Evil) : Kingpin, Cops, Tracksuit Mafia, les 5 manigances interchangeables.

## Les fichiers

| Fichier | Contenu |
|---|---|
| `cartes.md` | Relevé de **toutes les cartes** (≈ 143, 15 sets), carte par carte, relu en 300 dpi : texte, valeurs, icônes, illustrateur. Légende des icônes, comparaison avec un second relevé. |
| `regles-fr.md` | Livret de règles français : les 4 scénarios, règles de campagne, FAQ, noms français, **crédits complets**. |
| `maquette-ville.html` | Maquette de l'affichage des 9 lieux sur le plateau (voir « Décisions »). |
| `paquets-cartes/MC x DC 2026 - campagne Punisher/` (hors dépôt) | PDF des cartes (286 p., 291 Mo), PDF du livret FR et son `.txt`, `scans/pNNN.jpg` (une face par page, 200 dpi), planches d'aperçu. |

Sources : PDF des cartes sur Google Drive (propriétaire team@mcdc.fun, fichier `2026_scenario_print_300dpi.pdf`), livret FR sur
`bubblepack.org/downloads/la-ville-ne-dort-jamais-regles-fr-v1.pdf`, sites `mcdc.fun`. Un second PDF du même dossier Drive,
`2026_full_art_300dpi.pdf` (15 Mo, alliés/soutiens/améliorations de base en pleine illustration, numéros MC DC 6142+), **n'a pas été téléchargé**.

## Décisions de l'utilisateur (à respecter)

1. **Icônes** (tranché sur les cartes elles-mêmes, 19/10/2026) : « !! » = **Crise** ; croix à trois pointes + = **Amplify** ; triangle « toit de maison » + =
   **Accélération** ; carré « carte + » = **Aléas / Hazard** (une carte de rencontre en plus au premier joueur). Un autre relevé (fichier
   `Marvel_Champions_Scenarios_Extraction.md`) permute les noms : **le mien est le bon**, voir `cartes.md`. Le pictogramme à trois silhouettes (p271) = « par groupe / par table ».
2. **Hawkeye** (p283-284) = le vrai Hawkeye avec une **nouvelle version** de ses deux cartes (alter-ego : une Réponse en plus, l'Action change ; héros : THW 2 / ATK 1 / DEF 2, portée).
   Son deck officiel existe déjà dans le jeu (`04002` Arc, `04003` Carquois). **À vérifier avant de coder** : les cartes « ARROW » (flèches) existent-elles ?
3. **Contenu de Peur de Rien** (Kingpin, sets Cops et Tracksuit Mafia, manigances Art Museum Heist / The Getaway / The Raft Breakout / Protection Racket / Stop the
   Presses) : **à reprendre du jeu officiel** (confirmé par l'utilisateur).
4. **Affichage des neuf lieux sur le plateau : A + B** (recommandé, maquette validée pour le principe) : la table ne montre que **mon territoire** (chef de ma
   rangée, sbires engagés), une **mini-carte 3×3** reste dans un coin (chef par rangée, pion de position, pastille des cartes attachées), un clic ouvre une
   **fenêtre « La Ville »** déplaçable avec les 9 lieux en grand ; un sélecteur « voir le territoire de [joueur] » si deux joueurs sont dans des territoires
   différents. **Coins coupés des panneaux : 6 px** (pas plus). L'utilisateur n'a pas encore dit explicitement « A + B » : il a dit « ça a l'air pas mal A et B ».
5. **Crédits** : nommer **MC/DC** et toute l'équipe de `regles-fr.md` dans les remerciements du jeu (organisateurs, dév., testeurs, Batou et l'équipe de la version
   française, Huzzah Hobbies) + les illustrateurs imprimés sur chaque carte.
6. **Pas de code ni de gros dépense de tokens sans demande** : l'utilisateur est limité en tokens.

## Ce que le moteur devra savoir faire (par ordre logique)

1. **Scénario 1, The Big Apple** : 9 lieux en grille 3×3 (cartes « lieu », déplacement orthogonal, pion par joueur, départ Midtown), **3 territoires** = 3 zones de jeu
   séparées (un CAPO par rangée, pas d'interaction entre territoires, les méchants ne s'activent que contre les joueurs de leur territoire), deck de **pistes (LEADS)**
   avec compteurs et conditions par lieu, CAPO à deux faces (A/B), icônes Acceleration / Hazard / Amplify / Crise, sbires « attachés à un lieu » (Overdrive, Muse, Screwball),
   manigance principale à 3 stades avec Trafiquant d'armes. Campagne : mémoriser le lieu de la dernière piste et le CAPO Trafiquant.
2. **Scénarios 2 et 3** : sous-méchants Hobgoblin (Pumpkin Bomb) et Jigsaw, set Liste Noire du Punisher, **Punisher actif** avec Target Lock (Précision) face CONCENTRÉ / DISTRAIT,
   manigance « Un dernier meurtre », environnement Justice ou Châtiment, armes à munitions (compteurs).
3. **Scénario 4, Kingsfall** : multijoueur par assemblées de 2 à 4 groupes (Soutien des Citoyens, Longue Vie / À bas, Le Roi), **le plus lointain**, peut-être hors périmètre du jeu solo/coop.
4. Campagne : récompenses (Caisses de technologie saisies, Cache d'Armement, allié Punisher), mode « experte » (PV conservés), 4 défis optionnels.

Pour **chaque carte** : suivre `docs/reference/PROCESSUS-CARTE.md` (règle impérative du projet), avec le scan `scans/pNNN.jpg` correspondant.

## État du travail à la fin de cette session (19/10/2026)

- Relevé des cartes : **fait et relu** (voir marques `[?]` restantes dans `cartes.md`, très peu).
- Livret FR : **fait**. Maquette : **faite**.
- Tout ce qui précède est **committé** (branche `sauvegarde-cle-usb-2026-10-14`).
- Hors campagne, **non déployé** : couleurs de la phase du méchant en Épuré/Normal, pochettes des boîtes du choix du méchant, fenêtres glissables de partout, menu de carte en fenêtre,
  roue du hasard, polices `.woff2`, corrections de tests, bandeau d'annonce (déjà posé en ligne le 19/10/2026 pour 180 min). Le jeu **en ligne** est celui du déploiement manuel du 18/10/2026.
- Au prochain déploiement depuis cette machine Linux : voir la note de déploiement ci-dessous.

## Note de déploiement (machine Linux, sans Windows)

`deploiement/deployer-tout.sh` et `deployer.ps1` ne tournent pas ici. Séquence manuelle utilisée le 18/10/2026 : build `bash ui-app/deployer.sh` ; archive tar de
`Fusion/marvel-lcg-src` et `site` avec les exclusions de `deployer.ps1` ; `scp` ; sur le serveur, raser `src`, `public` et la racine de `site/` (sauf `comptes.json`, `*.db`, `rapports`) puis
extraire ; **envoyer à part `data/palettes-heros-corrections.json`** (exclu de l'archive, et le script officiel recopierait la version du serveur par-dessus : comparer avant, fusionner
si le serveur a des palettes en plus) ; redémarrer `narwhal` ; `python3 navigateur/publier.py --oui` (play.) ; images : étape « Images custom » du `.ps1` à refaire à la main
(scans manquants, vignettes `generer_vignettes.py`, et pour play. : `resoudre-images.py` + `installer-images.py`). Détails dans `docs/` et dans la conversation.
