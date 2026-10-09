from . import *

# hs107a Acquiring Targets
# Setup : tous les TRAP forment un paquet Trap a part, puis on avance a 1B (automatique, sans TargetThreat).

from cards.pack.hunting_season.campaign import CampaignSetup

def GetAbilities() -> Sequence['Ability']:

    def mise_en_place(effect: 'Effect', message: 'Message.WhenCardSetup') -> None:
        CreerPaquetsPiege(effect)

    return [AbilityFactory.WhenCardSetup("This", mise_en_place), *CampaignSetup(5)]
