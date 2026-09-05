from . import *

# Unworthy — OBLIGATION. 2 icones de boost. Uses (2 unworthy counters).
#   Victory 0.
# Give to the Beta Ray Bill player.
# When Revealed: Find Stormbreaker and tuck it here. While it is tucked here,
#   Stormbreaker cannot be found.
# Forced Response: After you defeat an enemy or scheme, remove 1 unworthy
#   counter from here.
#
# ⚠ EMPLACEMENT DU MODULE : le bandeau dit « BETA RAY BILL », pas « ... 
# NEMESIS ». Son `set_name` est celui du set HEROS, le module vit donc ICI.
# Piege bt019 / nt012 / yd013 / dr010 / bk017 / tt020 — SEPTIEME fois, et la
# troisieme ou il est vu AVANT d'ecrire.
#
# ⚠ ET CE PACK N'A AUCUN SET NEMESIS : le zip s'arrete a cette obligation. Le
# deck de depart EMPRUNTE donc celui de Thor (06026-06030), calque de ce qui a
# ete fait pour hulk_rainy avec le Hulk officiel. Troisieme pack de Rainy dans
# ce cas, apres hulk_rainy et viv_vision.
#
# CARTE DE REFERENCE
#  - `51031` T'Challa's Shadow : LE jumeau structurel — une obligation a
#    compteurs (`desc.Uses`), `Victory 0`, qui retire un pion sur une Reponse
#    forcee. `Uses` est lu NATIVEMENT (Obligation herite de `HasUses`) : rien
#    a coder pour les 2 pions de depart.
#  - `ma004` / `27007` : la zone de cartes POSEES (`TuckCardUnderHere`).
#
# TEXTE CONTRE CODE
#  « FIND Stormbreaker and TUCK IT HERE » -> le marteau est confisque. C'est
#    la punition, et elle vise la carte autour de laquelle tout le pack tourne.
#  « While it is tucked here, Stormbreaker CANNOT BE FOUND » -> ⚠ AUCUN CODE
#    N'EST NECESSAIRE, et c'est verifie par un cas : une carte glissee sous
#    l'obligation n'est ni en jeu, ni dans le deck, ni en defausse. Les
#    fouilles de br001a, br005 et br012 elle-meme la manquent donc NATIVEMENT.
#  « After you defeat AN ENEMY OR SCHEME » -> les deux, d'ou deux fabriques.
#  ⚠ AUCUNE LIMITE : deux ennemis vaincus dans le meme round retirent bien
#    deux pions. C'est ce qui rend l'obligation surmontable.


def GetAbilities() -> Sequence['Ability']:

    def confisquer_le_marteau(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Obligation)
        joueur = message.GetGaveToPlayer() if hasattr(message, "GetGaveToPlayer") else None
        if joueur is None:
            joueur = Worlds.GetCurrentPlayer(effect)
        if joueur is None:
            return
        marteau = MarteauEnJeu(effect)
        if marteau is None:
            marteau = Search.PlayerCard(
                effect, joueur,
                include_player_deck=True,
                include_discard_pile=True,
                include_player_hand_cards=True,
                name=NOM_MARTEAU,
                card_type=Upgrade,
            )
        if marteau is not None:
            this.TuckCardUnderHere(marteau, effect)

    def retirer_un_pion(effect: 'Effect', message: 'Message2') -> None:
        this = effect.this.CastTo(Obligation)
        Unused(message)
        Faces.RemoveCountersOn([this], 1, COMPTEUR_INDIGNE, effect)

    return [
        AbilityFactory.WhenThisObligationGiveToYou(
            confisquer_le_marteau,
        ),
        AbilityFactory.AfterUnitBeDefeated(
            AbilityType.ForcedResponse,
            Enemy,
            retirer_un_pion,
        ),
        AbilityFactory.WhenSchemeBeDefeated(
            AbilityType.ForcedResponse,
            Scheme2,
            retirer_un_pion,
        ),
    ]
