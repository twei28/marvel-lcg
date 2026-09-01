# TeamUp

**Texte imprimé / définition** : « Team-Up (Héros A and Héros B). » Cette carte suppose que les deux héros nommés ont des identités héros en jeu **simultanément**. Le mot-clé n'offre généralement pas une capacité distincte, il s'agit plutôt d'une **restriction d'usage** : la carte ne fonctionne que si les deux identités héros sont présentes.

**Mécanisme moteur** : clé `desc.TeamUp` sur la carte (ou une condition portée par le script), lue nativement par le moteur. La condition de présence est vérifiée quand on tente de jouer ou déclencher la carte, via la cible `SetTarget("TeamUp")`.

> ⚠️ **CORRIGÉ le 01/09/2026.** Cette fiche affirmait que « la clé `desc` suppose deux **identités héros** en jeu, pas seulement des alliés » et qu'un script était donc obligatoire dès qu'un des noms désigne un allié. **C'est faux.** `HasTeamUp.GetTeamUpUnits()`
> (`src/game/card/face/attribute/has_teamup.py:21`) balaie
> `Worlds.GetOnFieldFriendlyCharacters()`, qui rend
> `[player.GetIdentity()] + player.allies.Get()` (`worlds.py:289`) : les
> **ALLIÉS COMPTENT**. Le commentaire du moteur le dit d'ailleurs en toutes
> lettres, « both of the named characters (identity or ally) are in play ».
> La clé `desc.TeamUp` suffit donc, même quand un des deux noms est un allié.
> Vérifié en écrivant `al023` Little Rascals (Alligator Loki + Honey Badger,
> qui n'existe QUE comme allié : 43003 et wx003).

**Carte exemple** : `jj022` : Power Couple (`desc` ne contient pas TeamUp, la condition est portée par le `.py` correspondant). Ce script gère la condition `couple_present()` qui vérifie que Jessica Jones est l'identité actuelle et que Luke Cage (son allié signature) est en jeu. Un fichier `jj022.py` existe dans `src/cards/pack` : ce script gère la capacité complète avec sa condition de présence.

**Pièges connus** : le vrai piège n'est pas l'allié, c'est le **DECKBUILDING**. Un allié de classe `Hero` appartient à un seul héros : `43003` Honey Badger est une carte signature de X-23, donc un deck d'Alligator Loki ne peut PAS l'inclure. `al023` Little Rascals reste ainsi injouable en solo et ne s'ouvre qu'en multijoueur, aux côtés d'un joueur X-23 ou Wolverine/X-23 qui met son allié en jeu. C'est le fonctionnement voulu d'un Team-Up, pas un défaut.

`jj022` Power Couple porte sa condition en script pour une autre raison : sa carte n'imprime pas la clé `desc.TeamUp` (voir `docs/reference/GUIDE-CREATION-CONTENU.md` section 9, entrée `jessica_jones`).

**Variantes maison** : aucune recensée pour l'instant.

**Note historique** : Le brief du plan mentionnait la card_id `73022` pour Power Couple, mais cet identifiant est périmé (ancien schéma de numérotation). La carte réelle utilise l'identifiant `jj022` du pack jessica_jones et correspond exactement à la description du guide (section 9).
