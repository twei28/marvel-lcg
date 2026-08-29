# Retaliate

**Texte imprimé / définition** : « Retaliate. » Un personnage avec ce
mot-clé inflige, en plus de ses dégâts normaux de défense, des dégâts
supplémentaires égaux à sa valeur de Retaliate à l'attaquant qui vient de
l'attaquer, une fois le combat résolu. C'est un compteur (`Retaliate 1`,
`Retaliate 2`, ...), réinitialisé à sa valeur imprimée à chaque reset des
mots-clés.

**Mécanisme moteur** : clé `desc.Retaliate` sur la carte, lue nativement
par le moteur. `HasRetaliate`
(`src/game/card/face/attribute/can_retaliate.py`) enregistre l'attribut
`Retaliate` -> `printed_retaliate`, restaure la valeur à chaque
`OnResetKeywords` via `GainRetaliate`, et fournit
`ResolveRetaliate(atk_message)` qui applique les dégâts en retour en
s'appuyant sur la classe `Retaliate(GameRule)` de
`src/game/effect/rule.py` comme justification de l'effet. **Aucun script
requis** pour ce mot-clé.

**Carte exemple** : `01040a` : * Black Panther (`desc` contient
`"Retaliate": "1"`), lu directement depuis `desc`, aucun script requis.
Aucun fichier `01040a.py` trouvé dans `src/cards/pack` : cette face de
carte n'a pas de capacité imprimée distincte nécessitant un script.

**Pièges connus** : Retaliate est lié à l'ordre de résolution du combat
(voir Quickstrike, qui peut empêcher un Retaliate de se déclencher si
l'attaquant tue le défenseur avant qu'il ne riposte). Si une future carte
cumule Retaliate avec une capacité imprimée annexe (déclencheur sur les
dégâts infligés, par exemple), vérifier via `find` si un script existe
pour cette carte : le script devra porter uniquement cette capacité
annexe, jamais le mot-clé Retaliate lui-même. La carte `03009` (Captain
America's Shield) illustre ce piège concret ailleurs dans le catalogue :
elle a un script (`AbilityFactory.GiveKeywordToAttached`), mais ce script
code sa capacité d'ATTACHEMENT (donner Defense 1 et Retaliate 1 à
Captain America), pas le mot-clé Retaliate en tant que tel.

**Variantes maison** : aucune recensée pour l'instant.
