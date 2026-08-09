from . import *

# Repulsor Blasts

def GetAbilities() -> Sequence['Ability']:

    def repulsor_blasts(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(this)

        initiator = effect.GetInitiator()
        hero = initiator.GetHero()

        def tir(cibles: Sequence['CardFace']) -> None:
            hero.DealDamage(list(cibles), 2, effect,
                            property=AttackProperty(ranged=True))

        tir(effect.targets)

        # « Spend X [energy] resources (to a maximum of 3) -> repeat this attack
        # X times against targets of your choosing » : une repetition proposee a
        # la fois, chacune avec sa propre cible. ForChoiceAbilityWithCost rend le
        # choix refusable (forced=False dans ChooseAbilitiesHelper), et un refus
        # renvoie une liste vide -> on arrete.
        for _ in range(3):
            choix = initiator.ChooseAbilities(
                effect,
                AbilityFactory.ForChoiceAbilityWithCost(
                    Cost("Y"),
                    "Spend [energy] to repeat this attack",
                    lambda targets, res: tir(targets),
                ).SetLabel('attack')
                .SetTarget(Enemy),
            )
            if not choix:
                break

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            repulsor_blasts
        ).SetPlay().SetLabel('attack')
        .SetTarget(Enemy),
    ]
