from . import *
from game.card.face.attribute.can_boost import CanBoost

# * Betty Brant (DAILY BUGLE, PERSONA) — Uses (3 stamina) : base.
# Interrupt: When a boost card is turned faceup, exhaust Betty Brant and
#   remove 1 stamina counter from her -> cancel that card's boost icons and
#   "Boost" ability. Give the activating enemy another boost card for this
#   activation.
# WhenBoostCardWouldTurnedFaceUp + SetBeInstead : la carte DOIT quitter le
# paquet de boost (defausse), sinon boucle infinie (bc007 Misfortune) ; la
# carte de remplacement est posee face cachee (GiveFacedownBoostCardsInternal,
# 60072 Lady Bullseye).

def GetAbilities() -> Sequence['Ability']:

    def annule(effect: 'Effect', message: 'Message.WhenBoostCardWouldTurnedFaceUp') -> None:
        carte = message.trigger
        message.SetBeInstead(effect)
        if carte is not None:
            Faces.DiscardAll([carte], effect)
        ennemi = message.being_message.by_face if message.being_message is not None else None
        if ennemi is not None and CanBoost.IsType(ennemi):
            ennemi.GiveFacedownBoostCardsInternal(1, effect, message.would_message)

    a = AbilityFactory.WhenBoostCardWouldTurnedFaceUp(AbilityType.Interrupt, annule).SetName("Betty Brant: cancel this boost card, give another")
    for c in CoutDeReporter():
        a = a.SetCostFunc(c)
    return [a]
