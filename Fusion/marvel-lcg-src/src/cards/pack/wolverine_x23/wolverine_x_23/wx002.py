from . import *

# * Wolverine's Claws
# Permanent.
# Hero Action: Exhaust Wolverine's Claws and take 2 damage -> Wolverine gets
#   +2 ATK until the end of the round.
#
# Copie de X-23's Claws (43002). Le modele ciblait `name="X-23"` ; ici le nom
# ne suffit plus (cf. __init__.py), et « Wolverine » sur cette carte ne peut
# de toute facon designer que le porteur. On cible donc « YourIdentity », qui
# est le heros puisque c'est une Hero Action.


def GetAbilities() -> Sequence['Ability']:

    def wolverines_claws(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(this)

        for face in effect.targets:
            face.GainUntilRoundEnd(
                effect,
                attack=2
            )

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            wolverines_claws
        ).SetCostFunc(CostFunc.Exhaust("This"))
        .SetCostFunc(CostFunc.TakeDamage(2, "YourIdentity"))
        .SetTarget("YourIdentity"),
    ]
