# Incite

**Texte imprimé / définition** : « Incite X. » Quand une carte Rencontre avec ce mot-clé est révélée, placez X points de menace sur le complot principal. (X est la valeur indiquée à côté du mot-clé Incite.)

**Mécanisme moteur** : clé `desc.Incite` sur la carte, lue nativement par le moteur. `HasIncite` / `CanIncite` (`src/game/card/face/attribute/can_incite.py`) enregistre l'attribut `Incite` -> `printed_incite`, restaure la valeur à chaque `OnResetKeywords` via `GainIncite`. Quand la carte est révélée, `ResolveIncite()` place le nombre de menaces spécifié sur le complot principal via `Worlds.FindMainScheme()` et `PlaceThreatInternal()`. La classe `Incite(GameRule)` dans `src/game/effect/rule.py` sert de justification. **Aucun script requis** pour ce mot-clé : c'est une des « bases automatiques » du guide.

**Carte exemple** : `04056` : Hydra Regular (`desc` contient `"Incite": "1"`), lu directement depuis `desc`, aucun script requis. Aucun fichier `04056.py` trouvé dans `src/cards/pack` : toutes les capacités imprimées de cette carte sont couvertes par les compteurs `desc` automatiques du moteur, sans script dédié.

**Pièges connus** : Incite place la menace sur le **complot principal** uniquement, jamais sur les complots secondaires. Si le complot principal n'existe pas, l'effet ne s'applique pas. Si une future carte cumule Incite avec une capacité imprimée distincte, vérifier via `find` si un script existe : le script devra porter uniquement cette capacité annexe, jamais le mot-clé Incite lui-même.

**Variantes maison** : aucune recensée pour l'instant.
