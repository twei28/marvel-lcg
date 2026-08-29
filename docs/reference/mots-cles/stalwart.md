# Stalwart

**Texte imprimé / définition** : « Stalwart. » Un personnage avec ce mot-clé ne peut pas être étourdi ni confus. Le compteur `Stalwart` (`1`, `2`, ...) fixe le nombre de chargés Stalwart disponibles.

**Mécanisme moteur** : clé `desc.Stalwart` sur la carte, lue nativement par le moteur. `HasStalwart` (`src/game/card/face/attribute/has_stalwart.py`) enregistre l'attribut `Stalwart` -> `printed_stalwart`, restaure la valeur à chaque `OnResetKeywords` via `GainStalwart` et discard tout compteur Stun ou Confuse existant quand le mot-clé est gagné. La classe `Stalwart(GameRule)` dans `src/game/effect/rule.py` sert de justification. **Aucun script requis** pour ce mot-clé : c'est une des « bases automatiques » du guide.

**Carte exemple** : `16133` : Kree Lieutenant (`desc` contient `"Stalwart": "1"`), lu directement depuis `desc`, aucun script requis. Aucun fichier `16133.py` trouvé dans `src/cards/pack` : toutes les capacités imprimées de cette carte sont couvertes par les compteurs `desc` automatiques du moteur, sans script dédié.

**Pièges connus** : ne pas confondre avec d'autres mot-clés de protection (Guard, Retaliate, Toughness). Si une future carte cumule Stalwart avec une capacité imprimée distincte, vérifier via `find` si un script existe : le script devra porter uniquement cette capacité annexe, jamais le mot-clé Stalwart lui-même.

**Variantes maison** : aucune recensée pour l'instant.
