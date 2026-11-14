from . import *
def GetAbilities() -> Sequence['Ability']:
    def breach_their_defenses(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(message)
        this.DealDamage(effect.targets, 3 + len(CartesAvecTrait(effect, "WEAPON")), effect)
    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            breach_their_defenses,
        ).SetPlay().SetLabel('attack')
        .SetTarget(Enemy),
    ]
