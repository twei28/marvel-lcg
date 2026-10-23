from . import *

# Flame Spout — TRAITRISE. TRAP! Boost 3.
# When Revealed : Choose :
#  • Avoid — Discard an ally from your hand.
#  • Disarm — Discard an ally you control, then draw 2 cards.
#  • Trip — Deal 3 damage to your identity. Discard the top 3 cards of your deck.
#
# Cartes de reference : sl050 (meme gabarit), core/black_panther/01045 (`DrawUp(2, effect)`), player_action.py `DiscardDeckTopCards`.
# ⚠ Mots-pieges : Avoid « from your HAND » (allie en main), Disarm « you CONTROL » (allie EN JEU) : deux zones differentes ; « then draw 2 » : seulement si l'allie a ete defausse ;
#  Trip : 3 degats a l'identite PUIS 3 cartes du dessus du deck defaussees (deux effets).


def GetAbilities() -> Sequence['Ability']:

    def revele(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        joueur = message.GetToPlayer()

        def evite() -> None:
            DefausserUneCarteDeLaMain(effect, joueur, AlliesDeLaMain(joueur))

        def desarme() -> None:
            if DefausserUneCarteEnJeu(effect, joueur, joueur.GetControlAllies()) is not None:
                joueur.DrawUp(2, effect)

        def declenche() -> None:
            DegatsEtStatut(effect, joueur, 3, None)
            joueur.DiscardDeckTopCards(3, effect)

        ChoixDePiege(effect, joueur,
                     OptionDePiege(effect, joueur, PIEGE_AVOID, "Discard an ally from your hand", evite, faisable=bool(AlliesDeLaMain(joueur))),
                     OptionDePiege(effect, joueur, PIEGE_DISARM, "Discard an ally you control, then draw 2 cards", desarme, faisable=bool(joueur.GetControlAllies())),
                     OptionDePiege(effect, joueur, PIEGE_TRIP, "Deal 3 damage to your identity. Discard the top 3 cards of your deck", declenche))

    return [
        AbilityFactory.WhenThisRevealed(None, revele),
    ]
