from . import *
# * Helek (Justice, soutien 2 [mental]). KREE. PERSONA.
# Reduce the cost to play Helek by 2 if your identity has the STARJAMMER trait.
# Response: After a player reveals a treachery card, exhaust Helek → that player draws a card.
#
# Cartes de reference : `ReduceCostToPlayThis(N, your_identity_has_traits=[..])` (resources.py:657) ; 45049 Stepford Cuckoos
# (« a player reveals a treachery », `AfterPlayerRevealCard(.., "AnyPlayer", Treachery, op)`) ; as022 (`CanPlayThisSupportCard`).
# « that player draws » : le joueur qui a REVELE (`message.to_player`), pas forcement le proprietaire de Helek. Reduction : « your identity
# has STARJAMMER » (Honorary / Captain l'accordent aussi). Cout de base 2 : gratuit pour un STARJAMMER.
def GetAbilities() -> Sequence['Ability']:
    def helek(effect: 'Effect', message: 'Message.AfterCardRevealedEnd') -> None:
        joueur = message.to_player
        if joueur is not None:
            joueur.DrawUp(1, effect)
    return [
        AbilityFactory.CanPlayThisSupportCard(),
        AbilityFactory.ReduceCostToPlayThis(2, your_identity_has_traits=["STARJAMMER"]),
        AbilityFactory.AfterPlayerRevealCard(
            AbilityType.Response,
            "AnyPlayer",
            Treachery,
            helek,
        ).SetCostFunc(CostFunc.Exhaust("This")),
    ]
