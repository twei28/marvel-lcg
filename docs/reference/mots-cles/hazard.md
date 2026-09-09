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

> ### ✅ TROISIÈME MÉTHODE, PLUS SÛRE QUE L'ŒIL (09/09/2026)
>
> La comparaison de bandes découpées reste valable, mais il existe désormais
> plus direct : **l'icône est un glyphe de `public/fonts/ChampionsIcons.ttf`**,
> la police officielle, et `public/css/marvel/icon.css` dit lequel.
>
> - `H` → `.icon-hazard` : une carte penchée, un plus évidé sur son bord
>   gauche, **rien en dessous**.
> - `A` → `.icon-acceleration` : la même carte, mais une **pointe en haut à
>   droite** et une **barre épaisse dessous**.
>
> Méthode : rendre les deux glyphes avec Pillow à la même taille, les poser
> côte à côte du scan agrandi, et regarder. Aucune ambiguïté ne survit à cette
> comparaison. C'est ainsi qu'a été tranchée `vz031` First Contact, dont
> l'icône était restée « non identifiée » à son premier portage — elle porte
> **Hazard 1**, ce qui équilibre une amélioration à 2 qui donne +1 aux trois
> pouvoirs. Précédent exact : `27191` Symbiote Suit, la carte basique citée
> par la decklist du même auteur, qui déclare aussi `"Hazard": "1"` sans que
> son texte ne mentionne le mot.
>
> ⚠ **Le `desc` est la SEULE trace** : le texte de ces cartes ne dit pas
> « Hazard », seule l'icône le dit. `verifier_desc_mots_cles.py` ne peut donc
> pas l'attraper, et un oubli reste invisible. Le cas
> « vz031 First Contact » de `test_capacites.py` mesure l'icône en jeu par la
> clé `icones`, ajoutée pour cela.

**Variantes maison** : aucune recensée pour l'instant.
