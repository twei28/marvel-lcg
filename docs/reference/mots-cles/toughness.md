# Toughness

**Texte imprimé / définition** : « Toughness. » Un personnage avec ce
mot-clé entre en jeu avec le statut « Tough ». La première fois dans le
tour qu'une capacité de carte (pas l'icône ATK/THW/DEF standard) devrait
lui infliger des dégâts ou lui placer du threat, cet effet est annulé et
le statut Tough est retiré à la place. Le compteur `Toughness` (`1`, `2`,
...) fixe le nombre de charges Tough disponibles.

**Mécanisme moteur** : clé `desc.Toughness` sur la carte, lue nativement
par le moteur. `HasToughness`
(`src/game/card/face/attribute/has_toughness.py`) enregistre l'attribut
`Toughness` -> `printed_toughness`, pose le statut « Tough » à l'entrée en
jeu (`OnWhenCardEnterPlay`, via `Faces.GiveStatus`) et restaure la valeur
imprimée à chaque `OnResetKeywords` via `GainToughness`. Le statut Tough
lui-même est géré par `CanStatus`
(`src/game/card/face/attribute/can_status.py`, `tough`/`tough_max`/
`IsTough`), et la classe `Toughness(GameRule)` dans
`src/game/effect/rule.py` sert de justification (raison) à l'attribution
du statut. **Aucun script requis** pour ce mot-clé : c'est une des « bases
automatiques » du guide, à ne pas recoder inutilement dans le `.py` de la
carte.

**Carte exemple** : `01076` : * Luke Cage (`desc` contient `"Toughness":
"1"`), lu directement depuis `desc`, aucun script requis. Aucun fichier
`01076.py` trouvé dans `src/cards/pack` : toutes les capacités imprimées
de cette carte (celles qui ne sont pas Toughness) sont donc, sur cet
exemplaire précis, également couvertes par les compteurs `desc`
automatiques du moteur, sans script dédié.

**Pièges connus** : ne pas confondre avec Guard/Retaliate qui portent sur
le combat entre personnages ; Toughness ne protège que contre les dégâts
et le threat venant d'une capacité de carte, pas contre les dégâts/threat
encaissés via l'icône ATK/THW/DEF standard d'une attaque ou d'un schéma.
Si une future carte cumule Toughness avec une capacité imprimée distincte,
vérifier via `find` si un script existe pour cette carte : le script devra
porter uniquement cette capacité annexe, jamais le mot-clé Toughness
lui-même.

**Variantes maison** : aucune recensée pour l'instant.
