from . import *

# Sabotage Sequence — custom « Kajislav »
# Hero Action (thwart): Remove 3 threat from a scheme. If this thwart removes
# the last threat from that scheme, resolve Albert's "Initiate Protocol"
# ability.

def GetAbilities() -> Sequence['Ability']:

    def sabotage_sequence(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(this)

        removed = this.RemoveThreatFromSchemes(effect.targets, 3, effect)
        Unused(removed)

        for target in effect.targets:
            scheme = target.CastTo(Scheme2)
            if scheme.threat == 0:
                ResolveInitiateProtocol(effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            sabotage_sequence
        ).SetPlay().SetLabel('thwart')
        .SetTarget(Scheme2),
    ]
