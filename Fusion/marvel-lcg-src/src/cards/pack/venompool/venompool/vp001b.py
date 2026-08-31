from . import *

# * Wade Wilson (face alter-ego)
# MUTANT.  REC 6* — HS 6 / PV 9
# [star] Wade Wilson can only use his REC when he has 3 or fewer hit points.
# Unexpected Bond - Action: Exhaust Wade Wilson -> search your deck and
#   discard pile for the Klyntar Suit upgrade and add it to your hand.
#   Shuffle your deck.
#
# Cartes de reference :
#  - REC conditionnel : `AbilityFactory.UnitCannotRecover("This", conditions=)`
#    (game/ability/factory/recovery.py), qui pose `SetCannotRecover` sur le
#    message `CheckIfUnitCanRecover` consulte par `CanRecover.IsCanRecover`.
#    On code la NEGATION du texte : interdit tant que les PV COURANTS sont
#    strictement superieurs a 3.
#  - Unexpected Bond : 04001b Clint Barton, mot pour mot le meme montage
#    (`Search.PlayerCard(include_player_deck=True, include_discard_pile=True,
#    name=..., card_type=Upgrade)` puis `initiator.GainCard(face, effect)`).
#    Le melange du deck est fait par Search.PlayerCard, comme pour l'arc de
#    Hawkeye.

SEUIL_RECUPERATION = 3


def GetAbilities() -> Sequence['Ability']:

    def peut_pas_recuperer(effect: 'Effect', message: 'Message.CheckIfUnitCanRecover') -> bool:
        this = effect.this
        return this.health > SEUIL_RECUPERATION

    def unexpected_bond(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(AlterEgo)
        Unused(this, message)

        initiator = effect.GetInitiator()
        face = Search.PlayerCard(
            effect,
            initiator,
            include_player_deck=True,
            include_discard_pile=True,
            name=KLYNTAR_SUIT_NAME,
            card_type=Upgrade,
        )
        if face:
            initiator.GainCard(face, effect)

    return [
        *AbilityFactory.UnitCannotRecover(
            "This",
            conditions=[peut_pas_recuperer],
        ),
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.Action,
            unexpected_bond,
        ).SetName("Unexpected Bond")
        .SetCostFunc(CostFunc.Exhaust("This")),
    ]
