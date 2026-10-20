# Jeton recherché (« wanted counter »)

**Texte imprimé / définition** : Punisher MC×DC 2026, p237 *SWAT* (manigance annexe permanente, set modulaire « SWAT
Team », ID 6119, menace de départ 1 fixe) :
« Setup. Permanent. Players cannot thwart this scheme. **Forced Response**: After an enemy is defeated, place 1
threat here (3 threat instead if it had the POLICE trait). Then, if there is 4+ threat here, remove all threat and
place 1 **wanted counter** here. **If there are 5 or more wanted counters here, the players lose the game.** »
Les trois sbires du set (Cole North p239, Riot Police ×2 p241/243, Tactical Sniper ×2 p245/247) renvoient tous à ce
compteur : « When Cole North schemes, place that threat on SWAT, if able » ; deux capacités lisent le nombre de
jetons recherché en cours (« if there are fewer than 3 wanted counters on SWAT ») pour changer de comportement.

**Mécanisme moteur** : **à créer**, mécanique de petite taille. Deux briques déjà connues du dépôt suffisent :
- Un compteur nommé (`wanted`) posé sur la manigance annexe SWAT, lu et comparé comme n'importe quel compteur de
  carte (`all-purpose-counter.md`).
- Une seconde condition de défaite en plus de la menace de la manigance principale à son maximum (« If there are 5
  or more wanted counters here, the players lose the game ») : condition de défaite indépendante, à vérifier après
  chaque pose de jeton, sur le modèle d'une manigance annexe qui fait perdre la partie par un autre chemin que sa
  propre menace (ex. manigances à « Victory 0 »/pile de victoire particulière, voir `victory.md`) — aucune carte du
  dépôt n'a exactement ce « compteur qui remplace la menace comme jauge de défaite », donc pas de modèle 1:1, mais
  le mécanisme (comparer un compteur à un seuil fixe après une pose) est ordinaire.
- La manigance ne peut pas être « thwart » (« Players cannot thwart this scheme ») : flag déjà existant ailleurs
  dans le moteur pour les manigances annexes non-contrables ; à confirmer sur une carte modèle lors du portage.

**Carte exemple** : aucune carte portée à ce jour (lot PU-3 du cadrage, « Syndicate, Hit List, Armory, SWAT, Capo of
the Past », après PU-1 pour les briques communes).

**Pièges connus** :
- Le jeton recherché N'EST PAS de la menace : à 4+ menace sur SWAT, toute la menace est RETIRÉE et remplacée par un
  jeton recherché (pas cumulée dessus). Un script qui ajouterait le jeton sans vider la menace ferait boucler la
  pose à chaque défaite d'ennemi suivante avant d'atteindre 4 à nouveau.
- Le trait POLICE (porté par Cole North, Riot Police et Tactical Sniper eux-mêmes) triple la menace posée quand un
  ennemi qui le porte meurt (3 au lieu de 1) : lire le TRAIT de l'ennemi vaincu, pas son nom.
- SWAT est un set **modulaire** (il peut être ajouté à n'importe quel scénario qui le prévoit, cité par le combat 4
  Kingsfall p269 et par certains combats — vérifier au portage), pas une carte liée au seul scénario 1.

**Variantes maison** : aucune à ce jour ; brique neuve du lot Punisher MC×DC 2026 (cadrage §1.2, texte « SWAT Team
(6, "jetons recherché" = nouvelle condition de défaite, petite) »).
