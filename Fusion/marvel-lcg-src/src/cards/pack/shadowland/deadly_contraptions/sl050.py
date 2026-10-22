from . import *

# Blinding Powder — TRAITRISE. TRAP!
# When Revealed : Choose :
#  • Avoid — Discard a THWART event from your hand.
#  • Disarm — Discard 2 cards at random from your hand, then give a character you control a tough status card.
#  • Trip — Deal 2 damage to your identity and confuse it.
#
# Cartes de reference : hunting_season/trap/__init__ `PiegeAttachement` (`joueur.ChooseAbilities(effect, ForChoiceAbility(...), ...)` sur une revelation), shadows_in_the_night/sl004a
# (options payantes gardees par `PeutCouvrirLeCout`), player_action.py `DiscardRandomHandCards`, core/masters_of_evil/01131 (`Faces.GiveStatus`).
# ⚠ Mots-pieges : « Avoid » n'est offerte que si la main contient un evenement THWART (sinon elle serait gratuite) et jamais sous Iron Monk (sl047) ; « 2 cards AT RANDOM » :
#  au hasard (pas au choix) ; « THEN give a character YOU CONTROL » : identite ou allie du joueur, au choix ; « your identity » : l'identite du joueur qui revele ; Trip : toujours
#  possible ; les Forced Interrupt « When you choose the X effect » (sl046, sl048, sl049) passent avant chaque effet (`OptionDePiege`).


def GetAbilities() -> Sequence['Ability']:

    def revele(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        joueur = message.GetToPlayer()

        def evite() -> None:
            DefausserUneCarteDeLaMain(effect, joueur, EvenementsDeLaMain(joueur, "THWART"))

        def desarme() -> None:
            joueur.DiscardRandomHandCards(2, effect)
            cible = ChoisirUneCarte(effect, joueur, joueur.GetControlCharacters())
            if cible is not None:
                Faces.GiveStatus([cible], "Tough", effect)

        def declenche() -> None:
            DegatsEtStatut(effect, joueur, 2, "Confused")

        ChoixDePiege(effect, joueur,
                     OptionDePiege(effect, joueur, PIEGE_AVOID, "Discard a THWART event from your hand", evite, faisable=bool(EvenementsDeLaMain(joueur, "THWART"))),
                     OptionDePiege(effect, joueur, PIEGE_DISARM, "Discard 2 cards at random from your hand, then give a character you control a tough status card", desarme,
                                   faisable=len(joueur.hand_cards.Get()) >= 2),
                     OptionDePiege(effect, joueur, PIEGE_TRIP, "Deal 2 damage to your identity and confuse it", declenche))

    return [
        AbilityFactory.WhenThisRevealed(None, revele),
    ]
