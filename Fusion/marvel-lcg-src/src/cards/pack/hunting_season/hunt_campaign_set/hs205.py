from . import *

# hs205 * Lizard (sbire, ajoute au deck rencontre de Kraven si Lizard s'est echappe)
# Quickstrike, Retaliate 1 (donnees). Forced Interrupt : quand il attaque, l'attaque gagne piercing.

def GetAbilities() -> Sequence['Ability']:
    return [AbilityFactory.UnitAttackGainKeyword("This", piercing=True)]
