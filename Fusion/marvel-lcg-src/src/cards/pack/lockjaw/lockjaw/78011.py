from . import *

# Ruff Ambush — custom « Nugget »
# Hero Response (attack): After you change to hero form, deal 5 damage to an
#   enemy (7 damage instead if you paid for this card using a [wild] resource).


def GetAbilities() -> Sequence['Ability']:

    def embuscade(effect: 'Effect', message: 'Message.AfterUnitChangeForm') -> None:
        this = effect.this.CastTo(Event)
        valeur = 7 if PayeAvecOs(effect) else 5
        this.DealDamage(effect.targets, valeur, effect)

    return [
        AbilityFactory.AfterUnitChangeForm(
            AbilityType.HeroResponse,
            "You",
            embuscade,
            to_form=Hero,
        ).SetPlay()
        .SetLabel('attack')
        .SetTarget(Enemy),
    ]
