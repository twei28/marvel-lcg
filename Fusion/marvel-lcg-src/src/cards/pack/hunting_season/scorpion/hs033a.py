from . import *

# hs033a Thirst for Revenge
from cards.pack.hunting_season.campaign import CampaignSetup

def GetAbilities() -> Sequence['Ability']:

    def mise_en_place(effect: 'Effect', message: 'Message.WhenCardSetup') -> None:
        MettreEnJeuLeSoutien(effect)
        for scorpion in Worlds.FindCardsOnField(effect, name="Scorpion"):
            AttacherLaQueue(effect, scorpion)
        effect.this.CastTo(MainScheme).Advance(None, effect)

    return [
        AbilityFactory.WhenCardSetup("This", mise_en_place),
        *CampaignSetup(2),
    ]
