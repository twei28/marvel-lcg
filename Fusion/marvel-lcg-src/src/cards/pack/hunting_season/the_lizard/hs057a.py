from . import *

# hs057a Using the Mammal Brain
# Setup : mise en jeu de Reptilian Rage, le vilain commence cote Curtis Connors
# (premiere face de la pile), passage a 1B.
from cards.pack.hunting_season.campaign import CampaignSetup

def GetAbilities() -> Sequence['Ability']:

    def mise_en_place(effect: 'Effect', message: 'Message.WhenCardSetup') -> None:
        if Rage(effect) is None:
            Find.FindAndPutIntoPlay(
                effect, Worlds.GetFirstPlayer(effect),
                finder=CardFinder(name="Reptilian Rage", card_type=Environment,
                                  check_face_fn=lambda f: not f.IsInPlay()),
            )
        effect.this.CastTo(MainScheme).Advance(None, effect)

    return [
        AbilityFactory.WhenCardSetup("This", mise_en_place),
        *CampaignSetup(3),
    ]
