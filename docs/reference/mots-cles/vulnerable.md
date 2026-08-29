# Vulnerable

**Texte imprimé / définition** : « Vulnerable. » Un personnage avec ce mot-clé est défaussé s'il est ou devient étourdi ou confus. Le compteur `Vulnerable` (`1`, `2`, ...) fixe le nombre de chargés Vulnerable disponibles.

**Mécanisme moteur** : clé `desc.Vulnerable` sur la carte, lue nativement par le moteur. `HasVulnerable` (`src/game/card/face/attribute/has_vulnerable.py`) enregistre l'attribut `Vulnerable` -> `printed_vulnerable`, restaure la valeur à chaque `OnResetKeywords` via `GainVulnerable`. Quand le personnage reçoit un statut Stun ou Confuse, le moteur vérifie `IsVulnerable()` et le défausse si le mot-clé est actif. La classe `Vulnerable(GameRule)` dans `src/game/effect/rule.py` sert de justification. **Aucun script requis** pour ce mot-clé : c'est une des « bases automatiques » du guide.

**Carte exemple** : `50083` : A.I.M. Scientist (`desc` contient `"Vulnerable": "1"`), lu directement depuis `desc`, aucun script requis. Aucun fichier `50083.py` trouvé dans `src/cards/pack` : toutes les capacités imprimées de cette carte sont couvertes par les compteurs `desc` automatiques du moteur, sans script dédié.

**Pièges connus** : Vulnerable ne s'applique qu'au statuts Stun et Confuse, jamais aux autres formes de dégâts ou d'effets. Un personnage Vulnerable n'est pas défaussé par une simple menace ou un dégât normal, seulement s'il est ou devient Stun/Confus. Si une future carte cumule Vulnerable avec une capacité imprimée distincte, vérifier via `find` si un script existe : le script devra porter uniquement cette capacité annexe, jamais le mot-clé Vulnerable lui-même.

**Variantes maison** : aucune recensée pour l'instant.
