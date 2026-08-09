from . import *

# Web of Fate — custom « Kajislav »
# Response: After you spend this card, look at the top 5 cards of your deck.
#   Add 1 of those to your hand and put the rest back in the same order.
#
# LookAtDeck ne DEPLACE pas les cartes : celles qu'on ne prend pas restent en
# place, donc « dans le meme ordre » est acquis sans manipulation. Meme
# montage qu'Agatha Harkness (15007), qui repose la fin du paquet au fond parce
# que SA carte le demande — pas la notre.

def GetAbilities() -> Sequence['Ability']:

    def toile_du_destin(effect: 'Effect', message: 'Message.AfterCardsBeSpendAsResource') -> None:
        this = effect.this.CastTo(Resource)
        Unused(this)

        initiator = effect.GetInitiator()
        faces = initiator.LookAtDeck(initiator.player_deck, 5, effect)
        if not faces:
            return

        face = initiator.AskChooseFace(faces, effect)
        if face:
            initiator.GainCard(face, effect)

    return [
        AbilityFactory.AfterYouSpendThisCard(
            AbilityType.Response,
            toile_du_destin
        ),
    ]
