# Une cinquième couleur de ressource : l'éclair

**Décidé le 11/09/2026.** Le pack fan-made Zeus (Mozilla) invente une
ressource, l'**éclair**, distincte de l'énergie officielle. Relevé complet et
vocabulaire dans `.planning/todos/2026-09-11-zeus-releve-des-cartes.md`.
L'utilisateur a tranché : on ajoute une **vraie cinquième couleur au moteur**,
pas un contournement local au pack.

Ce document ne couvre que la couleur. Le pack Zeus est un chantier séparé, qui
suivra `docs/reference/PROCESSUS-HEROS.md` une fois la couleur en place.

## Règles retenues

- **Vocabulaire** : *énergie* = la ressource officielle jaune (`Y`) ;
  *éclair* = la nouvelle (`L`, *lightning*).
- **Un joker vaut aussi un éclair.** C'est la règle du jeu (un joker vaut
  n'importe quel type) et le défaut du moteur (`convert_green_res=True`).
  Décision de l'utilisateur, 11/09/2026.
- **Un éclair paie tout coût générique**, comme n'importe quelle ressource.
- **Un éclair ne paie PAS un coût typé d'une autre couleur** : « Requirement
  (énergie) » refuse un éclair, exactement comme il refuse un mental.
- **Rien n'est spécifique à Zeus** dans le moteur. Une carte d'aspect qui dit
  « dépensez une ressource de n'importe quel type » accepte un éclair sans
  qu'on la touche.

## Approche : un cinquième champ, à la manière du code existant

`ResRBYG(r, b, y, g)` devient `ResRBYG(r, b, y, g, l)`, et chaque endroit qui
énumère les quatre couleurs à la main en énumère cinq. C'est l'idiome du
moteur : lisible, greppable, et le test qui fige la liste des couleurs des deux
côtés devient la gate qui prouve qu'aucun endroit n'a été oublié.

Rejeté : réécrire `ResRBYG` autour d'une table de couleurs. Plus élégant, mais
c'est réécrire le cœur du paiement, qui marche, pour un besoin qu'on n'a qu'une
fois, avec un risque de régression sur 2 500 cartes.

## Conventions

| | Valeur |
|---|---|
| Lettre moteur (`desc.RES`, coûts typés, `res_text`) | `L` |
| Jeton de narration | `[[lightning]]` |
| Clé anglaise (plateau, deckbuilder) | `lightning` |
| Nom français | `éclair` |
| Couleur sur le plateau | bleu électrique, pour ne pas se confondre avec l'énergie jaune |
| Icône sur le plateau | SVG en ligne (la police `ChampionsIcons.ttf` n'a pas d'éclair droit) |

`L` n'entre en collision ni avec `R B Y G`, ni avec un chiffre, ni avec le
`lstrip("RBY")` de `ResRBYGA.FromText`.

## Moteur (`Fusion/marvel-lcg-src/src`)

- `game/element/rbyg.py` : `l` dans le constructeur, `__mul__`, `__add__`,
  `__sub__`, `FromText`, `GetColor`, `OnlyHasColor`, `GetTypeKindsInternal`,
  `IsSameType`, `IsDifferentType`, `CanPayThisCost`. `RBYG` et `RBY` gagnent
  `"L"`. Propriété `l` sur `ResRBYGA`.
- `game/element/resources.py` : `RES_TEXT["l"]`, `RBYG_LIST`, le `Literal` du
  constructeur, un `check_value` de plus dans `IsMatchCost`, propriété `l`.
- `game/element/cost.py` : propriété `l`, `GetSpendText` écrit `[[lightning]]`.
- `game/render/symbol.py` : `r_l_lightning`, sa ligne dans `CleanPrompt`.
- `game/player/model/player_ask.py` : `AskSpecifyResources` propose `L`
  quand on précise un joker ; `DeclareResourceType` gagne `l: bool=True`.
- `game/operate/faces_counter.py` : `"L": 0` dans le dictionnaire initial.
- `game/world/cheat/cheat_cmd_helper.py` : `Res("RBYGL")`.
- `checker.py`, `finder.py`, `players.py` et les annotations
  `Resources.RBYG|None` (`ability.py`, `cost_func.py`, `asset.py`,
  `asset_helper.py`, `enhance_self.py`, `face_gain.py`) suivent le `Literal`
  sans changement de logique.
- `data/cards.json` : aucun changement de format. Thunder Strike portera
  `"RES": "L"` quand le pack sera écrit.

## Plateau (`ui-app/src/board`)

- `icones-ressources.tsx` : cinquième entrée de `RESSOURCES`, marqueur
  `⟦L⟧`, rendu SVG pour cette entrée dans `avecIcones`.
- `ask.ts` : les regex `[rbyg]` deviennent `[rbygl]`, `NOM_TYPE.L`.
- `raisons-refus.ts` : `L: 'éclair'`.
- `compteurs-fr.ts` : `lightning: 'éclair'`. `dico-en.ts` : `éclair: 'lightning'`.
- `board.css` : `.icone-res.res-lightning`.
- Le rendu du jeton à un crochet `[lightning]` dans les textes français suit
  le chemin des quatre autres (à localiser dans le plan).

## Deckbuilder et outils

- `public/js/marvel/lib.js` : `lightning` dans `cleanResText`, classe
  `.icon-lightning` dans la feuille de style du deckbuilder.
- `tools/test_capacites.py` : le gabarit `icones` lit `desc.RES` et doit
  accepter `L`.

## Preuves

1. **Gate des couleurs** : `noms-ressources.test.ts` attend cinq lettres des
   deux côtés. Vue rouge avant que le plateau ne soit touché, verte après.
2. **Test moteur**, exécuté et vu rouge avant le changement :
   - `Resources.FromText("L")` compte 1 éclair, 0 partout ailleurs ;
   - un éclair paie `Cost("1")` ;
   - un joker satisfait `Cost("L")` ;
   - un éclair ne satisfait PAS `Cost("Y")` ;
   - `FacesCounter.GetPrintedResourcesCount` voit une face `RES: "L"` ;
   - `GetResourceIconTypes` compte l'éclair comme un type.
3. **Non-régression** : `tools/verifier_tous_les_decks.py` vert, et une
   fournée `tools/autoplay.py` sur deux decks témoins sans traceback, avec des
   rounds tenus comparables à la mesure du jour (spider_man / rhino 7,5).
4. `npm test` et `npm run build` du plateau verts.

## Hors périmètre

- Le pack Zeus lui-même (cartes, textes, scans, deck de départ).
- Toute règle qui ferait de l'éclair une exception aux jokers.
- L'icône sur les scans : la carte est une image, rien à dessiner.
