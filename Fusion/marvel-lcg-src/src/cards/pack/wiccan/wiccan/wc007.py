from . import *

# Magic Bolt (3/3) — exemplaire physique 3/3, contenu identique a wc005
# (voir ce fichier pour le detail des modeles et des arbitrages).


def GetAbilities() -> Sequence['Ability']:

    def magic_bolt(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(message)

        initiator = effect.GetInitiator()
        this.DealDamage(effect.targets, 3, effect)

        icones = IconesBoostDuDessus(effect, initiator)
        if initiator is None:
            return

        if icones <= 1:
            initiator.DrawUp(1, effect)
        else:
            initiator.ChooseAbilities(
                effect,
                AbilityFactory.ForChoiceAbility(
                    "Deal 3 damage to an enemy (this attack gains ranged)",
                    lambda targets:
                        this.DealDamage(targets, 3, effect,
                                        property=AttackProperty(ranged=True)),
                ).SetTarget(Enemy),
            )

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            magic_bolt,
        ).SetPlay().SetLabel('attack')
        .SetTarget(Enemy),
    ]
