from . import *

# * Ivan Banionis (CRIMINAL, TRACKSUIT) — Teamwork (TRACKSUIT) : base desc.
# When Revealed: Place 1 acceleration token here.
# [star] Forced Response: After Ivan Banionis schemes, place 1 acceleration
#   token here.
# PlaceAccelerationToken (50081 Abduct Superhumans).

def GetAbilities() -> Sequence['Ability']:

    def accelere(effect: 'Effect', message: 'Message') -> None:
        this = effect.this.CastTo(Minion)
        this.PlaceAccelerationToken(1, effect)

    return [
        AbilityFactory.WhenThisRevealed(None, accelere),
        AbilityFactory.AfterUnitSchemeEnd(AbilityType.ForcedResponse, "This", accelere),
    ]
