from . import *

# Turned Around — TRAITRISE (×2). 1 icone de boost.
#
# When Revealed: You are confused. Then, choose an engaged minion, if able.
#   That enemy attacks you.
#
# ---------------------------------------------------------------------------
# CARTES DE REFERENCE
#
# - Poser un statut : `Faces.GiveStatus`, comme ih002.
# - « choose an engaged minion ... That enemy attacks you » : 01132 (Melter)
#   pour l'attaque d'un ennemi contre le joueur, et `player.MayChooseFace`
#   pour un choix parmi des cartes en jeu (modele sg013, cite dans le guide :
#   `SetTarget` ne restreint pas les cartes hors zone standard).
#
# ---------------------------------------------------------------------------
# TEXTE CONTRE CODE
#
# « You are confused » -> D'ABORD le statut, ENSUITE l'attaque : l'ordre
#   compte, un heros desoriente ne peut pas contrer mais peut encore defendre.
# « choose an ENGAGED minion » -> les sbires engages AVEC CE JOUEUR, pas tous
#   les sbires en jeu.
# « IF ABLE » -> aucun sbire engage : rien ne se passe, la carte s'arrete la.
# « THAT enemy attacks YOU » -> le sbire choisi attaque le joueur qui revele.


def GetAbilities() -> Sequence['Ability']:

    def desoriente_et_frappe(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Treachery)
        Unused(this)

        joueur = message.GetToPlayer()
        if not joueur:
            return

        identite = joueur.GetIdentity()
        if identite is not None:
            Faces.GiveStatus([identite], "Confused", effect)

        sbires = [f for f in joueur.engaged_minions.Get(True)]
        if not sbires:
            return

        choisi = joueur.MayChooseFace(sbires, effect)
        if choisi is not None:
            choisi.CastTo(Minion).DoAttackYou(joueur, effect)

    return [
        AbilityFactory.WhenThisRevealed(None, desoriente_et_frappe),
    ]
