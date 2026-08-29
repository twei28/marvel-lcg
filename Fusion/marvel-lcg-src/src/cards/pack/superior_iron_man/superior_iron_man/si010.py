from . import *

# Endo-Sym Spare
#
# "search discard pile for X and shuffle it into your deck" : modele James
# Rhodes (warm/23001b.py) : `.SetTarget(name=..., from_where=["YourDiscardPile"])`
# + `Faces.ShuffleAllTo(effect.targets, initiator.player_deck, effect)`.

def GetAbilities() -> Sequence['Ability']:

    def endo_sym_spare(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(this)
        initiator = effect.GetInitiator()
        Faces.ShuffleAllTo(effect.targets, initiator.player_deck, effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.AlterEgoAction,
            endo_sym_spare,
        ).SetCostFunc(CostFunc.Exhaust("This"))
        .SetTarget(name="Endo-Sym Matter", from_where=["YourDiscardPile"]),
    ]
