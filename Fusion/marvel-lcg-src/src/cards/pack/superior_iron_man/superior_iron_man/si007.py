from . import *

# * Pepper Potts
#
# "ignoring its crisis icon" = `RemoveThreatFromSchemes(..., ignore_crisis=True)`,
# voir docs/reference/mots-cles/crisis.md.

def GetAbilities() -> Sequence['Ability']:

    def pepper_potts(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Support)
        this.RemoveThreatFromSchemes(effect.targets, 1, effect, ignore_crisis=True)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.Action,
            pepper_potts,
        ).SetTarget(Scheme2, has_threat=True)
        .SetCostFunc(CostFunc.Exhaust("This")),
    ]
