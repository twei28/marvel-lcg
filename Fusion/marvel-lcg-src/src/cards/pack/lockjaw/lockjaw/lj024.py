from . import *

# Wet Slobbering Kiss — custom « Nugget » (carte d'aspect PROTECTION)
# Action: Choose one:
# - Heal 3 damage from a friendly character that is not your identity.
# - Deal 3 damage to an enemy.


def GetAbilities() -> Sequence['Ability']:

    def soigner(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        this.HealthUnits(effect.targets, 3, effect)

    def frapper(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        this.DealDamage(effect.targets, 3, effect)

    return [
        # « un personnage ami qui n'est pas votre identité » : les alliés.
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.Action,
            soigner,
        ).SetPlay()
        .SetTarget(Ally, canbe_heal=True),
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.Action,
            frapper,
        ).SetPlay()
        .SetTarget(Enemy),
    ]
