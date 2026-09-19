from . import *

# * The Clown (ASSASSIN, TRACKSUIT) — Teamwork (TRACKSUIT), Villainous : bases.
# [star] Forced Response: After The Clown schemes, give him 1 facedown boost
#   card.  (Faces.GiveFacedownBoostCards, 55007b)

def GetAbilities() -> Sequence['Ability']:

    def apres_manigance(effect: 'Effect', message: 'Message.AfterUnitSchemeEnd') -> None:
        this = effect.this.CastTo(Minion)
        Faces.GiveFacedownBoostCards([this], 1, effect)

    return [
        AbilityFactory.AfterUnitSchemeEnd(AbilityType.ForcedResponse, "This", apres_manigance),
    ]
