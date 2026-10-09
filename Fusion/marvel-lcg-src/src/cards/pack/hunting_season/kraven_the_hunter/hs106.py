from . import *

# hs106 * Kraven The Hunter
# When Revealed : chaque joueur se distribue un piege.
# Forced Interrupt : piege distribue et revele (limite 2 par ronde et par joueur).

def GetAbilities() -> Sequence['Ability']:
    return [AbilityFactory.WhenThisRevealed(None, DonnerPiegeATous), PiegeSurAttaque(2, True)]
