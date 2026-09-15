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

## LA LISTE DE COURSES

Durées indicatives. ⚠ **La règle qui prime sur tout : court.** Ces sons partent
en rafale, plusieurs `activate` peuvent s'enchaîner en une seconde. Au-delà
d'une demi-seconde, ils se chevauchent et deviennent une bouillie.

### Les cinq qui donnent sa couleur au jeu

| Fichier | Ce qu'il doit évoquer | Durée | Fréquence |
|---|---|---|---|
| `activate.wav` | Une capacité qui part. Discret, presque un clic habillé : c'est le son de fond de toute la partie, 14 points d'appel. Un son marquant ici devient vite insupportable. | 80 à 150 ms | à chaque capacité, des dizaines par partie |
| `phase.wav` | Le gong qui annonce que la main change de camp. Le seul qui perce pendant une question : il a le droit d'être grave et de durer. | 400 à 800 ms | 4 fois par round |
| `damage.wav` | L'impact. Sec, physique, sans queue de réverbération. | 100 à 200 ms | très fréquent |
| `set.wav` | Une carte qu'on pose ou qu'on range. Le frottement du carton, rien de plus. Très présent en mise en place, 14 points d'appel. | 80 à 150 ms | très fréquent |
| `target.wav` | La visée, juste avant les dégâts. Doit s'entendre COMME une annonce de ce qui suit, donc plus clair que `damage`, jamais plus fort. | 80 à 150 ms | à chaque attaque |

### Ceux qui gagnent à être marquants, parce qu'ils sont rares

| Fichier | Ce qu'il doit évoquer | Durée | Fréquence |
|---|---|---|---|
| `destroyed.wav` | Une carte détruite. Un moment qu'on doit sentir. | 300 à 500 ms | quelques fois par partie |
| `banished.wav` | Bannie, retirée de la partie, un complot vaincu. Plus définitif encore que `destroyed`. | 300 à 600 ms | rare |
| `flip.wav` | Une carte se retourne : héros ↔ alter ego, changement de face du méchant. Le claquement du carton qui bascule. | 150 à 300 ms | quelques fois par partie |
| `nextturn.wav` | Le jeton de premier joueur qui bouge. Une respiration, pas une alarme. | 300 à 600 ms | une fois par round |

### Le quotidien

| Fichier | Ce qu'il doit évoquer | Durée | Fréquence |
|---|---|---|---|
| `draw.wav` | Une ou plusieurs cartes piochées. Le glissement du papier. | 100 à 200 ms | fréquent |
| `carddrop.wav` | Une carte jouée depuis la main, posée sur la table. | 100 à 200 ms | fréquent |
| `equip.wav` | Une amélioration qui s'installe sur un personnage. Un cran, un clic mécanique. | 150 à 250 ms | moyen |
| `shuffle.wav` | Un deck mélangé. Le seul qui peut durer un peu, il décrit un geste long. | 400 à 800 ms | rare |
| `gainlp.wav` | Des points de vie regagnés. Montant, chaleureux, à l'opposé de `damage`. | 200 à 400 ms | moyen |
| `token.wav` | Un jeton posé sur une carte (menace, dégâts, ressource). Léger, mat. | 60 à 120 ms | très fréquent |
| `addcounter.wav` | Un compteur qui monte. Court, montant. | 60 à 120 ms | fréquent |
| `removecounter.wav` | Un compteur qui descend. Le même, descendant : les deux doivent s'entendre comme une paire. | 60 à 120 ms | fréquent |
| `reveal.wav` | Une carte face cachée retournée face visible. Une découverte. | 200 à 400 ms | fréquent |
| `negate.wav` | Un effet annulé, contré. Doit se lire comme un refus : descendant, mat. | 150 à 300 ms | moyen |

### Les deux qu'on peut ignorer

`directattack.wav` et `cardpick.wav` : déclarés dans le moteur, **jamais
déclenchés** dans cette version. Quoi qu'on y mette, personne ne les entendra.

### Et la musique, à part

`musique-plateau.mp3` n'est pas un effet : c'est le fond sonore du plateau, avec
son propre réglage, et il ne fait pas partie de cette liste.

## Ce qui reste à établir avant d'écrire du code

⚠ **Quels déclencheurs tombent au mauvais moment ?** L'utilisateur dit que
certains arrivent mal, mais lesquels n'est pas su. À lui faire nommer en jouant,
ou à relever en écoutant une partie du début à la fin. **Ne rien déplacer avant
de savoir quoi.**

⚠ **Le mélange** : faut-il un curseur de volume, une limite au nombre de sons
simultanés, ou les deux ? Le volume est aujourd'hui figé à 20 % sans réglage.

## Statut

**Cadré le 15/09/2026.** La liste de courses est prête. Rien ne commence côté
fichiers tant que l'utilisateur ne les a pas ; le volume, les simultanés et les
déclencheurs peuvent partir avant, dès qu'on saura lesquels le gênent.
