from . import *
from cards.pack.fne.campaign import CapacitesDeCampagne

# The Getaway 1A
# Setup: Place 1 speed counter here (2 counters instead in expert mode).
#   Attach the Out Front attachment (129A) to the villain.
# Modele : 60121a (WhenCardSetup du complot 1A), Find.FindAndAttachTo (60066)
# pour aller chercher Out Front dans la mise de cote du scenario.

def GetAbilities() -> Sequence['Ability']:

    def mise_en_place(effect: 'Effect', message: 'Message.WhenCardSetup') -> None:
        this = effect.this.CastTo(MainScheme)
        Faces.PlaceCountersOn([this], 2 if Worlds.IsExpert(effect) else 1, 'speed', effect)
        vilain = Worlds.FindVillain(effect)
        if vilain is not None:
            Find.FindAndAttachTo(effect, vilain, who_perform=Worlds.GetFirstPlayer(effect), name="Out Front", card_type=Attachment)

    return [
        AbilityFactory.WhenCardSetup("This", mise_en_place),
        # Mode campagne (livret p. 9 et encarts CAMPAIGN INSTRUCTIONS) : inerte
        # hors campagne (`Worlds.IsCampaign`), voir cards/pack/fne/campaign.py.
        *CapacitesDeCampagne("the_getaway"),
    ]
