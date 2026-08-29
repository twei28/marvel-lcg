# Quickstrike

**Texte imprimé / définition** : « Quickstrike. » Un personnage avec ce
mot-clé inflige ses dégâts de combat avant que son adversaire ne puisse
riposter (par exemple, un minion Quickstrike attaquant un héros défenseur
inflige ses dégâts avant que ce héros ne puisse déclencher son propre
Retaliate). C'est un compteur (`Quickstrike 1`, `Quickstrike 2`, ...),
réinitialisé à sa valeur imprimée à chaque reset des mots-clés.

**Mécanisme moteur** : clé `desc.Quickstrike` sur la carte, lue nativement
par le moteur. `HasQuickstrike`
(`src/game/card/face/attribute/can_quickstrike.py`) enregistre l'attribut
`Quickstrike` -> `printed_quickstrike`, restaure la valeur à chaque
`OnResetKeywords` via `GainQuickstrike`, et expose `IsQuickstrike()`. La
séquence de résolution du combat (ordre dégâts / Retaliate) consulte cet
état pour décider qui frappe en premier. **Aucun script requis** pour ce
mot-clé.

**Carte exemple** : `01167` : * Vulture (`desc` contient `"Quickstrike":
"1"`), lu directement depuis `desc`, aucun script requis. Aucun fichier
`01167.py` trouvé dans `src/cards/pack` : cette carte porte aussi
`Nemesis: Spider-Man`, un autre mot-clé, sans que cela nécessite de script
propre (le nemesis est également géré nativement).

**Pièges connus** : ne pas coder manuellement un ordre de résolution des
dégâts dans le `.py` d'une carte Quickstrike : c'est le moteur de combat
qui l'orchestre via le compteur `desc`. Si une future carte cumule
Quickstrike avec une capacité imprimée annexe, vérifier via `find` si un
script existe pour cette carte : le script devra porter uniquement cette
capacité annexe, jamais le mot-clé Quickstrike lui-même.

**Variantes maison** : aucune recensée pour l'instant.
