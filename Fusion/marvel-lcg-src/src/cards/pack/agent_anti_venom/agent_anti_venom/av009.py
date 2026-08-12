from . import *

# Bear Arms — custom « DesignHacker »
# Hero Action: Exhaust Bear Arms -> Agent Anti-Venom's next attack gains
#   ranged.
# Hero Action (attack): Exhaust Bear Arms -> drain 1 from the villain.
#
# « next attack » : le moteur n'a pas de duree « prochaine attaque ». On pose
# donc une capacite temporaire UnitAttackGainKeyword sur l'identite, retiree
# des sa premiere execution. C'est la fabrique standard, donc "I've Got This!"
# voit ce ranged comme n'importe quel autre (voir le __init__.py du set).

def GetAbilities() -> Sequence['Ability']:

    def next_attack_ranged(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(this)

        identity = GetAgentAntiVenom(effect)
        if identity is None:
            return

        identity.effect.RegisterTemp(
            AbilityFactory.UnitAttackGainKeyword(
                "This",
                ranged=True,
            ).SetName("Bear Arms"),
            unregister_after_exec=True,
        )

    def bear_arms_drain(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Upgrade)
        Drain(this, effect.targets, 1, effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            next_attack_ranged,
        ).SetCostFunc(CostFunc.Exhaust("This")),

        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            bear_arms_drain,
        ).SetLabel('attack')
        .SetCostFunc(CostFunc.Exhaust("This"))
        .SetTarget(Villain),
    ]
