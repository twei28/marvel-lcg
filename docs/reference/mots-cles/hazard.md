# Hazard

**Texte imprimé / définition** : « Hazard. » Pour chaque schéma annexe en jeu avec ce mot-clé, une carte Rencontre supplémentaire est déalée pendant l'étape 3 de la phase vilain (après la pioche standard). Les cartes supplémentaires sont déalées dans l'ordre des joueurs. Le compteur `Hazard` (`1`, `2`, ...) fixe le nombre d'icônes Hazard portées par la carte.

**Mécanisme moteur** : clé `desc.Hazard` sur la carte, lue nativement par le moteur. `HasHazard` (`src/game/card/face/attribute/has_hazard.py`) enregistre l'attribut `Hazard` -> `printed_hazard`, restaure la valeur à chaque `OnResetKeywords` via `GainHazard`. Durant l'étape 3 de la phase vilain, le moteur compte les icônes Hazard en jeu et déale autant de cartes Rencontre supplémentaires. **Aucun script requis** pour ce mot-clé : c'est une des « bases automatiques » du guide.

**Carte exemple** : `01107` : Breakin' & Takin' (`desc` contient `"Hazard": "1"`), lu directement depuis `desc`, aucun script requis. Un fichier `01107.py` existe dans `src/cards/pack` : ce script gère une capacité imprimée annexe (placement de threat à la révélation), pas le mot-clé Hazard.

**Pièges connus** : Hazard s'ajoute aux pioches standards lors de l'étape 3 de la phase vilain ; ne pas confondre avec Acceleration qui agit à l'étape 1. Les cartes Hazard peuvent cumuler plusieurs icônes Hazard (compteur > 1), chaque icône déclenchant une pioche supplémentaire. Si une future carte cumule Hazard avec une capacité imprimée distincte, vérifier via `find` si un script existe : le script devra porter uniquement cette capacité annexe, jamais le mot-clé Hazard lui-même.

**Variantes maison** : aucune recensée pour l'instant.
