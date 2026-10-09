from . import *

# Rats and More Rats 1B
# [star] Forced Response: After step one of the villain phase, place 1 threat on
# each RAT minion. Resolve the "Special" effect on Even More Rats.
# Modele : 04079b (AfterResolveVillainPhaseStep, etape 1).

def GetAbilities() -> Sequence['Ability']:

    def invasion(effect: 'Effect', message: 'Message.AfterResolveVillainPhaseStep') -> None:
        PlaceUneMenaceSurChaqueRat(effect)
        ResoudreSpecialEvenMoreRats(effect)

    return [
        AbilityFactory.AfterResolveVillainPhaseStep(
            AbilityType.ForcedResponse,
            1,
            invasion,
        ),
    ]
