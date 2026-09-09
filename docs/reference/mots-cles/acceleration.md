# Acceleration

**Texte imprimé / définition** : « Acceleration. » Rappel imprimé sur les cartes qui le portent (ex. `01109`) : « Acceleration Icon: Place +1 threat on the main scheme at the start of the villain phase. » Le compteur `Acceleration` (`1`, `2`, ...) fixe le nombre d'icônes Acceleration portées par la carte.

**Mécanisme moteur** : clé `desc.Acceleration` sur la carte, lue nativement par le moteur. `HasAccelerationIcon` (`src/game/card/face/attribute/has_acceleration_icon.py`) enregistre l'attribut `Acceleration` -> `printed_acceleration_icon`, restaure la valeur à chaque `OnResetKeywords` via `GainAccelerationIcon`. `Worlds.GetIconsNum` (`src/game/operate/worlds.py`) compte les icônes Acceleration en jeu ; ce total pilote le threat posé sur le complot principal au début de la phase vilain. **Aucun script requis** pour ce mot-clé : c'est une des « bases automatiques » du guide.

**Carte exemple** : `01109` : Bomb Scare (`desc` contient `"Acceleration": "1"`), lu directement depuis `desc`, aucun script requis. Un fichier `01109.py` existe dans `src/cards/pack` : ce script gère une capacité imprimée annexe (placement de threat à la révélation), pas le mot-clé Acceleration.

**Pièges connus** : ne pas confondre avec Hazard, qui agit pendant la phase vilain en tirant des cartes Rencontre supplémentaires plutôt qu'en posant du threat.

> **Distinguer les deux ICÔNES imprimées** : voir l'encadré de `hazard.md`,
> qui donne la différence visuelle exacte (Acceleration = pointe vers le haut
> **+ barre de soulignement** ; Aléa = carte penchée **nue**) et la méthode de
> découpe employée le 30/08/2026 pour la trancher. `ag011` Assassination Plot
> est le témoin de référence du dépôt pour l'icône Acceleration : son `desc`
> déclare `Acceleration` et son scan porte bien la forme à pointe + barre. Les cartes Acceleration peuvent cumuler plusieurs icônes (compteur > 1), chaque icône plaçant un threat supplémentaire. Si une future carte cumule Acceleration avec une capacité imprimée distincte, vérifier via `find` si un script existe : le script devra porter uniquement cette capacité annexe, jamais le mot-clé Acceleration lui-même.

**Variantes maison** : aucune, mais ⚠ **un homonyme existe, et il est
désormais porté** : voir la fiche dédiée **`acceleration-2099.md`**. Le pack
fan-made **Spider-Man 2099** (Rainy) appelle « *Acceleration* » une CAPACITÉ
D'IDENTITÉ (défausser depuis le dessus du deck jusqu'à un événement, le jouer,
puis remettre les autres cartes sous le deck), sans aucun rapport avec l'icône
décrite ici. Six cartes du pack testent « si tu as joué cette carte via ta
capacité *Acceleration* ». `desc.Acceleration` et `HasAccelerationIcon` ne
sont **pas** employés par ce pack : ce sont deux notions différentes sous le
même mot.

⚠ **Et `sm013` Future in Crisis porte les DEUX** : c'est une obligation du
pack Spider-Man 2099 qui déclare bien `desc.Acceleration` (l'icône, celle de
cette fiche) alors que le héros du même pack porte la capacité homonyme.
Vérifié par comparaison d'image contre `ag011` le 08/09/2026.
