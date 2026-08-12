from . import *

# * Throg — custom « Nugget » (carte d'aspect JUSTICE)
# Companion.
# Action: Spend an [energy] resource and exhaust Throg → remove 1 threat from
#   each scheme. Deal 1 damage to Throg.


def GetAbilities() -> Sequence['Ability']:

    def coup_de_marteau(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Ally)
        schemes = Worlds.FindCardsOnField(effect, card_type=Scheme2)
        if schemes:
            this.RemoveThreatFromSchemes(schemes, 1, effect)
        this.TakeDamage(this, 1, effect)

    return [
        *Companion(),
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.Action,
            coup_de_marteau,
        ).SetName("Throg")
        .SetCost(Cost("Y"))
        .SetCostFunc(CostFunc.Exhaust("This")),
    ]
