# Surge

**Texte imprimé / définition** : « Surge. » Quand une carte Rencontre avec ce mot-clé est révélée, une carte Rencontre supplémentaire est piochée immédiatement. Le compteur `Surge` (`1`, `2`, ...) fixe le nombre de pioches supplémentaires déclenchées.

**Mécanisme moteur** : clé `desc.Surge` sur la carte, lue nativement par le moteur. `HasSurge` et `CanSurge` (`src/game/card/face/attribute/can_surge.py`) enregistrent l'attribut `Surge` -> `printed_surge`, restaurent la valeur à chaque `OnResetKeywords` via `GainSurge`. Quand Surge se déclenche, `ResolveSurge()` déale une ou plusieurs cartes Rencontre via `player.DealEncounterCards()`. La classe `Surge(GameRule)` dans `src/game/effect/rule.py` sert de justification. **Aucun script requis** pour ce mot-clé : c'est une des « bases automatiques » du guide.

**Carte exemple** : `01121` : Weapons Runner (`desc` contient `"Surge": "1"`), lu directement depuis `desc`, aucun script requis. Un fichier `01121.py` existe dans `src/cards/pack` : ce script gère une capacité imprimée annexe (entrée en jeu comme boost), pas le mot-clé Surge.

**Pièges connus** : Surge s'ajoute à la pioche standard des cartes Rencontre, il n'est pas une variante de celle-ci ; il faut compter la perte de contrôle engendrée par la pioche supplémentaire. Si une future carte cumule Surge avec une capacité imprimée distincte, vérifier via `find` si un script existe : le script devra porter uniquement cette capacité annexe, jamais le mot-clé Surge lui-même.

**Variantes maison** : aucune recensée pour l'instant.


**Rules Reference 1.8 (22/07/2026)** : Surge ne RÉVÈLE plus, il DISTRIBUE : « When an encounter card with this keyword is revealed, the player resolving the card deals themself a facedown encounter card » (équivaut à « When Revealed : Deal yourself 1 facedown encounter card »). Hors phase du méchant, la carte reste face cachée jusqu'à l'étape 4 de la phase suivante ; pendant l'étape 4, la boucle `RevealEncounterCards` la révèle dans la foulée. Moteur : règle `v18_surge` (posée par `v18_all`, que le lanceur pousse pour toute partie neuve) ; sans elle, `fix_surge` garde l'ancien comportement (révélation immédiate) pour rejouer les sauvegardes d'avant. Cas : `[RR1.8] 01191 Exhaustion` dans `tools/test_capacites.py`.

## Pièges vus au portage de Raza Longknife (26/10/2026)

- **« If no attachment was revealed this way, this card gains surge »** (`rl015` Shi'ar Host) : `ThisCardGainSurge(effect, message)` (helper de `cards/pack/__init__.py`). Mesure : un deck rencontre d'UNE seule carte et la clé d'attendu `carte_du_surge` (la carte ne doit plus être dans le deck), plus fiable qu'un `en_jeu` dont le résultat dépend de l'ordre du deck.
