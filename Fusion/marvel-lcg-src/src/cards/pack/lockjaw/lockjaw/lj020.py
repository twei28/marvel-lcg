from . import *

# * Redwing — custom « Nugget » (carte d'aspect LEADERSHIP)
# Companion.
# Hero Action: Exhaust Redwing and deal 1 damage to him → look at the top card
#   of the encounter deck.


def GetAbilities() -> Sequence['Ability']:

    def repérer(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Ally)
        initiator = effect.GetInitiator()
        this.TakeDamage(this, 1, effect)
        initiator.LookAtDeck("EncounterDeck", 1, effect)

    return [
        *Companion(),
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            repérer,
        ).SetName("Redwing")
        .SetCostFunc(CostFunc.Exhaust("This")),
    ]
