# TeamUp

**Texte imprimé / définition** : « Team-Up (Héros A and Héros B). » Cette carte suppose que les deux héros nommés ont des identités héros en jeu **simultanément**. Le mot-clé n'offre généralement pas une capacité distincte, il s'agit plutôt d'une **restriction d'usage** : la carte ne fonctionne que si les deux identités héros sont présentes.

**Mécanisme moteur** : clé `desc.TeamUp` sur la carte (ou plus souvent une condition portée par le script), lue nativement par le moteur. La clé `desc` suppose deux **identités héros** en jeu, pas seulement des alliés. La condition de présence des deux héros est vérifiée quand on tente de jouer ou déclencher la carte. **Script requis si un des héros nommés est en réalité un allié** (voir Pièges connus ci-dessous) : le mot-clé ne suffit plus.

**Carte exemple** : `jj022` : Power Couple (`desc` ne contient pas TeamUp, la condition est portée par le `.py` correspondant). Ce script gère la condition `couple_present()` qui vérifie que Jessica Jones est l'identité actuelle et que Luke Cage (son allié signature) est en jeu. Un fichier `jj022.py` existe dans `src/cards/pack` : ce script gère la capacité complète avec sa condition de présence.

**Pièges connus** : **Ne pas confondre identité et allié.** La clé `desc.TeamUp` suppose **deux vraies identités héros**. Si le second héros nommé est en réalité un **allié signature** (comme Luke Cage pour Jessica Jones), la clé seule ne suffit pas : une condition de script est nécessaire pour vérifier la présence de cet allié (voir `jj022.py` et `docs/reference/GUIDE-CREATION-CONTENU.md` section 9, entrée `jessica_jones`). Certaines cartes Team-Up imposent aussi un placement spécifique (par exemple, une doit être contrôlée par un joueur, l'autre par l'autre).

**Variantes maison** : aucune recensée pour l'instant.
