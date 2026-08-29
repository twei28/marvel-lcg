# Patrol

**Texte imprimé / définition** : « Patrol. » Un sbire avec ce mot-clé peut être engagé avec n'importe quel joueur (pas seulement celui dont c'est le tour). Patrol fonctionne souvent avec Guard pour augmenter les voies de défense disponibles. Le compteur `Patrol` (`1`, `2`, ...) fixe le nombre de chargés Patrol disponibles.

**Mécanisme moteur** : clé `desc.Patrol` sur la carte (réservée aux Minions), lue nativement par le moteur. `HasPatrol` (`src/game/card/face/attribute/has_patrol.py`) enregistre l'attribut `Patrol` -> `printed_patrol`, restaure la valeur à chaque `OnResetKeywords` via `GainPatrol`. Quand le mot-clé est gagné, la méthode `SetGuardPatrolEffectedBy()` marque le sbire comme pouvant être engagé par n'importe quel joueur. La classe `Patrol(GameRule)` dans `src/game/effect/rule.py` sert de justification. **Aucun script requis** pour ce mot-clé : c'est une des « bases automatiques » du guide.

**Carte exemple** : `16119` : Badoon Lieutenant (`desc` contient `"Patrol": "1"`), lu directement depuis `desc`, aucun script requis. Aucun fichier `16119.py` trouvé dans `src/cards/pack` : toutes les capacités imprimées de cette carte sont couvertes par les compteurs `desc` automatiques du moteur, sans script dédié.

**Pièges connus** : Patrol ne s'applique qu'aux Minions/sbires, jamais aux autres types de cartes. Patrol n'augmente pas directement la limite d'engagement d'un joueur, il permet simplement au sbire d'être choisi par n'importe quel joueur lors de l'engagement. Si une future carte cumule Patrol avec une capacité imprimée distincte, vérifier via `find` si un script existe : le script devra porter uniquement cette capacité annexe, jamais le mot-clé Patrol lui-même.

**Variantes maison** : aucune recensée pour l'instant.
