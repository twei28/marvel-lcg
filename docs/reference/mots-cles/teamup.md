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


## Pièges vus au portage de Hellcat (11/09/2026)

- **Le chargeur EXIGE `.SetTarget("TeamUp")`** sur chaque capacité d'un
  événement à `desc.TeamUp` (`cards/database.py:223`, assert en debug) : les
  deux personnages nommés deviennent les cibles. Sans lui la partie meurt au
  setup (« AssertionError: origin_card_id='hc020' »). Modèle 14018 Order and
  Chaos ; hc020 Green Hell, hc021 Hell-Iron.
- **« Team-Up (any 2 of A, B, C, D) »** (hc022 Divas) n'est pas exprimable
  par `desc.TeamUp` (deux groupes « A;B », les DEUX exigés). On omet la clé
  et on code la condition à la main (`conditions=` sur l'action : au moins
  deux des personnages nommés en jeu côté joueur). Le deckbuilder n'applique
  alors aucune restriction Team-Up à cette carte : écart noté.


## Plus aucune cible a designer (12/10/2026, signalement Lilipulse)

- **Regle** : RR 1.8 p.43, une carte Team-Up « ne peut etre jouee que si les deux
  personnages amis nommes (identite ou allie) sont en jeu ». C'est une CONDITION,
  pas un choix.
- **Defaut** : le selecteur `TeamUp` (range 2-2) etait rendu au plateau comme deux
  cibles a designer ; le plateau n'auto-coche qu'une cible unique, rien ne disait
  de cliquer les deux personnages (Daredevil etait meme cache sous le panneau) :
  « Choisir jusqu'a 2 cibles · 0/2 requise(s) » et le joueur restait bloque
  (60055 See No Evil, Hear No Evil).
- **Correctif** : `Effect.Render` n'expose ni cibles ni plage pour un premier
  selecteur `TeamUp` (`IsTeamUpSelection`, `game/effect/effect.py`), et le
  controleur pose lui-meme les deux personnages quand la reponse arrive sans cible
  (`engine/controller/controller.py`). Les selecteurs suivants (62023 : ennemi,
  personnage) restent demandes. Cas : 60055 (aucune cible, meme option deux fois,
  injouable sans Daredevil), temoin 62023.


## Team-Up avec un ALLIE au nom accentue (17/10/2026, ub019 Honorable Blades)

- `desc.TeamUp = "Leonardo;Usagi Yōjimbō"` : le nom de l'allie (`* Usagi Yōjimbō`, up041) se compare par
  `IsName` (etoile d'unicite et macron compris), il suffit d'ecrire le NOM EXACT de la carte alliee.
- `effect.targets` = les deux personnages, SANS ordre garanti : quand l'effet differe selon le personnage
  (« Cloak Leonardo, tough sur Usagi »), les distinguer par `perso.IsName(...)`.
- Cas : `[ub] ub019` (jouable avec les deux, injouable avec un seul, des deux cotes), `tools/cas/tmnt_aspect_basic.py`.



## Second selecteur lu une seule fois (25/10/2026, wn009 Hey you!)

- `effect.targets2` (l'ennemi choisi apres les deux personnages du Team-Up) ne se lit qu'UNE fois :
  une seconde lecture leve `AssertionError` (`initialized_targets`), AVALEE par le moteur. « Stun and
  confuse an enemy » posait le Sonne puis s'arretait. Garder `ennemis = list(effect.targets2)`.
- Team-Up dont un nom est porte par PLUSIEURS cartes (« Spider-Man », « Hulk ») : `desc.TeamUp` compare
  les noms, toute identite ou alliee de ce nom ouvre la carte (wn011 : allie 13019 Spider-Man).
