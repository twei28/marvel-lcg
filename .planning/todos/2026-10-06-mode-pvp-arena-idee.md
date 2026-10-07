# Mode PvP « Arena / Confrontation » : idée en backlog (06/10/2026)

**Statut : BACKLOG, très lointain. Rien n'est à développer, aucune urgence.**

## L'idée
Deux héros s'affrontent avec leurs decks normaux, sans vilain. Deux victoires : KO du héros
adverse, ou domination (10 points en contrôlant 3 objectifs au centre).
- THW devient une capture d'objectif (menace → contrôle, chaque objectif a un effet).
- ATK vise le héros adverse ou ses alliés, défense normale, pas de carte boost.
- Alter-Ego : intouchable, mais l'adversaire gagne du terrain (THW +1 ou contrôle gratuit).
- Notion de « Rival » dans le moteur (le héros adverse tient le rôle du vilain).
- Cartes classées NORMAL / ADAPTED / BANNED, lancement sur decks standards.
- Options reportées : ressource Momentum, cartes Battlefield communes.

## Ce que la simulation jouet a montré
Scripts : `.planning/todos/pvp-simulation/pvp_sim.py` (4 archétypes) et `pvp_sim2.py` (vraies stats
des 5 héros du set de base, tirées de `data/cards.json`, bonus de cartes par aspect INVENTÉS).
- Solide : héros équilibrés entre eux (42 à 56 %), premier joueur ~51 %, 9 à 12 rounds, domination
  à ~75 % des fins. Seuil de capture, nombre d'objectifs et points requis règlent la durée, pas
  l'équilibre.
- Règle vérifiée : la DEF réduit les dégâts de sa valeur (Rules Reference p.15), valeur imprimée fixe.
- Artefact probable : Aggression ~12 %, Leadership ~81 %. Vient des bonus inventés. Tendance de
  fond : sous DEF soustractive, attaquer (2 à 4 net) perd la course contre la capture.

## Si on reprend un jour
1. Calculer les vrais bonus ATK/THW/DEF par aspect depuis les cartes du dépôt, relancer pvp_sim2.
2. Seulement si l'équilibre tient : spécifier la notion de Rival (le héros adverse doit être une
   cible valide pour tout ce qui vise un « ennemi » : dégâts, statuts, défense par ses alliés).
3. Trancher le moment du ready du défenseur.
