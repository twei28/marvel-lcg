"""La cinquieme couleur de ressource : l'eclair (`L`, lightning).

    $PY tools/test_couleur_eclair.py [game_dir]

Aucune partie, aucun port : on importe les briques de paiement et on les
interroge. Le test est AUTONOME et rapide (< 2 s).

Ce qu'il prouve, et pourquoi (spec du 11/09/2026,
docs/superpowers/specs/2026-09-11-cinquieme-couleur-de-ressource-design.md) :
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
from game.player.model.player_ask import PlayerAsk
from game.operate.faces_counter import FacesCounter

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
        "[[lightning]]" in Cost("L").GetSpendText())

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

    print()
    if ECHECS:
        print(f"ECHEC : {len(ECHECS)} cas rouge(s)")
        for nom in ECHECS:
            print("  - " + nom)
        sys.exit(1)
    print("OK : la cinquieme couleur est en place")


if __name__ == "__main__":
    main()
