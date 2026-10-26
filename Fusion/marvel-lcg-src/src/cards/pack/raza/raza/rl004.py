from . import *
def GetAbilities() -> Sequence['Ability']:
    def boarding_action(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(message)
        this.RemoveThreatFromSchemes(effect.targets, 2 + len(CartesAvecTrait(effect, "TECH")), effect)
    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            boarding_action,
        ).SetPlay().SetLabel('thwart')
        .SetTarget(Scheme2),
    ]
