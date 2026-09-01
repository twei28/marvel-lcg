from . import *

# Mecha-Beast — amelioration Discovery (5/5). TECH. ARMOR. Cout 3.
# Attach to Beast.
# Beast gains +1 THW and +2 hitpoints.
#
# Carte de reference :
#  - an008 * Siri's Dress et ho011 * Goblin Glider : amelioration attachee a
#    SA PROPRE identite qui donne un bonus continu, rendue par
#    `GiveKeywordToAttached("You", ...)` (recette moteur §3). Comparable parce
#    que le bonus n'a ni declencheur ni duree : il vit tant que la carte est
#    en jeu, et disparait avec elle sans une ligne de plus.
#  - `AbilityFactory.CanPlayThisUpgradeCard()` sans argument : « attach to
#    Beast » = attacher a sa propre identite, exactement ho011.
#
# ⚠ « +2 hitpoints » se code `health=2`, PAS un soin : le maximum de PV monte
# de 2, les degats deja subis restent. `thwart=1` est bien le CTR (THW) et non
# le SCH : le mot imprime est THW, et le heros n'a pas de SCH.

def GetAbilities() -> Sequence['Ability']:

    return [
        AbilityFactory.CanPlayThisUpgradeCard(),
        *AbilityFactory.GiveKeywordToAttached(
            "You",
            thwart=1,
            health=2,
        ),
    ]
