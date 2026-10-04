from . import *

# * Aunt May & Uncle Ben
# Action: Exhaust Aunt May & Uncle Ben and discard the top 2 cards of your
#   deck (top 3 cards instead if you are in alter-ego form) -> add each SP//dr
#   card discarded this way to your hand.
#
# ⚠ DECK PLUS COURT QUE LE COUT (signalements 21 et 22 de Yarro, 25/09/2026).
#   Le cout exigeait EXACTEMENT 2 (ou 3) cartes : avec 2 cartes en alter-ego,
#   l'Action n'etait jamais offerte. Arbitrage utilisateur du 25/09/2026 : elle
#   reste utilisable. On defausse ce qui reste ; le deck vide se remelange par
#   la regle generique (Rules Reference, Empty Player Deck : carte de rencontre,
#   et rien n'est defausse du nouveau deck).


def _a_defausser(effect: 'Effect') -> int:
    joueur = effect.GetInitiator()
    voulu = 3 if joueur.IsAlterEgo() else 2
    return max(1, min(voulu, joueur.player_deck.GetSize()))


def GetAbilities() -> Sequence['Ability']:

    def aunt_may_uncle_ben(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Support)
        Unused(this)

        initiator = effect.GetInitiator()

        faces = effect.cost_func.Get(CostFunc.Discard).return_discarded_cards
        faces = CardFinder(card_class="IdentitySpecific").Checks(faces)
        Faces.AddToHand(faces, initiator, effect)


    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.Action,
            aunt_may_uncle_ben,
        ).SetCostFunc(CostFunc.Exhaust("This"))
        .SetCostFunc(CostFunc.Discard("YourPlayerDeckTop", range=(
            _a_defausser,
            _a_defausser,
        ))),
    ]
