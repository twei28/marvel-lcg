from . import *

# Sisterhood
# Action: Exhaust Sisterhood and discard a Wolverine card from your hand ->
#   search your deck and discard pile for Honey Badger and add her to your
#   hand. (Shuffle.)
#
# Copie de Sisterhood (43008), sans adaptation : `Search.PlayerCard` prend
# deja le joueur en parametre, et « discard a Wolverine card » se traduit par
# `card_class="IdentitySpecific"`, qui designe les cartes propres a TON
# identite quel que soit le nom du heros.


def GetAbilities() -> Sequence['Ability']:

    def sisterhood(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Support)
        Unused(this)

        initiator = effect.GetInitiator()
        face = Search.PlayerCard(
            effect,
            initiator,
            include_player_deck=True,
            include_discard_pile=True,
            name=NOM_SOEUR
        )
        if face:
            Faces.AddToHand([face], initiator, effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.Action,
            sisterhood
        ).SetCostFunc(CostFunc.Exhaust("This"))
        .SetCostFunc(CostFunc.Discard("YourHandCards", card_class="IdentitySpecific")),
    ]
