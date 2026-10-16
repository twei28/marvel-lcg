from . import *

# Quantanucleic Acid — EVENEMENT, cout 1, [wild]. QUANTA. x1.
# Hero Action: Give Venus a tough status card. You may remove 2 dredge counters from
#   Venus to draw 2 cards.
#
# CARTES DE REFERENCE
#  - `19001a` / `tg010` : `Faces.GiveStatus([...], "Tough", effect)`.
#  - `tv004` (meme pack) : choix facultatif a cout en compteurs (`ProposerRetraitDragage`).
#
# TEXTE CONTRE CODE
#  ⚠ « Give VENUS a tough status card » -> l'IDENTITE (une Hero Action ne se joue qu'en forme
#    heros : c'est Venus). Un heros deja Tough n'en recoit pas de seconde (`tough_max`).
#  ⚠ « You MAY remove 2 dredge counters ... to draw 2 cards » : facultatif, independant du
#    statut donne ; le retrait est le cout.
#  Aucun libelle (`SetLabel()` vide) : ni attaque, ni contre, ni defense.


def GetAbilities() -> Sequence['Ability']:

    def acide(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(this, message)
        joueur = JoueurDeCetteCarte(effect)
        identite = IdentiteDuJoueur(effect, joueur)
        if identite is not None:
            Faces.GiveStatus([identite], "Tough", effect)
        ProposerRetraitDragage(
            effect, joueur, 2,
            "Remove 2 dredge counters to draw 2 cards",
            lambda cibles: joueur.DrawUp(2, effect))

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            acide,
        ).SetPlay().SetLabel(),
    ]
