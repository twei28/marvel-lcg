# Cinquième couleur de ressource (l'éclair) : plan d'implémentation

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Le moteur et le plateau connaissent une cinquième couleur de ressource, `L` (*lightning*, « éclair »), avec les mêmes droits que les quatre officielles.

**Architecture:** Un cinquième champ `l` dans `ResRBYG`, propagé à la main partout où les quatre couleurs sont énumérées (moteur Python, plateau React, deckbuilder JS). Un joker vaut aussi un éclair (défaut `convert_green_res=True`). Le test `noms-ressources.test.ts` relit les deux tables et sert de gate.

**Tech Stack:** Python 3.10 (`$HOME/marvel-work/python/bin/python3.10`), React + TypeScript + vitest (`ui-app`), JS vanilla (deckbuilder).

**Spec:** `docs/superpowers/specs/2026-09-11-cinquieme-couleur-de-ressource-design.md`

## Global Constraints

- Lettre moteur `L`, jeton `[[lightning]]`, clé `lightning`, nom français `éclair`.
- Un joker (`G`) vaut aussi un éclair. Un éclair ne paie PAS un coût typé d'une autre couleur.
- Rien n'est spécifique à Zeus : aucun `if pack == zeus` nulle part.
- Le pack Zeus lui-même est HORS de ce plan.
- Français dans les commentaires et messages, jamais d'em dash.
- Chaque gate doit être vue ROUGE avant d'être vue verte (§9 du guide).
- Ne jamais lancer deux harnais moteur en même temps (ils réécrivent `launch.json`).
- Variables des commandes : `W="/mnt/c/Users/arnau/Desktop/Marvel LCG/Fusion/marvel-lcg-src"`, `PY=$HOME/marvel-work/python/bin/python3.10`, `UI="/mnt/c/Users/arnau/Desktop/Marvel LCG/ui-app"`. Les harnais visent `"$W/.game-src"` en chemin ABSOLU.
- Commits : messages en français, sans em dash, terminés par `Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>` et `Claude-Session: https://claude.ai/code/session_01R131dpS8vFms5zXYY8CHff`.

---

## Structure des fichiers

| Fichier | Rôle dans ce plan |
|---|---|
| `Fusion/marvel-lcg-src/tools/test_couleur_eclair.py` | **Créé.** Test moteur autonome de la cinquième couleur. |
| `src/game/element/rbyg.py` | Le champ `l` et toutes les opérations. |
| `src/game/element/resources.py` | `RES_TEXT`, `RBYG_LIST`, `IsMatchCost`, propriété `l`. |
| `src/game/element/cost.py` | Propriété `l`, `GetSpendText`. |
| `src/game/render/symbol.py` | `r_l_lightning`, `CleanPrompt`. |
| `src/game/player/model/player_ask.py` | `AskSpecifyResources`, `DeclareResourceType`. |
| `src/game/operate/faces_counter.py` | Dictionnaire initial des couleurs. |
| `src/game/world/cheat/cheat_cmd_helper.py` | `Res("RBYGL")`. |
| `ui-app/src/board/icones-ressources.tsx` | Cinquième entrée, rendu SVG. |
| `ui-app/src/board/board.css` | `.res-lightning`. |
| `ui-app/src/board/ask.ts` | `NOM_TYPE.L`, regex `[rbygl]`. |
| `ui-app/src/board/raisons-refus.ts` | `L: 'éclair'`. |
| `ui-app/src/board/compteurs-fr.ts`, `dico-en.ts` | Traductions. |
| `ui-app/src/board/noms-ressources.test.ts` | La gate : cinq lettres des deux côtés. |
| `ui-app/src/board/icones-ressources.test.tsx`, `paiement-type.test.ts` | Cas de l'éclair. |
| `Fusion/marvel-lcg-src/public/js/marvel/lib.js`, `public/css/marvel/icon.css` | Deckbuilder. |
| `docs/reference/mots-cles/eclair.md`, `README.md` | Fiche de la ressource maison. |

---

### Task 1 : le cœur du moteur (`rbyg.py`, `resources.py`, `cost.py`, `symbol.py`)

**Files:**
- Create: `Fusion/marvel-lcg-src/tools/test_couleur_eclair.py`
- Modify: `Fusion/marvel-lcg-src/src/game/element/rbyg.py`
- Modify: `Fusion/marvel-lcg-src/src/game/element/resources.py:10-25,100-112,160-175`
- Modify: `Fusion/marvel-lcg-src/src/game/element/cost.py:116-140`
- Modify: `Fusion/marvel-lcg-src/src/game/render/symbol.py:33-36,70-75`

**Interfaces:**
- Produces: `ResRBYG(r, b, y, g, l=0)`, propriété `.l` sur `ResRBYG`, `ResRBYGA`, `Resources`, `Cost` ; `Resources.RBYG_LIST == ["R","B","Y","G","L"]` ; `Symbol.r_l_lightning` ; jeton `[[lightning]]`.

- [ ] **Step 1 : écrire le test qui échoue**

Créer `Fusion/marvel-lcg-src/tools/test_couleur_eclair.py` :

