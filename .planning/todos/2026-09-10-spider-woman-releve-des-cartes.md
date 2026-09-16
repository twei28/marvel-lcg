# Spider-Woman (Kajislav) — relevé du matériel, avant toute ligne de code

**Relevé le 10/09/2026** sur `A créer/Spider-Woman (Released)-20260902T070156Z-1-001.zip`
(42 PNG). Aucune autre copie du zip dans le dépôt.

## Ce que contient vraiment le zip

| Dossier | Fichiers | Cartes distinctes |
|---|---|---|
| racine (identité) | 2 | 1 carte, 2 faces |
| `Hero cards` | 15 | 10 |
| `Aspect Cards` | 8 | 8 |
| `Encounter cards` | 11 | 9 |
| `extras` | 6 | 0 (visuels de boîte, decklists, compteur de PV) |

**29 cartes distinctes, 30 faces.**

## ⚠ Cinq pièges du matériel, tranchés

1. **Le pack numérote chaque EXEMPLAIRE, pas chaque carte.** Six paires ne
   diffèrent que sur le bandeau du numéro (mesure par différence de pixels :
   1,9 % à 3,0 % des lignes, toutes entre y 2008 et 2064) — `swing and kick`,
   `psi-web trap`, `psionic web blast`, `swinging rescue`, `hold im tight`,
   `interruption`.
2. **Les noms de fichiers ne sont PAS les noms des cartes.**
   `01 Cassandra Webb` → **Madame Web**. `45/46 interruption nemesis` →
   **Violent Disturbance**. `03 madame web_s powers` → *Madame Web's Powers*
   (l'apostrophe est devenue `_`). L'importeur d'images doit documenter chaque
   correspondance.
3. **Les numéros d'`Aspect Cards` sautent** (16-19, 23, 25, 35, 40). Ce ne sont
   PAS des cartes manquantes : la decklist de l'auteur montre que les trous
   correspondent à des cartes OFFICIELLES qu'il n'avait pas à dessiner
   (Desperate Defence, Armored Vest, Unflappable, Avengers Mansion…). Les 8
   fichiers présents SONT ses 8 cartes custom.
4. **Le pack livre DEUX SETS NÉMÉSIS ALTERNATIFS**, tous deux numérotés 1/5 à
   5/5, aux bordures différentes :
   - **A, « Man-Bull »** : Man-Bull (sbire), Vault Breakout (manigance),
     Bad Inspiration (traîtrise), Violent Disturbance ×2. Son obligation est
     `41 Separation from the Child`, rangée avec le set HÉROS (son bandeau dit
     « SPIDER-WOMAN », pas « SPIDER-WOMAN NEMESIS »).
   - **B, « verze 2 » (Ms. Marvel)** : Ms. Marvel (sbire), Superhuman
     Registration Act (manigance permanente), Fugitive ×2 (obligation),
     Fighting a Friend (traîtrise). Celui-là a SA PROPRE obligation.
   ⚠ Il faudra choisir lequel monte le deck de départ, et dire pourquoi.
5. **Deux coquilles imprimées de l'auteur** : *Arachnne Costume* (deux n) et
   *Misdiiirection* (trois i). Le nom de la carte garde ce qui est imprimé ;
   la decklist, elle, écrit « Misdirection ».

## Le cœur du pack : les compteurs `psionic web`

L'identité en porte de 0 à **10**. Julia Carpenter en pose 5 au setup, 3 par
Action ; Spider-Woman les dépense pour annuler des icônes de boost, contrer,
frapper. **12 des 29 cartes** les lisent, les posent ou les dépensent.

⚠ Le moteur connaît déjà un compteur `psionic` (`card_face.py:164`, utilisé par
`mw002` et `35013`) mais PAS `psionic web`. À trancher : réutiliser `psionic`
ou ajouter l'entrée.

## Les briques, et ce qui existe déjà

| Besoin | Ce qui existe |
|---|---|
| « pour chaque ressource [mental] utilisée pour payer cette carte » (5 cartes) | brique déjà rodée sur Throg, Beta Ray Bill, Hulk, Lady Sif, Spider-Man 2099, Venomized |
| annuler les icônes de boost **une par une** (identité) | `Message.WhenBoostCardTurnedFaceUp` + `CancelAllBoostIcons` existent ; l'annulation UNITAIRE reste à vérifier |
| **traiter un allié comme un SBIRE** (`44 Bad Inspiration`) | ✅ `AbilityFactory.TreatAsMinion` existe (`factory/treat.py:3`), avec ses gabarits en donnée (`possessed_minion`, `enthralled_minion`, `controlled_minion`…) — **ce n'était pas un sous-système à concevoir** |
| Team-Up (`40 Past and Future`) | base native `desc.TeamUp`, fiche `mots-cles/teamup.md` |
| manigance-joueur **permanente** (`48`) | ✅ correctif du 09/09/2026 (`PlayerSideScheme` hérite de `HasPermanent`/`HasSetup`), livré avec Iron Patriot |

## Ce qui reste à trancher avant de coder

1. Quel set némésis monte le deck de départ ?
2. `psionic` réutilisé, ou `psionic web` ajouté à l'énum ?


## ⛔ SORTI DU BACKLOG le 16/09/2026

Décision de l'utilisateur : **le pack ne sera pas porté.** Le relevé reste ici
pour le jour où l'on y reviendrait, avec ses deux questions jamais tranchées
(quel set némésis monte le deck de départ, et `psionic` réutilisé ou
`psionic web` ajouté à l'énum).

C'était le dernier item de la **vague 4** du plan des héros fan-made : cette
vague s'achève donc sans lui.
