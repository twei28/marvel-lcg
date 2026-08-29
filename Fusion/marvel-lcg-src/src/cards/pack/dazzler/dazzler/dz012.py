from . import *

# "Too Good to be True"
# SONG.
# Hero Action: Draw 3 cards. Choose and discard 1 card from your hand.
# Showtime!: Shuffle 3 cards from your discard pile into your deck.
#
# La defausse suit la pioche, elle ne peut donc PAS etre un cout : on peut
# tres bien defausser une des cartes qu'on vient de piocher. Elle se fait donc
# dans l'operation, apres le tirage.


def GetAbilities() -> Sequence['Ability']:

    def trop_beau(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(this)
        joueur = effect.GetInitiator()
        if joueur is None:
            return

        joueur.DrawUp(3, effect)

        main = [f for f in joueur.hand_cards.Get() if f is not None]
        if not main:
            return
        choisie = joueur.AskChooseOneText(main) if len(main) > 1 else main[0]
        if choisie is not None:
            Faces.DiscardAll([choisie], effect)

    def showtime(effect: 'Effect', message: 'Message2') -> None:
        this = effect.this.CastTo(Event)
        Unused(this)
        joueur = effect.GetInitiator()
        if joueur is None:
            return

        # « 3 cards from your discard pile » : on prend les 3 premieres si la
        # defausse en contient moins, on prend ce qu'il y a.
        defausse = [f for f in joueur.discard_pile.Get(True) if f is not None]
        if not defausse:
            return
        Faces.ShuffleAllTo(defausse[:3], joueur.player_deck, effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            trop_beau,
        ).SetPlay().SetLabel(),
        Showtime(showtime),
    ]
