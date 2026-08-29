# Steady

**Texte imprimé / définition** : « Steady. » Un personnage avec ce mot-clé peut avoir jusqu'à deux compteurs Stun supplémentaires et deux compteurs Confuse supplémentaires. Ce personnage n'est étourdi que s'il a déjà deux compteurs Stun (au lieu de un), et n'est confus que s'il a déjà deux compteurs Confuse (au lieu de un). Quand l'effet d'un statut de ce type résout (en remplacement de l'activation), tous les compteurs du type en question sont retirés.

**Mécanisme moteur** : clé `desc.Steady` sur la carte, lue nativement par le moteur. `HasSteady` (`src/game/card/face/attribute/has_steady.py`) enregistre l'attribut `Steady` -> `printed_steady`, stocke le compteur `Steady` via la clé `desc`, et restaure sa valeur à chaque `OnResetKeywords` via `GainSteady`. La classe `Steady(GameRule)` dans `src/game/effect/rule.py` sert de justification (raison) à l'attribution du compteur. **Aucun script requis** pour ce mot-clé : c'est une des « bases automatiques » du guide, à ne pas recoder inutilement dans le `.py` de la carte.

**Carte exemple** : `27074` : * Venom (`desc` contient `"Steady": "1"`), lu directement depuis `desc`, aucun script requis. Un fichier `27074.py` existe dans `src/cards/pack` : ce script gère des capacités imprimées annexes, pas le mot-clé Steady.

**Pièges connus** : Steady ne s'applique que aux statuts Stun et Confuse ; ne pas confondre avec les autres mot-clés de protection. Si une future carte cumule Steady avec une capacité imprimée distincte, vérifier via `find` si un script existe pour cette carte : le script devra porter uniquement cette capacité annexe, jamais le mot-clé Steady lui-même.

**Variantes maison** : aucune recensée pour l'instant.
