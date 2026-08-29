# Hazard

**Texte imprimé / définition** : « Hazard. » Rappel imprimé sur les cartes qui le portent (ex. `01107`) : « Hazard Icon: Deal +1 encounter card during the villain phase. » Le compteur `Hazard` (`1`, `2`, ...) fixe le nombre d'icônes Hazard portées par la carte.

**Mécanisme moteur** : clé `desc.Hazard` sur la carte, lue nativement par le moteur. `HasHazard` (`src/game/card/face/attribute/has_hazard.py`) enregistre l'attribut `Hazard` -> `printed_hazard`, restaure la valeur à chaque `OnResetKeywords` via `GainHazard`. `Worlds.GetHazardIcons`/`GetIconsNum` (`src/game/operate/worlds.py`) comptent les icônes Hazard en jeu ; ce total pilote le nombre de cartes Rencontre supplémentaires tirées pendant la phase vilain. **Aucun script requis** pour ce mot-clé : c'est une des « bases automatiques » du guide.

**Carte exemple** : `01107` : Breakin' & Takin' (`desc` contient `"Hazard": "1"`), lu directement depuis `desc`, aucun script requis. Un fichier `01107.py` existe dans `src/cards/pack` : ce script gère une capacité imprimée annexe (placement de threat à la révélation), pas le mot-clé Hazard.

**Pièges connus** : ne pas confondre avec Acceleration, qui agit au début de la phase vilain en posant du threat plutôt qu'en tirant des cartes. Les cartes Hazard peuvent cumuler plusieurs icônes Hazard (compteur > 1), chaque icône déclenchant une pioche supplémentaire. Si une future carte cumule Hazard avec une capacité imprimée distincte, vérifier via `find` si un script existe : le script devra porter uniquement cette capacité annexe, jamais le mot-clé Hazard lui-même.

**Variantes maison** : aucune recensée pour l'instant.
