# Amplify

**Texte imprimé / définition** : « Amplify. » Quand une carte boost est retournée face-up pendant l'activation d'un ennemi, ajouter un icône boost supplémentaire pour chaque schéma annexe en jeu avec ce mot-clé. Le compteur `Amplify` (`1`, `2`, ...) fixe le nombre d'icônes Amplify portées par la carte.

**Mécanisme moteur** : clé `desc.Amplify` sur la carte, lue nativement par le moteur. `HasAmplify` (`src/game/card/face/attribute/has_amplify.py`) enregistre l'attribut `Amplify` -> `printed_amplify`, restaure la valeur à chaque `OnResetKeywords` via `GainAmplify`. Quand une carte boost est révélée durant l'activation d'un ennemi, `ResolveAmplify()` compte les icônes Amplify en jeu et ajoute autant d'icônes boost via `face.GainBoostIcons()`. **Aucun script requis** pour ce mot-clé : c'est une des « bases automatiques » du guide.

**Carte exemple** : `16054` : Vendetta (`desc` contient `"Amplify": "1"`), lu directement depuis `desc`, aucun script requis. Aucun fichier `16054.py` trouvé dans `src/cards/pack` : cette carte ne porte que le mot-clé Amplify, sans capacité imprimée annexe.

**Pièges connus** : Amplify s'ajoute aux icônes boost d'une carte révélée, il ne remplace pas les icônes existants. Les cartes Amplify peuvent cumuler plusieurs icônes (compteur > 1), chaque icône ajoutant un boost supplémentaire à la carte révélée. Amplify s'applique uniquement au moment de la révélation d'un boost ; c'est un modificateur d'activation d'ennemi, pas une propriété permanente de la carte boost. Si une future carte cumule Amplify avec une capacité imprimée distincte, vérifier via `find` si un script existe : le script devra porter uniquement cette capacité annexe, jamais le mot-clé Amplify lui-même.

**Variantes maison** : aucune recensée pour l'instant.
