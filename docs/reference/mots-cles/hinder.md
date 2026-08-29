# Hinder

**Texte imprimé / définition** : « Hinder X. » Quand une carte Rencontre avec ce mot-clé entre en jeu, placez X points de menace sur cette carte. (X est la valeur indiquée à côté du mot-clé Hinder.)

**Mécanisme moteur** : clé `desc.Hinder` sur la carte, lue nativement par le moteur. `HasHinder` / `CanHinder` (`src/game/card/face/attribute/can_hinder.py`) enregistre l'attribut `Hinder` -> `printed_hinder`, restaure la valeur à chaque `OnResetKeywords` via `GainHinder`. Quand la carte entre en jeu (`OnWouldEnterPlay`) ou après un retournement (`OnAfterFlip`), `ResolveHinder()` place le nombre de menaces spécifié sur la carte elle-même via `PlaceTokensInternal()`. La classe `ResetKeyword(...)` dans `src/game/effect/rule.py` sert de justification. **Aucun script requis** pour ce mot-clé : c'est une des « bases automatiques » du guide.

**Carte exemple** : `16066` : Blockade (`desc` contient `"Hinder": "2*"`), lu directement depuis `desc`, aucun script requis. Le script `16066.py` existe et code une capacité annexe d'exhaustion pour retirer de la menace (« Exhaust the Milano to remove 3 threat from the main scheme »), pas le mot-clé lui-même : le moteur lit `Hinder` nativement dans `desc`, aucun module n'est nécessaire pour lui.

**Pièges connus** : Hinder place la menace **sur la carte elle-même**, jamais sur le complot principal ou les autres cartes. Le `2*` en `desc` indique une menace **par joueur**. Si une future carte cumule Hinder avec une capacité imprimée distincte, vérifier via `find` si un script existe : le script devra porter uniquement cette capacité annexe, jamais le mot-clé Hinder lui-même.

**Variantes maison** : aucune recensée pour l'instant.
