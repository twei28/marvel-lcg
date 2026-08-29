from . import *

# * Laura Kinney
# Shhnk! — Setup: Put Wolverine's Claws into play.
# Action: Shuffle either the Honey Badger ally or the Sisterly Bond event
#   from your discard pile into your deck -> draw 1 card.
#   (Limit once per round.)
#
# Copie de Laura Kinney (43001b), avec wx002 a la place de 43002.
# Le cout pioche dans `YourDiscardPile` : deja borne au joueur, donc les noms
# « Honey Badger » et « Sisterly Bond » ne peuvent pas partir chez le voisin.


def GetAbilities() -> Sequence['Ability']:

    def laura_kinney_shuffle(targets: Sequence['CardFace'], effect: 'Effect') -> bool:
        this = effect.this.CastTo(AlterEgo)
        Unused(this)

        initiator = effect.GetInitiator()
        return Faces.ShuffleAllTo(targets, initiator.player_deck, effect) == targets

    def laura_kinney(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(AlterEgo)
        Unused(this)

        initiator = effect.GetInitiator()

        initiator.DrawUp(1, effect)

    return [
        AbilityFactory.SetupPutIntoPlay(
            ["wx002"],
        ).SetName("Shhnk!"),
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.Action,
            laura_kinney,
        ).SetCostFunc(CostFunc.Custom(
            Select.From(
                CardFinder(name=NOM_SOEUR, card_type=Ally)|
                CardFinder(name="Sisterly Bond", card_type=Event),
                from_where=["YourDiscardPile"]
            ),
            laura_kinney_shuffle))
        .LimitOncePerRound(),
    ]
