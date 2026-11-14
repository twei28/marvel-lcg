# Temporary

**Texte imprimé / définition** : « Temporary. *(Discard this card at the end
of the round.)* » Une carte avec ce mot-clé est défaussée du jeu à la fin du
round.

**Mécanisme moteur** : clé `desc.Temporary` sur la carte, lue nativement par
le moteur. `HasTemporary` (`src/game/card/face/attribute/has_temporary.py`)
enregistre l'attribut `Temporary` -> `printed_temporary` et restaure la valeur
à chaque `OnResetKeywords` via `GainTemporary`. La défausse de fin de round
est faite par `ProcessTemporary()`
(`src/game/world/world_action.py`) : `Worlds.FindCardsOnField(by_effect,
is_temporary=True)` puis `Faces.DiscardAll(...)`. Le filtre `is_temporary`
vit dans `CardFinder` (`src/game/card/card_finder/checker.py`). **Aucun
script requis** pour ce mot-clé : c'est une des « bases automatiques » du
guide. ⚠ Ne pas se fier à `ResolvedTemporaryDiscard` dans
`has_temporary.py` : ce chemin-là est commenté, le vrai mécanisme est
`ProcessTemporary`.

**Carte exemple** : `59016` : Lion of Olympus (`desc` contient
`"Temporary": "1"`), lu directement depuis `desc`, aucun script requis pour le
mot-clé. `33005`-`33007` (Cyclops) et `60052` (Daredevil) pareil.

**Pièges connus** :
- La défausse a lieu à la FIN DU ROUND, pas à la fin du tour du joueur.
  `rg008` (* Red Guardian's Shield) imprime en plus un retour en main à la fin
  du TOUR : c'est une capacité distincte, scriptée, qui court-circuite en
  pratique la défausse de fin de round.
- Une carte Temporary attachée à un ennemi part avec la fin du round même si
  l'ennemi survit (cf. `33005` Exploit Weakness).

- **Perdre Temporary** (« loses the temporary keyword ») : capacité CONTINUE
  `GiveKeywordToInPlayWhenApplyThis(<finder>, temporary=-1)` (`33004` Field
  Commander, `64001b` Danny Rand « Your Technique cards lose temporary »). Posée
  sur une face d'identité, elle cesse quand la face se retourne : la carte
  redevient Temporary et `ProcessTemporary` la défausse à la fin du round
  (décision utilisateur du 19/10/2026 pour Iron Fist ; cas `[iron_fist] 64001b`).
  Le `CardFinder` doit porter `card_type` ET `trait` (assert
  `len(card_finder.params) == 2`, environment.py).

**Variantes maison** : `ho012` (« That Had to Hurt », pack `harry_osborn`)
cumule Temporary avec « Hero form only », « Max 1 per enemy » et une Response :
seul le surplus est scripté, jamais le mot-clé.
