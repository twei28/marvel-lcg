from . import *

# * Kaine Parker (face alter-ego)
# Spider Link — Action: Discard 1 card from your hand -> search your
#   discard pile for 1 copy of Spider-pathy and add it to your hand. (Limit
#   once per round.)
#
# Modele : okoye/okoye/ok001b.py (Vanguard Leader/Marshalling Forces), meme
# couple `Search.PlayerCard(include_discard_pile=True, name=...)` +
# `initiator.GainCard(face, effect)`. Cout "discard 1 card from your hand" :
# modele `CostFunc.Discard("YourHandCards")` (aoa/45014.py).


def GetAbilities() -> Sequence['Ability']:

    def spider_link(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(AlterEgo)
        Unused(this)

        initiator = effect.GetInitiator()
        if initiator is None:
            return

        face = Search.PlayerCard(
            effect,
            initiator,
            include_player_deck=False,
            include_discard_pile=True,
            name="Spider-pathy",
        )
        if face:
            initiator.GainCard(face, effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.Action,
            spider_link,
        ).SetCostFunc(CostFunc.Discard("YourHandCards"))
        .SetName("Spider Link")
        .LimitOncePerRound(),
    ]
