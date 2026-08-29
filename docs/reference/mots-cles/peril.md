# Peril

**Texte imprimé / définition** : « Peril. » Pendant qu'un joueur résout une carte Rencontre avec ce mot-clé, ce joueur ne peut consulter aucun autre joueur, et les autres joueurs ne peuvent jouer aucune carte ni déclencher d'abilité. Le compteur `Peril` (`1`, `2`, ...) fixe le nombre de charges Peril disponibles.

**Mécanisme moteur** : clé `desc.Peril` sur la carte, lue nativement par le moteur. `HasPeril` (`src/game/card/face/attribute/has_peril.py`) enregistre l'attribut `Peril` -> `printed_peril`, restaure la valeur à chaque `OnResetKeywords` via `GainPeril`. L'isolement du joueur et l'interdiction pour les autres de jouer sont appliqués par le moteur lors de la résolution de la carte. La classe `Peril(GameRule)` dans `src/game/effect/rule.py` sert de justification. **Aucun script requis** pour ce mot-clé : c'est une des « bases automatiques » du guide.

**Carte exemple** : `16145` : Blind Side (`desc` contient `"Peril": "1"`), lu directement depuis `desc`, aucun script requis. Le script `16145.py` existe et code la capacité de révélation (« When revealed, choose one: exhaust the Milano or pay RR. If you don't, stun the first player »), pas le mot-clé lui-même : le moteur lit `Peril` nativement dans `desc`, aucun module n'est nécessaire pour lui.

**Pièges connus** : Peril isole complètement le joueur qui résout la carte, y compris de la consultation tactique (le joueur ne peut pas demander l'avis des autres). Si une future carte cumule Peril avec une capacité imprimée distincte, vérifier via `find` si un script existe : le script devra porter uniquement cette capacité annexe, jamais le mot-clé Peril lui-même.

**Variantes maison** : aucune recensée pour l'instant.
