# Territoire (« turf »), zones de jeu cloisonnées par rangée

**Texte imprimé / définition** :
- Punisher MC×DC 2026, p011 *Never Sleeps* (environnement, Setup/Permanent, forme avec *The City* p009 le nom
  complet « The City Never Sleeps ») : « Each row of locations is the "turf" of the villain in that row. Villains
  only activate against players in their turf. Players can only interact with villains or other players (including
  their play areas) if they are in the same turf. Players can interact with all schemes. »
- p006 *Gunrunner's Warehouse (3B)* : « The villain with Gunrunner attached is the active villain and each player
  **is considered to be in their turf** » — au stade 3B, les territoires s'effacent, tout le monde est réputé dans
  le même territoire que le méchant actif.
- `regles-fr.md` lignes 22-26 (règle imprimée + confirmation utilisateur) : chaque ligne de la grille = territoire
  d'un CAPO ; pas d'interaction ENTRE territoires (joueurs, sbires, aires de jeu) ; les méchants ne s'activent que
  contre les joueurs de leur propre territoire ; manigances (principale et annexes) et icônes Accélération / Aléas /
  Amplification / Crise sont **communes à toute la partie**, pas cloisonnées par territoire (seuls joueurs, sbires et
  méchants le sont).
- `regles-fr.md` ligne 57 : les capacités de carte rencontre (ex. Teamwork) qui vérifient des sbires « en jeu » ne
  sont PAS limitées à un territoire ; seule l'interaction joueur↔joueur, joueur↔sbire et joueur↔méchant l'est.

**Mécanisme moteur** : brique partiellement existante, **à compléter** (cadrage §1.2, M2, « la brique la plus
risquée »). Base déjà dans le dépôt :
- `World.CreateGameArea()` (`src/game/world/world.py:184`) et `GameArea.AddPlayer()` /
  `GameArea.AddCard()` (`src/game/world/game_area/game_area.py:11,44`) : une zone de jeu par groupe de joueurs,
  utilisées par Kang (`src/cards/pack/toafk/kang/__init__.py`, `KangMainSchemStage3Reveal`, une zone par joueur, un
  Kang par zone) et par le mode compétitif Civil War (`GetTeamGameArea`, `src/game/world/world.py:206`, appelé
  depuis `src/game/world/competitive.py:211`). `Worlds.GetVillains(game_area)` filtre déjà par zone.
- Ce que Kang NE fait PAS et que Punisher demande en plus : (1) manigances (principale et annexes) et deck de
  rencontre **partagés** entre les trois (ou quatre) zones, alors que Kang/Civil War leur en donnent un jeu par
  zone ; (2) un joueur qui **change de territoire en cours de partie** (déplacement libre entre lieux de rangées
  différentes via l'action de *The City*), alors que Kang fixe la zone une fois pour toutes à la mise en place.

**Carte exemple** : aucune carte portée à ce jour. Pas de modèle direct pour les deux points manquants ci-dessus ;
spec à écrire et faire relire par un agent fort avant de coder (cadrage §1.5).

**Pièges connus** :
- Un territoire n'est PAS une partie séparée : la pile de victoire, le deck LEADS, les icônes de crise/accélération
  etc. restent uniques pour toute la table (voir ci-dessus). Seules la liste des sbires engagés, les méchants actifs
  et l'interaction entre joueurs sont cloisonnées.
- Le stade 3B (*Gunrunner's Warehouse*) ANNULE le cloisonnement : tous les joueurs rejoignent le territoire du
  méchant actif (celui qui porte Gunrunner). Un script qui lirait « le territoire du joueur » doit donc passer par
  un point unique (prévu : un crochet comparable à `GettingVillain` de `mechants-multiples.md`), pas relire la
  position en dur.
- Les capacités de lieu limitées « une fois par round au total » (`lieu.md`) sont au total pour TOUTE la table, pas
  par territoire : un joueur d'un autre territoire qui visite le même numéro de lieu (improbable vu le cloisonnement
  des rangées, mais l'Extension Uptown ajoute une 4e rangée) consomme la même limite.
- Pas de confusion avec le **changement de territoire** de Kang : celui-ci est définitif et posé une seule fois (à
  la révélation du stade 3) ; Punisher, lui, doit le permettre à répétition via le déplacement normal du joueur.

**Variantes maison** : aucune à ce jour ; brique neuve du lot Punisher MC×DC 2026 (cadrage §1.2, mécanique M2), à
écrire en même temps que `lieu.md` (M1) dont elle dépend (déplacement = changement de lieu = parfois changement de
territoire).
