from . import *

# hs104 * Kraven The Hunter
# Forced Interrupt : quand un personnage que vous controlez l'attaque, distribue un piege et revele tous ceux distribues (limite 1 par ronde et par joueur).

def GetAbilities() -> Sequence['Ability']:
    return [PiegeSurAttaque(1, True)]
