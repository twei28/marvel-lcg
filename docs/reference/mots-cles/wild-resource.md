# Wild resource (ressource wild, icône étoile verte)

**Texte imprimé / définition** (Rules Reference v1.8, « Wild Resource ») : « When a player generates a wild resource, they may specify which
resource type (energy, mental, physical, or wild) it is being used as. » Et : « When resources are not being generated for a cost, a wild
resource does not have any characteristic other than "wild resource." In such contexts, wild resources cannot be interpreted as any of the
other resource types. » Arbitrage du 26/10/2026 : un wild DÉPENSÉ compte pour UN seul type, celui que le joueur déclare ; un wild IMPRIMÉ
sur une carte (en main, dans le deck, glissé, défaussé) n'est QUE « wild » : il ne vaut ni physique, ni mental, ni énergie.

**Mécanisme moteur** :
- Les ressources sont des `Resources` (`src/game/element/resources.py`, `rbyg.py`) : `r`, `b`, `y`, `g` (wild), `l`.
- **Payer** : le wild reste `G` dans `effect.GetPaidResources()` (mesuré le 26/10/2026 sur Polymath payée avec Hellcat : `G=1, R=B=Y=0`).
  `effect.GetPaidResources(True)` appelle `Player.AskSpecifyResources` (`game/player/model/player_ask.py`) : le joueur choisit une combinaison
  (`R`, `B`, `Y`, `L` pour un wild ; `RR`, `RB`, ... pour deux) et le `G` est remplacé par ces couleurs. Le wild lui-même n'est pas proposé
  (inutile : une ligne « wild » n'existe pas dans les textes de cartes).
- **Lire une icône imprimée** : `face.printed_resource.GetColor(c, convert_green_res=False)` (ou `HasColorPrinted(c)`). `GetColor(c)` sans
  l'argument CONVERTIT le wild en R, B et Y à la fois : à ne pas utiliser pour « a printed [x] resource » (voir `has_printed_res` du
  `CardFinder`, qui ne convertit pas).
- **Ensemble de types d'une carte** (Ch'od) : `Types(face)` dans `src/cards/pack/chod/*/__init__.py` rend un sous-ensemble de `{R, B, Y, G}`.
  « Different printed resources » (Mentor) = `len(ensemble)` ; « matches » (Duel of Wits, Strike and Phase) = intersection non vide, donc un
  wild ne correspond qu'à un autre wild.

**Carte exemple** : `co005` Polymath (une ligne par type payé, wild déclaré), `bg005` Batarangs (une ligne par ressource payée),
`gs301` No Holding Back (modèle de `GetPaidResources(True)`), `co008`-`co010` (wild en main : aucun bonus), `co012` Mentor, `co013`, `co015`.

**Pièges connus** :
- Le harnais choisit la PREMIÈRE option : un wild payé est donc déclaré `R`. Pour tester une autre déclaration : `preferer_option="Y"` (un
  wild) ou `preferer_option="BY"` (deux). Pour deux ressources payées il faut deux cartes wild (`payer_avec=["01020", "01020"]`).
- `DECK("01020")` + `Puzzle.Gain('01020')` en main : le `Gain` PREND la Hellcat du deck. Un cas qui veut un wild en main ET au dessus du deck
  en met deux dans le deck.
- Mesurer « la carte milled est en défausse » est fragile quand le deck se vide (le moteur remélange la défausse) : mesurer la main.
- `SeulementPaye(...)` de Batgirl (« paid using ONLY [x] ») regarde `OnlyHasColor` : le wild y compte comme n'importe quelle couleur (RR :
  il peut être déclaré de ce type).

**Variantes maison** : « [wild] » à l'impression sur une ressource d'un pack fan-made = `RES: "G"` dans `cards.json`. Nightwing (`bg003`) et
Master Plan (`bg006`) transforment les ressources générées en wild : le joueur déclare alors leur type au paiement.

**Compléments du 26/10/2026 (passe `verifier_api_cartes`)** : `bw010` / `bw011` Shockwave et `bw025` Brains and Brawn comptaient `icones.r + icones.g` et
`icones.b + icones.g` (chaque wild IMPRIMÉ frappait ET retirait de la menace) ; corrigé : `icones.r` et `icones.b` seuls (cas `[api] bw0…`, deck de wild
seulement : aucun effet). À l'inverse, les cartes dont le TEXTE imprime « [wild] – All of the above » ou « printed [energy] and [wild] » (`53018` Spectrum,
`56055`, `09028`, `09004`, `17011`, `mw010`, `45156`, `45157`, `56070`, `wd154`) comptent le wild exprès : ne pas les « corriger ». Les lectures d'un seul type
dans un paiement (`GetPaidResources().GetColor("R")`…) restent justes : le joueur peut déclarer le wild de ce type.
