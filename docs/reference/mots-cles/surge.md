# Surge

**Texte imprimé / définition** : « Surge. » Quand une carte Rencontre avec ce mot-clé est révélée, une carte Rencontre supplémentaire est piochée immédiatement. Le compteur `Surge` (`1`, `2`, ...) fixe le nombre de pioches supplémentaires déclenchées.

**Mécanisme moteur** : clé `desc.Surge` sur la carte, lue nativement par le moteur. `HasSurge` et `CanSurge` (`src/game/card/face/attribute/can_surge.py`) enregistrent l'attribut `Surge` -> `printed_surge`, restaurent la valeur à chaque `OnResetKeywords` via `GainSurge`. Quand Surge se déclenche, `ResolveSurge()` déale une ou plusieurs cartes Rencontre via `player.DealEncounterCards()`. La classe `Surge(GameRule)` dans `src/game/effect/rule.py` sert de justification. **Aucun script requis** pour ce mot-clé : c'est une des « bases automatiques » du guide.

**Carte exemple** : `01121` : Weapons Runner (`desc` contient `"Surge": "1"`), lu directement depuis `desc`, aucun script requis. Un fichier `01121.py` existe dans `src/cards/pack` : ce script gère une capacité imprimée annexe (entrée en jeu comme boost), pas le mot-clé Surge.

**Pièges connus** : Surge s'ajoute à la pioche standard des cartes Rencontre, il n'est pas une variante de celle-ci ; il faut compter la perte de contrôle engendrée par la pioche supplémentaire. Si une future carte cumule Surge avec une capacité imprimée distincte, vérifier via `find` si un script existe : le script devra porter uniquement cette capacité annexe, jamais le mot-clé Surge lui-même.

**Variantes maison** : aucune recensée pour l'instant.
