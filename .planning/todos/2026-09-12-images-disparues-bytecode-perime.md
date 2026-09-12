# « Pourquoi j'ai plus les images ? » : le moteur d'une table tournait sur du bytecode périmé

**Signalé le 12/09/2026** (capture : l'assistant en prod, tuiles de héros et
scène sans image).

## Ce qui s'est passé

1. `launcher_fast.py` compile `src/` vers `.game/*.pyc` de façon
   incrémentale : une source n'est recompilée que si elle est **plus récente**
   que son `.pyc`.
2. `deploiement/deployer.ps1` extrayait le code avec `tar -xzf`, qui
   **conserve la date d'origine** des fichiers. `asset.py` modifié le 11/09
   à 15:08 (ajout de `villainous=` pour Hellcat) est arrivé sur le serveur
   après un `.pyc` compilé à 15:10 depuis l'ancienne version : jamais
   recompilé.
3. Ta table a lancé une partie Hellcat : `hc010.py` appelle
   `GiveKeywordToAttached(..., villainous=1)`, le vieux bytecode ne connaît
   pas l'argument, la mise en place plante (`.game/crash.log` 10:31).
4. Le plantage arrête l'exécuteur de tâches du moteur
   (`cannot schedule new futures after shutdown`, 492 fois dans
   `moteur-1.log`) : toute requête passant par `TaskManager.ToThread`, dont
   **les images**, échoue. L'assistant se charge (HTML servi autrement), les
   images non.

## Ce qui a été fait

- Serveur : `touch` de toutes les sources, recompilation complète
  (6 667 fichiers), moteur périmé de la table arrêté. Au prochain « Entrer »
  la table repart sur le bon code.
- `deployer.ps1` : extraction avec `tar -xzmf` (`-m`) : les sources prennent
  la date de l'extraction, donc toujours plus récentes que les `.pyc` ; la
  première table lancée après un déploiement recompile tout (5 s).

## Ce qui reste, à décider

Un plantage de mise en place ne devrait pas tuer la table entière (images,
pages) : le moteur devrait rester servable, ou la table s'éteindre
franchement pour que le site la relance. À cadrer, sans demande pour
l'instant.
