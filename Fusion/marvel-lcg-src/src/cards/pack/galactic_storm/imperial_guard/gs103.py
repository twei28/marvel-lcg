from . import *

# * Mentor — SBIRE (Imperial Guard). IMPERIAL GUARD. PV 4, MNG 3, ATQ 1. 1 icone(s) de boost.
# When Revealed: Discard a player side scheme from play. If you cannot, resolve the "Special" ability on the SETTING environment.
#
# Cartes de reference :
#  - « When Revealed ... If you cannot, resolve the "Special" ability on the SETTING environment » : `QuandRevele`
#    (imperial_guard/__init__.py, `WhenThisRevealed` + `ResolveSpecialAbility`, modele baxter_stockman `ResoudreLeSpecial`).
#  - « a player side scheme » : `Worlds.GetSideSchemes` filtre `PlayerSideScheme` (carte joueur du livret p.4, RECETTES).
#
# ⚠ Mots-pieges : « PLAYER side scheme » (pas une manigance annexe de rencontre) ; « from PLAY » ; le joueur qui revele choisit s'il y en a plusieurs ; defaussee, pas vaincue (aucune pile de victoire).


def GetAbilities() -> Sequence['Ability']:

    def effet_imprime(effect: 'Effect', joueur: 'Player') -> bool:
        candidates = [f for f in Worlds.GetAllSideSchemes(effect) if PlayerSideScheme.IsType(f) and f.IsInPlay()]
        return DefausserUneParmi(effect, joueur, candidates)

    return [
        QuandRevele(effet_imprime),
    ]
