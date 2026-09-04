from . import *

# * Pine Ridge Reservation — SOUTIEN, cout 2, [wild]. LOCATION.
# Drew Daniels gets +1 REC.
# Alter-Ego Action: Exhaust Pine Ridge Reservation -> return the top card of
#   your discard pile to your hand.
#
# CARTE DE REFERENCE
#  - `aa003` Ebony (pack agatha_harkness) : `GiveKeywordToInPlayWhenApplyThis(
#    Identity, control_by="You", recover=1)` PUIS une Alter-Ego Action a cout
#    d'inclinaison. Structure identique, ligne pour ligne.
#
# TEXTE CONTRE CODE
#  « DREW DANIELS gets +1 REC » -> le bonus est nomme sur l'ALTER-EGO. Le
#    moteur ne lit la REC que sur cette face, donner le bonus a `Identity`
#    entier est donc sans effet observable cote heros ; c'est l'idiome du
#    depot (`aa003`, `al011`) et il evite un filtre de face fragile.
#  « the TOP card of your discard pile » -> la DERNIERE defaussee,
#    `discard_pile.GetTop()` (deck.py:398, qui rend `self.cards[-1]`). Pas de
#    choix offert au joueur : la carte impose laquelle.
#  « to your HAND » -> `Faces.ReturnToHand`, et non un remelange : c'est le
#    contraste imprime avec tt001b Slowdown, qui remet dans le DECK.
#  « ALTER-EGO Action » -> recuperer coute un tour en forme civile, ce qui
#    est exactement ce que l'obligation tt020 cherche a rendre impossible.


def GetAbilities() -> Sequence['Ability']:

    def reprendre_la_derniere(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Support)
        Unused(this, message)
        joueur = JoueurDeCetteCarte(effect)
        if joueur is None:
            return
        face = joueur.discard_pile.GetTop()
        if face is not None:
            Faces.ReturnToHand([face], "Owner", effect)

    return [
        AbilityFactory.CanPlayThisSupportCard(),
        *AbilityFactory.GiveKeywordToInPlayWhenApplyThis(
            Identity,
            control_by="You",
            recover=1,
        ),
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.AlterEgoAction,
            reprendre_la_derniere,
        ).SetCostFunc(CostFunc.Exhaust("This")),
    ]
