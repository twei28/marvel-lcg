# Acceleration

**Texte imprimé / définition** : « Acceleration. » Pour chaque schéma annexe en jeu avec ce mot-clé, un threat supplémentaire est placé sur le schéma principal pendant l'étape 1 de la phase vilain (avant les pioches standard). Le compteur `Acceleration` (`1`, `2`, ...) fixe le nombre d'icônes Acceleration portées par la carte.

**Mécanisme moteur** : clé `desc.Acceleration` sur la carte, lue nativement par le moteur. `HasAccelerationIcon` (`src/game/card/face/attribute/has_acceleration_icon.py`) enregistre l'attribut `Acceleration` -> `printed_acceleration_icon`, restaure la valeur à chaque `OnResetKeywords` via `GainAccelerationIcon`. Durant l'étape 1 de la phase vilain, le moteur compte les icônes Acceleration en jeu et place autant de threat sur le schéma principal. **Aucun script requis** pour ce mot-clé : c'est une des « bases automatiques » du guide.

**Carte exemple** : `01109` : Bomb Scare (`desc` contient `"Acceleration": "1"`), lu directement depuis `desc`, aucun script requis. Un fichier `01109.py` existe dans `src/cards/pack` : ce script gère une capacité imprimée annexe (placement de threat à la révélation), pas le mot-clé Acceleration.

**Pièges connus** : Acceleration s'ajoute au threat du schéma principal à l'étape 1 (avant les pioches) ; ne pas confondre avec Hazard qui agit à l'étape 3 et déale des cartes supplémentaires. Les cartes Acceleration peuvent cumuler plusieurs icônes (compteur > 1), chaque icône plaçant un threat supplémentaire. Si une future carte cumule Acceleration avec une capacité imprimée distincte, vérifier via `find` si un script existe : le script devra porter uniquement cette capacité annexe, jamais le mot-clé Acceleration lui-même.

**Variantes maison** : aucune recensée pour l'instant.
