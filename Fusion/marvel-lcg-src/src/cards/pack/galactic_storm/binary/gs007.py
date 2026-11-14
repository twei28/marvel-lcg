from . import *

# * Prophet-Singer — SOUTIEN, cout 0, [physical]. AERIAL. CREATURE. Binary 10/15.
# Action: Exhaust Prophet-Singer → look at the top card of your deck and swap
#   it with a card in your hand.
#
# Cartes de reference :
#  - **`next_evol/domino/40037a`** Domino : echanger une carte de la main avec
#    le dessus du deck = `Faces.SwapWithDeckTop([carte], deck, effect)`.
#  - **`core/01091`** Avengers Mansion : « Action: Exhaust X → ... » sur un
#    soutien = `WhenInYourPlayTurn(Action, op).SetCostFunc(CostFunc.Exhaust("This"))`.
#  - « look at the top card » : `joueur.LookAtDeck(deck, 1, effect)` (journal).
#
# ⚠ Mots-pieges (PROCESSUS-CARTE etape 5) :
#  - « LOOK at ... AND swap » : on regarde D'ABORD, puis on choisit la carte de
#    la main (le choix ne se fait pas avant d'avoir vu la carte, contrairement a
#    Domino qui cible a l'activation).
#  - « swap it with A card in your hand » : obligatoire, une seule carte ; la
#    carte de la main part SUR le deck (dessus), celle du dessus arrive en main.
#  - Deck vide ou main vide : rien a echanger, l'Action n'est pas proposee.
#  - « Action » nue : jouable en heros ET en alter ego.


def GetAbilities() -> Sequence['Ability']:

    def echange_possible(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> bool:
        Unused(message)
        joueur = JoueurDeCetteCarte(effect)
        return joueur is not None and joueur.player_deck.GetSize() > 0 and len(joueur.hand_cards.Get()) > 0

    def chant(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Support)
        Unused(this, message)

        joueur = JoueurDeCetteCarte(effect)
        if joueur is None:
            return
        dessus = joueur.LookAtDeck(joueur.player_deck, 1, effect)
        main = list(joueur.hand_cards.Get())
        if not dessus or not main:
            return
        carte = joueur.AskChooseFace(main, effect, prompt="Swap with the top card of your deck")
        if carte is not None:
            Faces.SwapWithDeckTop([carte], joueur.player_deck, effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.Action,
            chant,
            conditions=[echange_possible],
        ).SetCostFunc(CostFunc.Exhaust("This")),
    ]
