from . import *

# Boa Constricted

def GetAbilities() -> Sequence['Ability']:

    def defausser(effect: 'Effect', message: 'Message.WhenPhaseEnd') -> None:
        Faces.DiscardAll([effect.this], effect)

    return [
        AbilityFactory.AttachToFaceWhenPutIntoPlay("YourIdentity"),
        AbilityFactory.WhenPhaseEnd(AbilityType.ForcedInterrupt, "Player", defausser),
    ]
