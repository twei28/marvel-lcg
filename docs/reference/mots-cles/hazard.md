# Hazard

**Texte imprimé / définition** : « Hazard. » Rappel imprimé sur les cartes qui le portent (ex. `01107`) : « Hazard Icon: Deal +1 encounter card during the villain phase. » Le compteur `Hazard` (`1`, `2`, ...) fixe le nombre d'icônes Hazard portées par la carte.

**Mécanisme moteur** : clé `desc.Hazard` sur la carte, lue nativement par le moteur. `HasHazard` (`src/game/card/face/attribute/has_hazard.py`) enregistre l'attribut `Hazard` -> `printed_hazard`, restaure la valeur à chaque `OnResetKeywords` via `GainHazard`. `Worlds.GetHazardIcons`/`GetIconsNum` (`src/game/operate/worlds.py`) comptent les icônes Hazard en jeu ; ce total pilote le nombre de cartes Rencontre supplémentaires tirées pendant la phase vilain. **Aucun script requis** pour ce mot-clé : c'est une des « bases automatiques » du guide.

**Carte exemple** : `01107` : Breakin' & Takin' (`desc` contient `"Hazard": "1"`), lu directement depuis `desc`, aucun script requis. Un fichier `01107.py` existe dans `src/cards/pack` : ce script gère une capacité imprimée annexe (placement de threat à la révélation), pas le mot-clé Hazard.

**Pièges connus** : ne pas confondre avec Acceleration, qui agit au début de la phase vilain en posant du threat plutôt qu'en tirant des cartes.

> **Distinguer les deux ICÔNES imprimées** (relevé le 30/08/2026 sur le pack
> `howard_the_duck`, tranché par l'utilisateur ; les deux se ressemblent
> beaucoup et une lecture au jugé les confond) :
> - **Aléa / Hazard** : une carte à jouer **penchée**, portant une croix, et
>   **rien en dessous**. Exemple : `hd022` Duck and Cover!
> - **Acceleration** : la même croix, mais la forme porte une **pointe/flèche
>   vers le haut à droite** ET une **barre épaisse de soulignement** en
>   dessous. Exemples : `hd026` A Fowl Plot, `ag011` Assassination Plot.
>
> Méthode de vérification employée : découper la bande basse du cadre de
> texte des cartes à comparer, agrandir ×2, et les mettre côte à côte (une
> carte du dépôt dont le `desc` déclare déjà le mot-clé sert de témoin —
> ici `ag011`, qui déclare `Acceleration`). Une manigance sans aucune icône
> (`hd025` Duck, Duck, Doom!) sert de contrôle négatif : elle prouve que
> l'icône n'est pas un décor du gabarit. Les cartes Hazard peuvent cumuler plusieurs icônes Hazard (compteur > 1), chaque icône déclenchant une pioche supplémentaire. Si une future carte cumule Hazard avec une capacité imprimée distincte, vérifier via `find` si un script existe : le script devra porter uniquement cette capacité annexe, jamais le mot-clé Hazard lui-même.

**Variantes maison** : aucune recensée pour l'instant.
