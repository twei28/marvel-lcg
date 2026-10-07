# La refonte des sons

Cadrage du 15/09/2026, question par question. Ce document fait foi : ce qui n'y
est pas n'est pas décidé.

## Le problème, dans ses mots

« Et après il faudra revoir les sons aussi » (14/09), puis, interrogé sur ce qui
le gêne, **les quatre réponses à la fois** : les sons eux-mêmes, le moment où
ils se déclenchent, le mélange, et ceux qui manquent sur les mouvements de
cartes.

Ce n'est donc pas un réglage, c'est une refonte.

## Ce qui existe, et qu'on ne redécouvre pas

Tout est déjà relevé dans `docs/reference/SONS-DECLENCHEURS.md` (06/09/2026) :

- **21 sons**, dont les noms sont FIGÉS dans le moteur
  (`src/game/message/message.py`, `SOUND_NAMES`). On peut remplacer n'importe
  lequel des 21 fichiers sans toucher une ligne de code ; en ajouter un
  nouveau demande de modifier le moteur.
- Le moteur décide, le plateau obéit : `WorldDescriptor.sound_name` à chaque
  rendu, et `sons.ts` joue `<nom>.wav`.
- Deux règles déjà en place : rien ne se joue quand l'onglet est caché, rien ne
  se joue pendant qu'on attend une décision du joueur, **sauf le gong de phase**.
- Le volume est **figé à 20 %** dans le code (`const VOLUME = 0.2`), sans
  curseur.
- Deux sons ne sont jamais déclenchés dans cette version : `directattack.wav` et
  `cardpick.wav`.

## Les décisions

### Les fichiers : une liste de courses, pas une fabrication

⚠ **Je ne sais pas fabriquer de fichier audio.** Décision : je rends une liste
de courses (ci-dessous), l'utilisateur va chercher les sons dans une banque
libre, et je m'occupe du reste (nommage, emplacement, vérification que chacun
se déclenche où il faut).

### Les sons de mouvement : au plateau, pas au moteur

Choix retenu : **le plateau les joue lui-même**, là où la carte vole
(`CoucheAnimations`). Il sait exactement quand elle décolle et quand elle se
pose ; le son colle à l'image à la milliseconde, et le moteur n'est pas touché.

⚠ Conséquence assumée : cette famille ne suit PAS la règle des 21 noms figés.
C'est une seconde source de son, à côté de celle du moteur, et il faudra qu'elles
ne se marchent pas dessus.

### Le reste

Le mélange (volume, sons simultanés) et les déclencheurs mal placés restent à
traiter, mais ils ne dépendent d'aucun fichier : ils se travaillent tout de
suite.

## LA LISTE DE COURSES : SEPT SONS, PAS VINGT ET UN

⚠ **Correction du 15/09/2026, et c'est l'utilisateur qui a raison.** J'avais
présenté les 21 noms du moteur comme 21 sons à trouver. Ce sont 21
DÉCLENCHEURS. Sa réaction : « c'est un jeu de cartes, on n'a pas besoin de 21
sons, on en a besoin de 6-7 maximum ».

**Rien n'oblige à un fichier différent par nom.** Le plateau joue `<nom>.wav` :
il suffit de déposer le MÊME son sous plusieurs noms. Sept sons couvrent donc
les vingt et un déclencheurs.

### Les sept familles

| Le son | Ce qu'il doit évoquer | Durée | Les noms à servir |
|---|---|---|---|
| **Capacité** | Une capacité qui part. Discret, presque un clic habillé. ⚠ Il sonne des dizaines de fois par partie : c'est le seul qui reste SEUL dans sa famille, parce qu'un son marquant ici devient insupportable en dix minutes. | 80 à 150 ms | `activate` |
| **Impact** | Le coup porté ou encaissé. Sec, physique, sans traîne. | 100 à 200 ms | `damage`, `target`, `directattack` |
| **Carte qui bouge** | Le frottement du carton : piochée, posée, rangée, équipée, mélangée. | 80 à 200 ms | `draw`, `carddrop`, `set`, `equip`, `cardpick`, `shuffle` |
| **Retournement** | Le claquement d'une carte qui bascule ou se révèle. | 150 à 300 ms | `flip`, `reveal` |
| **Jeton** | Un pion qu'on pose ou qu'on retire. Léger, mat. | 60 à 120 ms | `token`, `addcounter`, `removecounter`, `gainlp` |
| **Disparition** | Ce qui quitte la table : détruit, banni, annulé. Le seul de la liste qui a le droit d'être un peu marquant, parce qu'il est rare. | 300 à 500 ms | `destroyed`, `banished`, `negate` |
| **Gong** | La main change de camp. Grave, il a le droit de durer : c'est le seul qui perce pendant qu'on pose une question au joueur. | 400 à 800 ms | `phase`, `nextturn` |

⚠ **La brièveté prime sur tout le reste.** Ces sons partent en rafale, plusieurs
`activate` peuvent s'enchaîner en une seconde. Au-delà d'une demi-seconde, ils
se chevauchent et deviennent une bouillie. Seuls « gong » et « disparition »
échappent à la règle, parce qu'ils sont rares.

⚠ Deux noms ne servent à rien (`directattack`, `cardpick`) : déclarés par le
moteur, jamais déclenchés dans cette version. Ils sont dans la liste par
propreté, personne ne les entendra.

### Ce qui n'existe pas encore : l'interface