```python
"""La cinquieme couleur de ressource : l'eclair (`L`, lightning).

    $PY tools/test_couleur_eclair.py [game_dir]

Aucune partie, aucun port : on importe les briques de paiement et on les
interroge. Le test est AUTONOME et rapide (< 2 s).

Ce qu'il prouve, et pourquoi (spec du 11/09/2026) :
- `L` est une couleur a part entiere : lue, comptee, rendue ;
- un eclair paie un cout generique comme n'importe quelle ressource ;
- un joker vaut aussi un eclair (regle du jeu, defaut du moteur) ;
- un eclair ne paie PAS un cout type d'une autre couleur.

⚠ Avant le changement moteur, `Resources.FromText("L").val` vaut 0 : la lettre
est ignoree en silence. C'est le premier cas ci-dessous, et il DOIT etre vu
rouge avant d'etre vu vert.
"""
import os
import sys

RACINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GAME_DIR = sys.argv[1] if len(sys.argv) > 1 else os.path.join(RACINE, "src")
os.chdir(GAME_DIR)
sys.path.insert(0, GAME_DIR)

from engine import Engine  # noqa: F401  amorce les imports du moteur dans le bon ordre
from game.element.resources import Resources
from game.element.cost import Cost
from game.render.symbol import Symbol

ECHECS = []


def cas(nom: str, ok: bool) -> None:
    print(("OK    " if ok else "ECHEC ") + nom)
    if not ok:
        ECHECS.append(nom)


def main() -> None:
    eclair = Resources.FromText("L")
    cas("`L` est lu comme une ressource (val == 1)", eclair.val == 1)
    cas("`L` ne compte dans aucune couleur officielle",
        eclair.r == 0 and eclair.b == 0 and eclair.y == 0 and eclair.g == 0)
    cas("`L` est compte par GetColor('L')", eclair.GetColor("L") == 1)
    cas("`L` figure dans RBYG_LIST", "L" in Resources.RBYG_LIST)

    cas("un eclair paie un cout generique de 1", eclair.IsMatchCost(Cost("1")))
    cas("un eclair paie un cout type `L`", eclair.IsMatchCost(Cost("L")))
    cas("un joker paie un cout type `L`", Resources.FromText("G").IsMatchCost(Cost("L")))
    cas("un eclair ne paie PAS un cout type `Y`", not eclair.IsMatchCost(Cost("Y")))
    cas("une energie ne paie PAS un cout type `L`", not Resources.FromText("Y").IsMatchCost(Cost("L")))
    cas("`YL` exige une energie ET un eclair : `YY` echoue",
        not Resources.FromText("YY").IsMatchCost(Cost("YL")))
    cas("`YL` exige une energie ET un eclair : `YL` passe",
        Resources.FromText("YL").IsMatchCost(Cost("YL")))
    cas("`YL` exige une energie ET un eclair : `YG` passe (joker)",
        Resources.FromText("YG").IsMatchCost(Cost("YL")))
    cas("CanPayThisCost : un eclair peut contribuer a un cout `L`",
        eclair.CanPayThisCost(Cost("L")))

    cas("l'eclair est un type d'icone a part entiere (RBYGL -> 5)",
        Resources.FromText("RBYGL").GetResourceIconTypes() == 5)
    cas("IsSameType : `LL` est d'un seul type", Resources.FromText("LL").rbyg.IsSameType())
    cas("IsSameType : `LY` n'est pas d'un seul type", not Resources.FromText("LY").rbyg.IsSameType())
    cas("IsDifferentType : `RBYL` fait 4 types", Resources.FromText("RBYL").rbyg.IsDifferentType() == 4)
    cas("OnlyHasColor('L') : `LG` ne contient que des eclairs (joker compris)",
        Resources.FromText("LG").OnlyHasColor("L"))
    cas("addition et multiplication portent `l`",
        (Resources.FromText("L") + Resources.FromText("L")).l == 2
        and (Resources.FromText("L") * 3).l == 3)

    cas("le texte couleur d'un eclair contient la lettre L",
        "L" in Symbol.Clean(eclair.color_text))
    cas("CleanPrompt rend le jeton [[lightning]]",
        Symbol.CleanPrompt(Symbol.r_l_lightning) == "[[lightning]]")
    cas("Cost('L').GetSpendText() ecrit [[lightning]]",
        any("[[lightning]]" in morceau for morceau in Cost("L").GetSpendText()))

    print()
    if ECHECS:
        print(f"ECHEC : {len(ECHECS)} cas rouge(s)")
        for nom in ECHECS:
            print("  - " + nom)
        sys.exit(1)
    print("OK : la cinquieme couleur est en place")


if __name__ == "__main__":
    main()
```

- [ ] **Step 2 : le lancer et le voir échouer**

```bash
W="/mnt/c/Users/arnau/Desktop/Marvel LCG/Fusion/marvel-lcg-src"; PY=$HOME/marvel-work/python/bin/python3.10
cd "$W" && $PY tools/test_couleur_eclair.py
```
Attendu : le premier cas `ECHEC` (`val == 0`), puis d'autres rouges, et `sys.exit(1)`. Une exception `AttributeError: 'Resources' object has no attribute 'l'` est aussi un échec acceptable à ce stade. Si TOUT est vert, le test ne teste rien : s'arrêter.

- [ ] **Step 3 : `symbol.py`**

