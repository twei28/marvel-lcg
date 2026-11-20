from . import *

# * Magique — SBIRE (Imperial Guard). IMPERIAL GUARD. SHI'AR. PV 4, MNG 2, ATQ 2. 1 icone(s) de boost.
# When Revealed: Give the villain a tough status card. If you cannot, resolve the "Special" ability on the SETTING environment.
#
# Cartes de reference :
#  - « When Revealed ... If you cannot, resolve the "Special" ability on the SETTING environment » : `QuandRevele`
#    (imperial_guard/__init__.py, `WhenThisRevealed` + `ResolveSpecialAbility`, modele baxter_stockman `ResoudreLeSpecial`).
#  - « Give the villain a tough status card » : `Faces.GiveStatus([mechant], "Tough", effect)` (modele gs135 / sk151).
#
# ⚠ Mots-pieges : « THE villain » ; « If you CANNOT » = le mechant a deja une carte Tough (maximum 1) : Special.


def GetAbilities() -> Sequence['Ability']:

    def effet_imprime(effect: 'Effect', joueur: 'Player') -> bool:
        mechant = Worlds.FindVillain(effect)
        return mechant is not None and bool(Faces.GiveStatus([mechant], "Tough", effect))

    return [
        QuandRevele(effet_imprime),
    ]
