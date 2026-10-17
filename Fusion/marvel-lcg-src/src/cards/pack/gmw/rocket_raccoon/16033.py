from . import *

# Salvage

def GetAbilities() -> Sequence['Ability']:

    def salvage(effect: 'Effect', message: 'Message.AfterCardsBeSpendAsResource') -> None:
        this = effect.this.CastTo(Resource)
        Unused(this)

        initiator = effect.GetInitiator()
        Faces.MoveAllToDeck(effect.targets, initiator.player_deck, "Top", effect)


    return [
        AbilityFactory.AfterYouSpendThisCard(
            AbilityType.Response,
            salvage
        # « a [tech] UPGRADE » : `card_type=Upgrade` (modele 54003, `SetTarget(trait=..., card_type=...,
        # from_where=["YourDiscardPile"])`). Sans lui, un soutien Tech (56012 Air Cover...) partait aussi
        # sur le deck (17/10/2026, relevé en traitant le rapport Yarro n85).
        ).SetTarget(trait="TECH", card_type=Upgrade, from_where=["YourDiscardPile"]),
    ]

