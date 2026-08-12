from . import *

# * Alias Investigations — custom « ekAugust »
# Action: Exhaust Alias Investigations -> discard cards from the top of the
#   encounter deck until you discard a side scheme. Reveal that side scheme.

def GetAbilities() -> Sequence['Ability']:

    def alias_investigations(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Support)
        Unused(this)

        initiator = effect.GetInitiator()
        face = Worlds.DiscardEncounterCardsUntil(
            effect,
            card_type=SchemeSide2,
        )
        if face:
            face.Reveal(initiator, effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.Action,
            alias_investigations,
        ).SetCostFunc(CostFunc.Exhaust("This")),
    ]