Demande de l'utilisateur, hors des 21 : **le survol d'un bouton, le survol d'un
personnage dans les menus, la carte qui vole**. Le moteur ne connaît aucun de
ces moments.

Ils vivront donc côté plateau, comme les sons de mouvement (décision plus haut).
Compte **un ou deux fichiers de plus**, très courts (30 à 80 ms) : un survol qui
dure s'entend comme un défaut dès qu'on balaie l'écran à la souris.

### Le compte final

**Sept fichiers pour le jeu, un ou deux pour l'interface.** Neuf au maximum, là
où la première version de cette spec en demandait vingt et un.

## Ce qui reste à établir avant d'écrire du code

⚠ **Quels déclencheurs tombent au mauvais moment ?** L'utilisateur dit que
certains arrivent mal, mais lesquels n'est pas su. À lui faire nommer en jouant,
ou à relever en écoutant une partie du début à la fin. **Ne rien déplacer avant
de savoir quoi.**

⚠ **Le mélange** : faut-il un curseur de volume, une limite au nombre de sons
simultanés, ou les deux ? Le volume est aujourd'hui figé à 20 % sans réglage.

## Statut

**Cadré le 15/09/2026.** La liste de courses tient en sept sons plus le survol.
Rien ne commence côté fichiers tant que l'utilisateur ne les a pas ; le volume,
les simultanés et les déclencheurs peuvent partir avant, dès qu'on saura
lesquels le gênent.

## Décisions du 06/10/2026 (reprise du chantier)

Questions posées une à une :
- **Fichiers** : pris dans une banque libre CC0 que je propose (packs Kenney en
  priorité), écoutés par l'utilisateur sur une page de comparaison (actuel
  contre trois candidats par famille) AVANT tout remplacement. Remplace la
  décision du 15/09 « l'utilisateur fournit les fichiers ».
- **Mélange** : curseur de volume des effets dans Réglages « Image et son »
  (séparé de la musique) ET au plus 2 sons simultanés (un 3e pendant une
  rafale est sauté).
- **Déclencheurs** : l'utilisateur ne se souvient plus lesquels tombaient mal ;
  on n'y touche pas.
- **Sons nouveaux côté plateau** : sans préférence exprimée, retenus d'après la
  demande du 15/09 : carte qui vole (calée sur l'animation), survol des
  boutons et des héros des menus, gestes du mode manuel joués avec le son de
  leur famille. Pas de fanfare de victoire ou de défaite (jamais demandée).
- **07/10/2026, durées** : l'utilisateur veut « de préférence des sons d'une
  durée similaire à l'originale », et plus de candidats par famille. Cela
  remplace la règle « la brièveté prime » et les plages de durée du tableau
  des sept familles. La limite de 2 sons simultanés reste le garde-fou
  contre la bouillie en rafale.

## Statut au 07/10/2026 : INTÉGRÉ (non commité, non déployé)

Choix de l'utilisateur sur la page d'écoute (version 4, Freesound CC0) :
Capacité B, Impact D, Carte qui bouge J, Retournement E, Jeton H, Gong I,
Survol K, Carte qui vole I ; **Disparition : garder l'actuel**. Détail des
sources et des noms servis : `Fusion/marvel-lcg-src/assets/sounds/SOURCES.md`.

- Fichiers : chaque son copié sous tous les noms de sa famille, niveau ramené
  entre −18 et −21 dB RMS (crête −1 dB) pour rester proche de la Disparition
  conservée ; `survol.wav` et `vol.wav` ajoutés. Anciens fichiers sauvegardés
  hors dépôt (récupérables aussi par git).
- Plateau (`ui-app/src/board/sons.ts`) : curseur « Volume des bruitages » dans
  Réglages, onglet Son (défaut 20 %, clé `marvel-board-volume-sons` partagée
  avec le lanceur) ; au plus 2 sons simultanés ; survol des boutons des
  fenêtres Menu et Réglages (35 % du volume, un toutes les 80 ms, souris
  seulement) ; `vol.wav` au décollage de chaque carte qui vole ; gestes du mode
  manuel sonorisés via `triche.ts`, un son du moteur de la même famille dans
  les 600 ms qui suivent est sauté (pas de doublon).
- Lanceur (`public/js/prepare/sons.js`) : même volume partagé, même limite de
  2 sons, survol des boutons et tuiles.
- Inchangé : réglage « Bruitages » coupé = silence, onglet caché = silence,
  voile d'ouverture, pas de son pendant une question sauf le gong.
- Vérifié au navigateur le 07/10/2026 (moteur d'essai, espion sur
  `HTMLMediaElement.play`) : sons du moteur à 20 %, curseur à 60 % suivi par
  les sons suivants, survol à 35 % dans les Réglages et le lanceur, geste
  manuel (F7, Ctrl+D, double-clic) avec son de famille, `vol.wav` au décollage
  d'une mise en jeu (main vers table).
- ⚠ Le vol ne suit PAS la règle « pas de son pendant une question » : elle
  vise le son répété du moteur ; appliquée au vol, elle le rendait muet en
  mode manuel (question garée) et pendant presque toutes les pioches.
- ⚠ Constaté hors périmètre : une PIOCHE (deck vers main) ne fait voler
  aucune carte, donc pas de `vol.wav`. `CoucheAnimations` n'anime qu'une carte
  APPARUE dans la main, or le deck affiche désormais sa carte du dessus avec
  son vrai identifiant : la carte piochée « existait » déjà. Animation à
  corriger à part (la mise en jeu et la défausse depuis la main volent bien).
