# Toughness

**Texte imprimé / définition** : « Toughness. *(This character enters play with
a tough status card.)* » Un personnage avec ce mot-clé entre en jeu avec une
carte de statut « Tough ». C'est tout : le mot-clé ne dit rien de plus, ni
limite par round, ni clause sur la menace. Le compteur `Toughness` (`1`, `2`,
...) est réinitialisé à sa valeur imprimée à chaque reset des mots-clés.

**Mécanisme moteur** : clé `desc.Toughness` sur la carte, lue nativement
par le moteur. `HasToughness`
(`src/game/card/face/attribute/has_toughness.py`) enregistre l'attribut
`Toughness` -> `printed_toughness`, pose le statut « Tough » à l'entrée en
jeu (`OnWhenCardEnterPlay`, via `Faces.GiveStatus([self], "Tough",
Toughness(self))`) et restaure la valeur imprimée à chaque `OnResetKeywords`
via `GainToughness`. La classe `Toughness(GameRule)` de
`src/game/effect/rule.py` sert de justification (raison) à l'attribution du
statut.

Ce que fait ensuite la carte de statut relève d'elle, pas du mot-clé : le
statut est géré par `CanStatus`
(`src/game/card/face/attribute/can_status.py`, `tough`/`tough_max`/`IsTough`/
`DiscardTough`), et sa capacité vit dans `src/cards/pack/status/tough.py`. Elle
écoute `WhenUnitWouldTakeDamage` sur `"AttachedCharacter"` : elle appelle
`message.SetBeInstead(effect)` (les dégâts n'ont pas lieu) puis
`unit.DiscardTough(effect, rule=1)` (une carte Tough est défaussée), sauf si la
source porte `property.ignore_tough`. **Aucun script requis** pour ce mot-clé :
c'est une des « bases automatiques » du guide, à ne pas recoder inutilement
dans le `.py` de la carte.

**Carte exemple** : `01076` : * Luke Cage (`desc` contient `"Toughness":
"1"`), lu directement depuis `desc`, aucun script requis. Aucun fichier
`01076.py` trouvé dans `src/cards/pack` : cette carte n'a pas de capacité
imprimée distincte nécessitant un script.

**Pièges connus** :
- Le mot-clé ne fait qu'UNE chose : donner une carte de statut Tough à l'entrée
  en jeu. Toute la mécanique d'absorption appartient au statut, et se déclenche
  sur n'importe quels dégâts (`WhenUnitWouldTakeDamage`), qu'ils viennent d'une
  attaque ou d'une capacité de carte. Il n'y a **ni limite « une fois par
  round », ni clause sur la menace**.
- Une source peut ignorer le statut via `property.ignore_tough` (les dégâts
  perforants passent aussi outre : `can_attack.py` défausse alors tous les Tough
  via `DiscardTough(..., rule="All")` quand `IsPiercing()`).
- Distinguer le mot-clé `desc.Toughness` (état de départ) du statut Tough
  lui-même, qu'une autre carte peut donner ou retirer en cours de partie :
  `GainStatus` refuse d'en ajouter au-delà de `tough_max`.
- Ne pas confondre avec Guard, Retaliate ou Patrol, qui portent sur le ciblage
  ou sur le combat.
- Si une future carte cumule Toughness avec une capacité imprimée distincte,
  vérifier via `find` si un script existe pour cette carte : le script devra
  porter uniquement cette capacité annexe, jamais le mot-clé Toughness
  lui-même.

**Variantes maison** : aucune recensée pour l'instant.
