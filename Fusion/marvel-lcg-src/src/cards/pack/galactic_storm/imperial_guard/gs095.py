from . import *

# * Earthquake — SBIRE (Imperial Guard). IMPERIAL GUARD. PV 5, MNG 1, ATQ 2. 2 icone(s) de boost.
# When Revealed: Exhaust your identity. If you were already exhausted, resolve the "Special" ability on the SETTING environment.
#
# Cartes de reference :
#  - « When Revealed ... If you cannot, resolve the "Special" ability on the SETTING environment » : `QuandRevele`
#    (imperial_guard/__init__.py, `WhenThisRevealed` + `ResolveSpecialAbility`, modele baxter_stockman `ResoudreLeSpecial`).
#  - « Exhaust your identity » : `Faces.ExhaustAll([identite], effect)` (modele gs301 / `Puzzle.Exhaust`).
#
# ⚠ Mots-pieges : « If you WERE ALREADY exhausted » : l'etat est lu AVANT, une identite deja inclinee ne declenche pas d'autre effet que le Special ; « your IDENTITY » (alter ego compris).


def GetAbilities() -> Sequence['Ability']:

    def effet_imprime(effect: 'Effect', joueur: 'Player') -> bool:
        identite = joueur.GetIdentity()
        if identite.IsExhaust():
            return False
        Faces.ExhaustAll([identite], effect)
        return True

    return [
        QuandRevele(effet_imprime),
    ]
