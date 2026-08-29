# Crisis

**Texte imprimé / définition** : « Crisis. » Un schéma annexe avec ce mot-clé force une réponse immédiate du joueur : il doit être vaincu avant que le threat puisse être retiré du schéma principal. Le compteur `Crisis` (`1`, `2`, ...) fixe le nombre de charges de crise.

**Mécanisme moteur** : clé `desc.Crisis` sur la carte, lue nativement par le moteur. `CanCrisis` (`src/game/card/face/attribute/has_crisis.py`) enregistre l'attribut `Crisis` -> `printed_crisis`, restaure la valeur à chaque `OnResetKeywords` via `GainCrisis`. Quand un schéma Crisis entre en jeu, `SetCrisisEffectedBy()` marque le complot principal comme affecté (`scheme.card.ui.SetEffectedBy(diff, GameRule(self))`). Le blocage réel se joue dans `CardFace.RemoveThreatFromSchemes` (`src/game/card/face/card_face.py`) : sa signature porte un paramètre `ignore_crisis` que le moteur enregistre via une règle temporaire (`AbilityFactory.UnitIgnoreKeywordIcons(..., crisis=True)`) quand une carte veut explicitement passer outre. C'est donc un vrai contrôle côté moteur, intégré à la fonction de retrait de menace elle-même, pas une simple restriction d'affichage. **Aucun script requis** pour ce mot-clé lui-même : c'est une des « bases automatiques » du guide.

**Carte exemple** : `01108` : Crowd Control (`desc` contient `"Crisis": "1"`), lu directement depuis `desc`, aucun script requis. Aucun fichier `01108.py` trouvé dans `src/cards/pack` : cette carte ne porte que le mot-clé Crisis, sans capacité imprimée annexe.

**Pièges connus** : Crisis bloque le retrait de menace sur le complot principal au niveau de `RemoveThreatFromSchemes` lui-même, pas via une règle de perte de PV. Une carte qui veut explicitement l'ignorer doit passer `ignore_crisis=True` à cet appel. Ne pas confondre avec Peril, qui agit de manière similaire mais sur un autre déclencheur. Si une future carte cumule Crisis avec une capacité imprimée distincte, vérifier via `find` si un script existe : le script devra porter uniquement cette capacité annexe, jamais le mot-clé Crisis lui-même.

**Variantes maison** : aucune recensée pour l'instant.
