from . import *

# It's Clobberin' Time! — custom « DesignHacker »
# Hero Action: Make the following 2 attacks:
# - Deal 4 damage to an enemy.
# - Deal 4 damage to an enemy.

def GetAbilities() -> Sequence['Ability']:

    def clobberin_time(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(this)

        initiator = effect.GetInitiator()

        def une_attaque(targets: Sequence['CardFace']) -> None:
            this.DealDamage(targets, 4, effect)

        for _ in range(2):
            initiator.ChooseAbilities(
                effect,
                AbilityFactory.ForChoiceAbility(
                    "Deal 4 damage to an enemy",
                    une_attaque
                # CORRECTIF 4/8/2026 : `SetLabel` DOIT preceder `SetTarget`
                # (assertion dans ability.py). Dans l'autre ordre, la carte
                # levait une AssertionError et se defaussait sans rien faire,
                # a chaque utilisation depuis sa livraison.
                ).SetLabel('attack').SetTarget(Enemy),
            )

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            clobberin_time
        ).SetPlay().SetLabel('attack'),
    ]