Dans `src/game/render/symbol.py`, après `r_g_wild` (ligne 36) :
```python
    r_l_lightning   = f'{Fore.CYAN}L{Fore.RESET}'  # eclair, ressource maison du pack Zeus (11/09/2026)
```
Dans `CleanPrompt`, après la ligne `[[wild]]` :
```python
        text = text.replace(Symbol.r_l_lightning, "[[lightning]]")
```

- [ ] **Step 4 : `rbyg.py`**

Remplacer la classe `ResRBYG` (jusqu'à `class ResRBYGA`) par :
```python
class ResRBYG:

    # `L` : l'eclair (lightning), ressource MAISON du pack Zeus, ajoutee le
    # 11/09/2026. Cinquieme couleur a part entiere : un joker la vaut aussi,
    # et elle ne paie pas un cout type d'une autre couleur.
    RBYG: TypeAlias = Literal["R", "B", "Y", "G", "L"]
    RBY: TypeAlias = Literal["R", "B", "Y", "L"]

    def __init__(self, r: int, b: int, y: int, g: int, l: int = 0) -> None:
        from game.element.resources import Resources
        self.r = r # phySiCal
        self.b = b # mental
        self.y = y # energy
        self.g = g # wild, can be used as their type or any of the other types.
        self.l = l # lightning (eclair)

        self.total = r + b + y + g + l

        self.types = sum(1 for color in [self.r, self.b, self.y, self.g, self.l] if color > 0)

        self.color_text = ""
        self.color_text += f'{Resources.RES_TEXT["r"]*self.r}'
        self.color_text += f'{Resources.RES_TEXT["b"]*self.b}'
        self.color_text += f'{Resources.RES_TEXT["y"]*self.y}'
        self.color_text += f'{Resources.RES_TEXT["g"]*self.g}'
        self.color_text += f'{Resources.RES_TEXT["l"]*self.l}'

    def __mul__(self, val: int) -> 'ResRBYG':
        return ResRBYG(self.r*val, self.b*val, self.y*val, self.g*val, self.l*val)

    def __add__(self, other: 'ResRBYG|int') -> 'ResRBYG':
        if isinstance(other, int):
            return ResRBYG(self.r, self.b, self.y, self.g, self.l)
        else:
            return ResRBYG(self.r+other.r, self.b+other.b, self.y+other.y, self.g+other.g, self.l+other.l)

    def __sub__(self, other: 'ResRBYG|int') -> 'ResRBYG':
        if isinstance(other, int):
            return self + (-1 * other)
        else:
            return ResRBYG(self.r-other.r, self.b-other.b, self.y-other.y, self.g-other.g, self.l-other.l)

    @staticmethod
    def FromText(rbyg: str) -> 'ResRBYG':
        rbyg = rbyg.lower()
        r, b, y, g, l = rbyg.count('r'), rbyg.count('b'), rbyg.count('y'), rbyg.count('g'), rbyg.count('l')
        return ResRBYG(r, b, y, g, l)

    def OnlyHasColor(self, text: "ResRBYG.RBY") -> bool:
        if self.total == 0:
            return False
        if text == "R":
            return self.r + self.g == self.total
        elif text == "B":
            return self.b + self.g == self.total
        elif text == "Y":
            return self.y + self.g == self.total
        elif text == "L":
            return self.l + self.g == self.total

    def GetColor(self, text: 'ResRBYG.RBYG', *, convert_green_res: bool = True) -> int:
        if "G" in text:
            assert convert_green_res == False, f"{text=}"
        if convert_green_res:
            g = self.g
        else:
            g = 0
        if text == "R":
            return self.r + g
        elif text == "B":
            return self.b + g
        elif text == "Y":
            return self.y + g
        elif text == "L":
            return self.l + g
        elif text == "G":
            return self.g

    # if `green_is_a_type`, return [0, 5]
    # if not `green_is_a_type`, return [0, 4]
    def GetTypeKindsInternal(self, green_is_a_type: bool) -> int:
        types = 0
        if self.r > 0:
            types += 1
        if self.b > 0:
            types += 1
        if self.y > 0:
            types += 1
        if self.l > 0:
            types += 1
        if green_is_a_type:
            types += self.g
            types = min(5, types)
        return types

    def IsSameType(self) -> bool:
        # Au plus UNE couleur non-joker presente.
        return sum(1 for color in [self.r, self.b, self.y, self.l] if color > 0) <= 1

    def IsDifferentType(self) -> int:
        types = self.GetTypeKindsInternal(False)
        if self.g:
            types += self.g
            types = min(4, types)
        return types

    def CanPayThisCost(self, cost: 'ResRBYGA') -> bool:
        if self.total == 0:
            return False
        if cost.rbyg.total == 0:
            return True
        else:
            return \
                cost.r > 0 and self.r > 0 or \
                cost.b > 0 and self.b > 0 or \
                cost.y > 0 and self.y > 0 or \
                cost.l > 0 and self.l > 0 or \
                self.g > 0 or \
                cost.a > 0
```

Dans `ResRBYGA`, après la propriété `g` :
```python
    @property
    def l(self) -> int:
        return self.rbyg.l
```

- [ ] **Step 5 : `resources.py`**

Ligne 12, `RES_TEXT` devient :
```python
    RES_TEXT: Final = {'r': Symbol.r_r_physical, 'g': Symbol.r_g_wild, 'b': Symbol.r_b_mental, 'y': Symbol.r_y_energy, 'l': Symbol.r_l_lightning}
```
⚠ Garder EXACTEMENT la forme `'l': Symbol.r_l_lightning` : `noms-ressources.test.ts` la relit par regex.

Ligne 13 :
```python
    RBYG_LIST: List[ResRBYG.RBYG] = ["R", "B", "Y", "G", "L"]
```
Dans le `Literal` du constructeur (lignes 17-24), ajouter `"L",` après `"G",` et `"LL",` après `"GG",`.

Dans `IsMatchCost`, après `check_value(self.rbyg.y - cost.rbyga.y)` :
```python
            check_value(self.rbyg.l - cost.rbyga.l)
```
Après la propriété `g` en fin de classe :
```python
    @property
    def l(self) -> int:
        return self.rbyg.l
```

- [ ] **Step 6 : `cost.py`**

Après la propriété `g` (ligne 126) :
```python
    @property
    def l(self) -> int:
        return self.rbyga.l
```
Dans `GetSpendText`, remplacer les deux lignes du bloc couleur :
```python
        if self.y + self.b + self.r + self.g + self.l:
            has_color = True
            texts.append(f"{'[[energy]]' * self.y}{'[[mental]]' * self.b}{'[[physical]]' * self.r}{'[[wild]]' * self.g}{'[[lightning]]' * self.l}")
```
Dans le `Literal` du constructeur de `Cost` (ligne 35-41), ajouter `"L", "LL", "YL",` avant `"0"`.

- [ ] **Step 7 : relancer le test, le voir vert**

```bash
cd "$W" && $PY tools/test_couleur_eclair.py
```
Attendu : tous `OK`, dernière ligne `OK : la cinquieme couleur est en place`.

- [ ] **Step 8 : témoin de non-régression immédiat**

```bash
cd "$W/src" && $PY -c "
from engine import Engine
from game.element.resources import Resources
from game.element.cost import Cost
assert Resources.FromText('G').IsMatchCost(Cost('Y'))
assert not Resources.FromText('Y').IsMatchCost(Cost('B'))
assert Resources.FromText('RBYG').GetResourceIconTypes() == 4
assert Resources.FromText('BB').rbyg.IsSameType()
assert Resources.FromText('RBY').rbyg.IsDifferentType() == 3
print('les quatre couleurs officielles n ont pas bouge')"
```
Attendu : la phrase finale, sans AssertionError. (Ce sont les valeurs mesurées AVANT le changement, le 11/09/2026.)

- [ ] **Step 9 : commit**

```bash
cd "/mnt/c/Users/arnau/Desktop/Marvel LCG" && git add Fusion/marvel-lcg-src/tools/test_couleur_eclair.py Fusion/marvel-lcg-src/src/game/element/rbyg.py Fusion/marvel-lcg-src/src/game/element/resources.py Fusion/marvel-lcg-src/src/game/element/cost.py Fusion/marvel-lcg-src/src/game/render/symbol.py
git commit -m "feat(moteur): une cinquieme couleur de ressource, l'eclair (L)

Champ l dans ResRBYG et toutes ses operations, RES_TEXT, RBYG_LIST,
IsMatchCost, GetSpendText, jeton [[lightning]]. Un joker vaut aussi un
eclair ; un eclair ne paie pas un cout type d'une autre couleur.
Test autonome tools/test_couleur_eclair.py, vu rouge puis vert."
```
(Ajouter les deux lignes d'attribution des Global Constraints.)

---

### Task 2 : les demandes au joueur, le compteur d'icônes, le cheat

**Files:**
- Modify: `Fusion/marvel-lcg-src/src/game/player/model/player_ask.py:17-32,126-136`
- Modify: `Fusion/marvel-lcg-src/src/game/operate/faces_counter.py:62-67`
- Modify: `Fusion/marvel-lcg-src/src/game/world/cheat/cheat_cmd_helper.py:393`
- Modify: `Fusion/marvel-lcg-src/tools/test_couleur_eclair.py`

**Interfaces:**
- Consumes: `Resources`, `Cost` de la Task 1.
- Produces: `PlayerAsk.DeclareResourceType(r, b, y, g, l=True)` ; `FacesCounter.GetPrintedResourcesCountInternal` rend une clé `"L"`.

- [ ] **Step 1 : étendre le test**

Dans `tools/test_couleur_eclair.py`, ajouter les imports après `Symbol` :
```python
from game.player.model.player_ask import PlayerAsk
from game.operate.faces_counter import FacesCounter
```
Et dans `main()`, avant `print()` final :
```python
    # Les demandes au joueur : on capture ce qui lui est propose.
    class Faux(PlayerAsk):
        def __init__(self):
            self.propositions = []
        def AskChooseOneText(self, item_list, text_list=None):
            self.propositions.append(list(item_list))
            return item_list[0]

    faux = Faux()
    faux.AskSpecifyResources(Resources.FromText("G"))
    cas("preciser un joker propose aussi `L`", "L" in faux.propositions[-1])
    faux.DeclareResourceType()
    cas("nommer un type propose `L` par defaut", "L" in faux.propositions[-1])
    faux.DeclareResourceType(l=False)
    cas("nommer un type sans `L` reste possible", "L" not in faux.propositions[-1])

    cas("le compteur d'icones imprimees a une case `L`",
        "L" in FacesCounter.GetPrintedResourcesCountInternal([]))
```

- [ ] **Step 2 : le voir échouer**

```bash
cd "$W" && $PY tools/test_couleur_eclair.py
```
Attendu : les quatre nouveaux cas `ECHEC` (ou `TypeError: ... unexpected keyword argument 'l'`).

- [ ] **Step 3 : `player_ask.py`**

`AskSpecifyResources` (lignes 17-32) devient :
```python
    def AskSpecifyResources(self, res: 'Resources') -> 'Resources':
        g = res.GetColor("G", convert_green_res=False)
        if g == 0:
            return res

        from itertools import combinations_with_replacement
        def generate_combinations(n: int):
            letters = ["R", "B", "Y", "L"]
            # Generate combinations with replacement
            combinations = combinations_with_replacement(letters, n)
            # Convert tuples to strings and return as a list
            return ["".join(comb) for comb in combinations]

        res_text = "R" * res.r + "B" * res.b + "Y" * res.y + "L" * res.l
        res_text += self.AskChooseOneText(generate_combinations(g))
        return Resources.FromText(res_text)
```
`DeclareResourceType` (lignes 126-136) devient :
```python
    def DeclareResourceType(self, r:bool=True, b:bool=True, y:bool=True, g:bool=True, l:bool=True) -> "Resources.RBYG":
        text: List["Resources.RBYG"] = []
        if r:
            text.append("R")
        if b:
            text.append("B")
        if y:
            text.append("Y")
        if l:
            text.append("L")
        if g:
            text.append("G")
        return self.AskChooseOneText(text)
```

- [ ] **Step 4 : `faces_counter.py`**

Le dictionnaire initial (lignes 62-67) devient :
```python
        return_res: Dict["Resources.RBYG", int] = {
            "R": 0,
            "B": 0,
            "Y": 0,
            "G": 0,
            "L": 0,
        }
```

- [ ] **Step 5 : `cheat_cmd_helper.py`**

Ligne 393 : `def Res(res: str = "RBYGL"):`

- [ ] **Step 6 : le voir vert**

```bash
cd "$W" && $PY tools/test_couleur_eclair.py
```
Attendu : tout `OK`.

- [ ] **Step 7 : commit**

```bash
cd "/mnt/c/Users/arnau/Desktop/Marvel LCG" && git add Fusion/marvel-lcg-src/tools/test_couleur_eclair.py Fusion/marvel-lcg-src/src/game/player/model/player_ask.py Fusion/marvel-lcg-src/src/game/operate/faces_counter.py Fusion/marvel-lcg-src/src/game/world/cheat/cheat_cmd_helper.py
git commit -m "feat(moteur): l'eclair dans les demandes au joueur, le compteur d'icones et le cheat"
```

---

### Task 3 : non-régression moteur sur de vraies parties

**Files:** aucun changement de code. Résultats consignés dans le message de commit de la Task 8.

⚠ Un seul harnais à la fois.

- [ ] **Step 1 : monter tous les decks de départ**

```bash
cd "$W" && $PY tools/verifier_tous_les_decks.py "$W/.game-src" 27000 /tmp/rapport-decks.json
```
Attendu : aucun deck en échec. Comparer le nombre de decks montés à celui du dernier rapport connu (`git log -p --all -S"rapport-decks" -- .planning | head`), il doit être identique.

- [ ] **Step 2 : les cas de capacités des packs qui lisent des couleurs**

```bash
cd "$W" && PARALLELES=4 $PY tools/test_capacites.py "$W/.game-src" 40000 /tmp/rapport-cap.json sw0
cd "$W" && PARALLELES=4 $PY tools/test_capacites.py "$W/.game-src" 40000 /tmp/rapport-cap.json sd0
cd "$W" && PARALLELES=4 $PY tools/test_capacites.py "$W/.game-src" 40000 /tmp/rapport-cap.json ra0
```
Attendu : mêmes totaux verts qu'avant (`spider_woman_kajislav` : 39/39 au 11/09/2026). Les packs `speed` (`sd0`) et `rainy` (`ra0`) lisent `GetColor` et `OnlyHasColor("Y")` : ils exercent exactement les fonctions modifiées.

- [ ] **Step 3 : parties jouées jusqu'au bout**

```bash
cd "$W" && $PY tools/autoplay.py "$W/.game-src" --deck spider_man --vilains rhino --profils equilibre --parties 8
```
Attendu : 0 traceback, rounds tenus proches de 7,5 (mesure du 11/09/2026, `84570d1b`). Un écart de plus d'un round est à expliquer avant de continuer.

- [ ] **Step 4 : la gate des refus**

```bash
cd "$W" && $PY tools/verifier_raisons_refus.py "$W/.game-src" 47000
```
Attendu : `OK`.

---

### Task 4 : le plateau rend l'éclair (`icones-ressources.tsx`, `board.css`)

**Files:**
- Modify: `ui-app/src/board/icones-ressources.tsx`
- Modify: `ui-app/src/board/board.css:2867-2870`
- Test: `ui-app/src/board/icones-ressources.test.tsx`

**Interfaces:**
- Produces: `Ressource.lettre` accepte `'L'`, `cle` accepte `'lightning'`, marqueur `⟦L⟧`, classe CSS `res-lightning`.

- [ ] **Step 1 : écrire le test qui échoue**

Ajouter dans `icones-ressources.test.tsx`, avant la fermeture du `describe` :
```tsx
  it("connait l'eclair, la ressource maison du pack Zeus (11/09/2026)", () => {
    expect(marquerRessources('Génère [[lightning]]')).toBe('Génère ⟦L⟧')
    expect(marquerRessources('a lightning resource')).toBe('a ⟦L⟧ resource')
    expect(coutEnIcones('YL')).toBe('⟦E⟧⟦L⟧')
    const { container } = render(<span>{avecIcones('Paie ⟦L⟧')}</span>)
    const icone = container.querySelector('i.icone-res.res-lightning')
    expect(icone).not.toBeNull()
    // Pas de glyphe d'eclair droit dans ChampionsIcons : c'est un SVG.
    expect(icone?.querySelector('svg')).not.toBeNull()
    expect(icone?.getAttribute('aria-label')).toBe('éclair')
    expect(container.textContent).toBe('Paie ')
  })
```

- [ ] **Step 2 : le voir échouer**

```bash
cd "$UI" && npx vitest run src/board/icones-ressources.test.tsx
```
Attendu : le nouveau cas échoue (`'Génère [[lightning]]'` inchangé).

- [ ] **Step 3 : `icones-ressources.tsx`**

Le type et la table deviennent :
```tsx
export type Ressource = {
  /** Lettre du moteur (`desc.RES`, couts types). */
  lettre: 'R' | 'B' | 'Y' | 'G' | 'L'
  /** Glyphe dans la police ChampionsIcons ; `L` n'y existe pas et se rend en SVG. */
  glyphe: 'P' | 'M' | 'E' | 'W' | 'L'
  /** Cle des jetons de narration (« [[physical]] »). */
  cle: 'physical' | 'mental' | 'energy' | 'wild' | 'lightning'
  nom: string
}

export const RESSOURCES: readonly Ressource[] = [
  { lettre: 'R', glyphe: 'P', cle: 'physical', nom: 'physique' },
  { lettre: 'B', glyphe: 'M', cle: 'mental', nom: 'mentale' },
  { lettre: 'Y', glyphe: 'E', cle: 'energy', nom: 'énergie' },
  { lettre: 'G', glyphe: 'W', cle: 'wild', nom: 'libre' },
  // L'eclair : ressource MAISON du pack Zeus (11/09/2026), cinquieme couleur
  // du moteur. Distincte de l'energie : un eclair ne paie pas un cout energie.
  { lettre: 'L', glyphe: 'L', cle: 'lightning', nom: 'éclair' },
]
```
Les deux regex :
```tsx
const JETONS = /\[\[(physical|mental|energy|wild|lightning)\]\]/g
const MOTS = /\b(physical|mental|energy|wild|lightning)(?= resources?\b)/gi
```
Dans `coutEnIcones` : `if (!/^[RBYGL]+$/i.test(cout)) return cout`.

`const MARQUEUR = /⟦([PMEWL])⟧/g`

Dans `avecIcones`, le bloc `if (ressource)` devient :
```tsx
    if (ressource) {
      morceaux.push(
        <i
          key={`icone-${rang}`}
          className={`icone-res res-${ressource.cle}`}
          role="img"
          aria-label={t(ressource.nom)}
          title={t(ressource.nom)}
        >
          {ressource.cle === 'lightning' ? <IconeEclair /> : ressource.glyphe}
        </i>
      )
    }
```
Et, au-dessus de `avecIcones`, le composant :
```tsx
/** Un eclair droit, comme sur les cartes de Zeus. `currentColor` suit `--res`. */
function IconeEclair() {
  return (
    <svg viewBox="0 0 24 24" aria-hidden="true" focusable="false">
      <path d="M13 2 4 14h6l-1 8 9-12h-6z" />
    </svg>
  )
}
```

- [ ] **Step 4 : `board.css`**

Après `.icone-res.res-wild { --res: #2ecc71; }` :
```css
  /* L'eclair (pack Zeus) : bleu electrique, pour ne pas se confondre avec
     l'energie jaune. Pas de glyphe dans la police : un SVG a la place. */
  .icone-res.res-lightning { --res: #5ec8ff; }
  .icone-res.res-lightning svg {
    width: 0.95em;
    height: 0.95em;
    vertical-align: -0.12em;
    fill: currentColor;
    stroke: color-mix(in srgb, var(--res) 55%, #000);
    stroke-width: 1.2;
    stroke-linejoin: round;
    paint-order: stroke fill;
  }
```

- [ ] **Step 5 : le voir vert, et le reste aussi**

```bash
cd "$UI" && npx vitest run src/board/icones-ressources.test.tsx src/board/icones-ressources-fr.test.ts
```
Attendu : tout vert.

- [ ] **Step 6 : commit**

```bash
cd "/mnt/c/Users/arnau/Desktop/Marvel LCG" && git add ui-app/src/board/icones-ressources.tsx ui-app/src/board/icones-ressources.test.tsx ui-app/src/board/board.css
git commit -m "feat(plateau): l'eclair, cinquieme ressource, rendu en SVG bleu electrique"
```

---

### Task 5 : le plateau nomme et paie l'éclair (`ask.ts`, refus, dictionnaires, gate)

**Files:**
- Modify: `ui-app/src/board/ask.ts:213-222,232,261,326`
- Modify: `ui-app/src/board/raisons-refus.ts:43-48`
- Modify: `ui-app/src/board/compteurs-fr.ts:29`
- Modify: `ui-app/src/board/dico-en.ts:815`
- Test: `ui-app/src/board/noms-ressources.test.ts`, `ui-app/src/board/paiement-type.test.ts`

**Interfaces:**
- Consumes: `Resources.RES_TEXT` du moteur (Task 1), relu par la gate.
- Produces: `NOM_TYPE.L === 'lightning'`.

- [ ] **Step 1 : la gate passe à cinq lettres, et on la voit rouge**

Dans `noms-ressources.test.ts`, les deux cas « en déclare bien quatre » deviennent :
```ts
  it('le moteur en déclare bien cinq (l’éclair depuis le 11/09/2026)', () => {
    expect(Object.keys(tableDuMoteur()).sort()).toEqual(['B', 'G', 'L', 'R', 'Y'])
  })

  it('le plateau en déclare bien cinq', () => {
    expect(Object.keys(tableDuPlateau()).sort()).toEqual(['B', 'G', 'L', 'R', 'Y'])
  })
```
Ajouter dans `paiement-type.test.ts`, dans le `describe('les autres formes de cout par types')` :
```ts
  it("exige une energie ET un eclair pour « YL » (Skyfather's Tempest, pack Zeus)", () => {
    const option = optionAvecCout('YL', [
      [1, 'Y'],
      [2, 'Y'],
      [3, 'L'],
      [4, 'G'],
    ])
    expect(reponsePrete(option, [], [1, 2]).prete).toBe(false)
    expect(reponsePrete(option, [], [1, 2]).raison).toMatch(/lightning|éclair/i)
    expect(reponsePrete(option, [], [1, 3]).prete).toBe(true)
    // Un joker vaut aussi un eclair.
    expect(reponsePrete(option, [], [1, 4]).prete).toBe(true)
  })
```
```bash
cd "$UI" && npx vitest run src/board/noms-ressources.test.ts src/board/paiement-type.test.ts
```
Attendu : « le plateau en déclare bien cinq » et « dit exactement la même chose » ROUGES (le moteur en a cinq depuis la Task 1, le plateau quatre), et le cas `YL` rouge.

- [ ] **Step 2 : `ask.ts`**

`NOM_TYPE` gagne, après `G: 'wild',` :
```ts
  L: 'lightning',
```
Les trois regex `/[rbyg]/gi` (dans `coutParType`, `typesManquants`, `valeurMoyen`) deviennent `/[rbygl]/gi`. Dans le commentaire de `valeurMoyen`, « R/B/Y/G » devient « R/B/Y/G/L ».

- [ ] **Step 3 : `raisons-refus.ts`**

Dans `ressourcesLisibles`, `NOMS` gagne `L: 'éclair',`.

- [ ] **Step 4 : dictionnaires**

`compteurs-fr.ts`, après `energy: 'énergie',` : `lightning: 'éclair',`.
`dico-en.ts`, après `joker: 'wild',` : `éclair: 'lightning',`.

- [ ] **Step 5 : tout le plateau vert**

```bash
cd "$UI" && npm run typecheck && npm test
```
Attendu : 0 erreur de type, tous les tests verts.

- [ ] **Step 6 : commit**

```bash
cd "/mnt/c/Users/arnau/Desktop/Marvel LCG" && git add ui-app/src/board/ask.ts ui-app/src/board/raisons-refus.ts ui-app/src/board/compteurs-fr.ts ui-app/src/board/dico-en.ts ui-app/src/board/noms-ressources.test.ts ui-app/src/board/paiement-type.test.ts
git commit -m "feat(plateau): l'eclair dans le paiement, les refus et les dictionnaires ; gate a cinq lettres"
```

---

### Task 6 : le deckbuilder

**Files:**
- Modify: `Fusion/marvel-lcg-src/public/js/marvel/lib.js:303`
- Modify: `Fusion/marvel-lcg-src/public/css/marvel/icon.css:120-123`

- [ ] **Step 1 : `lib.js`**

Ligne 303 : `const cardTypes = ["mental", "physical", "energy", "wild", "lightning", 'boost'];`

- [ ] **Step 2 : `icon.css`**

Après le bloc `.icon-energy:before` :
```css
/* L'eclair, ressource maison du pack Zeus (11/09/2026). Meme glyphe que
   l'energie, en bleu electrique : la police n'a pas d'eclair droit. */
.icon-lightning:before {
    content: "E";
    color: #2f8fd6
}
```

- [ ] **Step 3 : vérifier à l'œil**

Ouvrir `http://localhost:<port>/prepare.html` avec le moteur lancé, coller dans la console : `Lib.cleanResText("[[lightning]] et [[energy]]")` (ou la classe qui porte `cleanResText` si `Lib` n'est pas exposé). Attendu : deux `<span>`, `icon-lightning` et `icon-energy`.

- [ ] **Step 4 : commit**

```bash
cd "/mnt/c/Users/arnau/Desktop/Marvel LCG" && git add Fusion/marvel-lcg-src/public/js/marvel/lib.js Fusion/marvel-lcg-src/public/css/marvel/icon.css
git commit -m "feat(deckbuilder): le jeton [[lightning]] a son icone"
```

---

### Task 7 : la fiche de la ressource maison

**Files:**
- Create: `docs/reference/mots-cles/eclair.md`
- Modify: `docs/reference/mots-cles/README.md` (section `## Maison`)

- [ ] **Step 1 : écrire la fiche**

```markdown
# Éclair (ressource maison, `L`)

**Texte imprimé / définition** : le pack fan-made Zeus (Mozilla) imprime sur
ses quatre Thunder Strike une icône de ressource qui n'existe pas dans le jeu
officiel, un éclair droit. Ce n'est PAS l'énergie : Zeus exige de payer un
même événement « avec une énergie ET un éclair » (*Skyfather's Tempest*).
Vocabulaire fixé le 11/09/2026 : **énergie** = la ressource officielle jaune ;
**éclair** = celle-ci.

**Mécanisme moteur** : cinquième couleur à part entière, lettre `L`, ajoutée
le 11/09/2026 (`src/game/element/rbyg.py`, champ `l`). Elle se déclare comme
les autres : `"RES": "L"` dans `desc`, `Cost("YL")` pour un coût typé, jeton
`[[lightning]]` dans les narrations, `GetColor("L")` pour la compter.
- Un joker (`G`) vaut aussi un éclair (défaut `convert_green_res=True`).
- Un éclair paie tout coût générique, et ne paie PAS un coût typé d'une autre
  couleur : « Requirement (énergie) » le refuse.
- Plateau : `icones-ressources.tsx`, entrée `lightning`, rendue en SVG bleu
  électrique. Deckbuilder : classe `icon-lightning`.
- Gate : `ui-app/src/board/noms-ressources.test.ts` relit la table du moteur
  et celle du plateau et exige les cinq lettres des deux côtés.
- Test : `tools/test_couleur_eclair.py`.

**Carte exemple** : aucune livrée à ce jour ; le pack Zeus suivra
`PROCESSUS-HEROS.md`. Le relevé complet est dans
`.planning/todos/2026-09-11-zeus-releve-des-cartes.md`.

**Pièges connus** :
- **Ne pas lire l'éclair comme une énergie.** La première version du relevé
  Zeus l'a fait sur toutes les cartes ; le set némésis, lui, vise bien
  l'ÉNERGIE officielle, pas l'éclair.
- `DeclareResourceType()` propose désormais `L` à toute carte qui fait nommer
  un type (Psylocke, Iron Lad, Mojo). C'est la règle : un type existe pour
  tout le monde. Passer `l=False` si une carte doit s'en tenir aux quatre
  officiels.
- Les jetons à un crochet `[energy]` des textes français ne sont pas rendus
  en icône aujourd'hui (ils s'affichent tels quels) ; `[lightning]` suivra le
  même sort. Hors périmètre de la couleur.

**Variantes maison** : c'est la variante. Aucune autre ressource maison dans
le projet.
```

- [ ] **Step 2 : l'indexer**

Dans `README.md`, section `## Maison`, ajouter en tête de liste :
```markdown
- [x] eclair.md (pack `zeus` : une RESSOURCE maison, cinquième couleur du
      moteur `L`, ajoutée le 11/09/2026. ⚠ Distincte de l'énergie, que le set
      némésis vise, lui)
```

- [ ] **Step 3 : commit**

```bash
cd "/mnt/c/Users/arnau/Desktop/Marvel LCG" && git add docs/reference/mots-cles/eclair.md docs/reference/mots-cles/README.md
git commit -m "docs(mots-cles): fiche de l'eclair, la ressource maison du pack Zeus"
```

---

### Task 8 : construction du plateau et bilan

**Files:** aucun.

- [ ] **Step 1 : construire le plateau**

```bash
cd "$UI" && npm run build
```
Attendu : build vert. Ne PAS déployer : c'est la décision de l'utilisateur.

- [ ] **Step 2 : relire le relevé Zeus**

Dans `.planning/todos/2026-09-11-zeus-releve-des-cartes.md`, section « Ce qu'il faut avant de commencer », le point 2 (⛔ BLOQUANT) devient :
```markdown
2. ✅ **Fait le 11/09/2026** : l'éclair est une cinquième couleur du moteur,
   lettre `L`. Fiche `docs/reference/mots-cles/eclair.md`, spec et plan dans
   `docs/superpowers/`. Thunder Strike portera `"RES": "L"`.
```

- [ ] **Step 3 : commit final**

```bash
cd "/mnt/c/Users/arnau/Desktop/Marvel LCG" && git add .planning/todos/2026-09-11-zeus-releve-des-cartes.md
git commit -m "docs(zeus): la couleur eclair est en place, le pack peut commencer"
```

---

## Auto-revue

**Couverture de la spec.** Règles (joker, coût générique, coût typé) : Task 1. Moteur, fichier par fichier : Tasks 1 et 2 (les annotations `Resources.RBYG|None` suivent le `Literal` sans édition). Plateau : Tasks 4 et 5. Deckbuilder et `test_capacites` (qui lit `RES[0]` sans valider la lettre, donc rien à changer) : Task 6. Preuves 1 à 4 : Tasks 1, 3, 5, 8. Fiche maison exigée par `CLAUDE.md` : Task 7.

**Cohérence des noms.** `r_l_lightning`, `RBYG_LIST`, `NOM_TYPE.L`, `res-lightning`, `icon-lightning`, `[[lightning]]`, `⟦L⟧` : chacun apparaît avec la même graphie dans le test qui le lit.
