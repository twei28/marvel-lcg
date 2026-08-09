from . import *

# Sock 'Em — custom « DesignHacker »
# Hero Action (attack): Deal 4 damage to an enemy. If that enemy is defeated
# by this attack, give The Thing a tough status card or draw a card.

def GetAbilities() -> Sequence['Ability']:

    def sock_em(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)

        def vaincu(unit: 'Unit2'):
            Unused(unit)

            initiator = effect.GetInitiator()
            hero = initiator.GetHero()

            initiator.ChooseAbilities(
                effect,
                AbilityFactory.ForChoiceAbility(
                    "Give The Thing a tough status card",
                    lambda targets: Faces.GiveStatus([hero], "Tough", effect),
                    condition=hero is not None,
                ),
                AbilityFactory.ForChoiceAbility(
                    "Draw a card",
                    lambda targets: initiator.DrawUp(1, effect)
                ),
            )

        this.DealDamage(effect.targets, 4, effect, if_this_attack_defeats=vaincu)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            sock_em
        ).SetPlay().SetLabel('attack')
        .SetTarget(Enemy),
    ]
