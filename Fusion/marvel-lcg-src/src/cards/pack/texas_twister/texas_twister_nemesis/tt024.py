from . import *

# Soul Fragmentation — TRAITRISE NEMESIS, 1 boost. DEUX EXEMPLAIRES.
# When Revealed: Discard the top 3 cards of your deck. If [physical] resource
#   was discarded this way, you are stunned, if [mental] resource was
#   discarded this way, you are confused, if [wild] resource was discarded
#   this way, exhaust your identity.
#
# CARTE DE REFERENCE
#  - `40049` Probability Field : `FacesCounter.GetPrintedResourcesCount` pour
#    compter une couleur IMPRIMEE.
#
# ⚠ LA DEFAUSSE NE PEUT PAS ETRE UN COUT ICI, ET LE MOTEUR NE LE DIT PAS.
# Une premiere version copiait `40049` jusqu'au bout, avec
# `SetCostFunc(CostFunc.DiscardDeckTopCards("YourDeck", 3))` sur le
# `WhenThisRevealed`. Une carte de RENCONTRE n'a pas de joueur qui paie : le
# cout n'est jamais regle, l'operation n'est jamais appelee, et le journal ne
# montre qu'un banal « was revealed / were discarded ». Aucun statut, aucune
# erreur. On defausse donc a la main, dans l'operation, par
# `player_deck.GetTops(3)` (deck.py:404).
#
# TEXTE CONTRE CODE
#  ⚠ TROIS TESTS INDEPENDANTS, PAS UN CHOIX. Les trois clauses se cumulent :
#    trois cartes aux trois bonnes couleurs infligent Etourdi, Confus ET
#    l'inclinaison. Lire « ou » la ou la carte ecrit trois « if » diviserait
#    sa puissance par trois.
#  ⚠ L'ENERGIE [energy] N'EST PAS CITEE : c'est la seule couleur qui ne fait
#    rien, et c'est justement celle que Master Pandemonium reclame pour ne pas
#    activer. La carte pousse donc a garder ses energies, ce qui expose aux
#    trois autres couleurs. Ne PAS « completer » la liste par symetrie.
#  « was discarded THIS WAY » -> uniquement les trois cartes defaussees par
#    cette carte, pas la defausse entiere.
#  « EXHAUST your identity » et non « stun » : troisieme statut, troisieme
#    effet, tous distincts.


def GetAbilities() -> Sequence['Ability']:

    def fragmentation(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Treachery)
        Unused(this, message)
        joueur = Worlds.GetCurrentPlayer(effect)
        if joueur is None:
            return
        deck_du_joueur = joueur.player_deck
        faces = list(deck_du_joueur.GetTops(3))
        if faces:
            Faces.DiscardAll(faces, effect)
        identite = joueur.GetIdentity()
        if identite is None:
            return
        deck = deck_du_joueur
        if FacesCounter.GetPrintedResourcesCount(faces, "R", deck) > 0:
            Faces.GiveStatus([identite], "Stunned", effect)
        if FacesCounter.GetPrintedResourcesCount(faces, "B", deck) > 0:
            Faces.GiveStatus([identite], "Confused", effect)
        if FacesCounter.GetPrintedResourcesCount(faces, "G", deck) > 0:
            Faces.ExhaustAll([identite], effect)

    return [
        AbilityFactory.WhenThisRevealed(
            None,
            fragmentation,
        ),
    ]
