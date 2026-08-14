from . import *

# * Doppelganger

def GetAbilities() -> Sequence['Ability']:

    def sortie(effect: 'Effect', message: 'Message.AfterCardLeavePlay') -> None:
        # « Response: After Doppelganger leaves play, search your deck and
        # discard pile for a SUPERPOWER card and add it to your hand. »
        ChercherEtPrendreEnMain(effect, effect.GetInitiator(), trait="SUPERPOWER")

    return [
        AbilityFactory.AfterCardLeavePlay(
            AbilityType.Response,
            "This",
            sortie
        ),
    ]
