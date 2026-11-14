from . import *

# Ground Stomp (variante Why Not) : 2 degats a chaque ennemi au lieu de 1.
# Modele 01022.


def GetAbilities() -> Sequence['Ability']:

    def ground_stomp(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        this.DealDamage(effect.targets, 2, effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            ground_stomp
        ).SetPlay().SetLabel()
        .SetTarget(Enemy, range="All"),
    ]
