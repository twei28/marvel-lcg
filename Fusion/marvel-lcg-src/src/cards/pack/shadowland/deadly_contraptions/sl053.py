from . import *

# Oil Slick — TRAITRISE. TRAP! Boost 1.
# When Revealed : Choose :
#  • Avoid — Discard an upgrade from your hand.
#  • Disarm — Discard an upgrade you control, then remove 4 threat from the main scheme.
#  • Trip — Discard 1 card from your hand. Discard the top 8 cards of your deck.
#
# Cartes de reference : sl050 (meme gabarit), mister_fantastic/mf009 (`RemoveThreatFromSchemes("MainScheme", n, effect)`), `GetControlUpgrade` (player_get.py : ameliorations des
# allies comprises).
# ⚠ Mots-pieges : Avoid « from your hand » / Disarm « you control » (en jeu, y compris celles posees sur un allie) ; « remove 4 threat from the MAIN scheme » ; Trip : 1 carte de
#  la main AU CHOIX puis 8 cartes du dessus du deck (si la main est vide, seule la deuxieme partie a lieu).


def GetAbilities() -> Sequence['Ability']:

    def revele(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        joueur = message.GetToPlayer()
        this = effect.this

        def evite() -> None:
            DefausserUneCarteDeLaMain(effect, joueur, AmeliorationsDeLaMain(joueur))

        def desarme() -> None:
            if DefausserUneCarteEnJeu(effect, joueur, list(joueur.GetControlUpgrade())) is not None:
                this.RemoveThreatFromSchemes("MainScheme", 4, effect)

        def declenche() -> None:
            DefausserUneCarteDeLaMain(effect, joueur, joueur.hand_cards.Get())
            joueur.DiscardDeckTopCards(8, effect)

        ChoixDePiege(effect, joueur,
                     OptionDePiege(effect, joueur, PIEGE_AVOID, "Discard an upgrade from your hand", evite, faisable=bool(AmeliorationsDeLaMain(joueur))),
                     OptionDePiege(effect, joueur, PIEGE_DISARM, "Discard an upgrade you control, then remove 4 threat from the main scheme", desarme,
                                   faisable=bool(joueur.GetControlUpgrade())),
                     OptionDePiege(effect, joueur, PIEGE_TRIP, "Discard 1 card from your hand. Discard the top 8 cards of your deck", declenche))

    return [
        AbilityFactory.WhenThisRevealed(None, revele),
    ]
