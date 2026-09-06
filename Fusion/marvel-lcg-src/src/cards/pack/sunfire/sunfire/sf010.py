from . import *

# Shame — OBLIGATION. 2 icones de boost.
# Give to the Shiro Yoshida player.
# You get -1 hand size. The number of cards in your hand cannot exceed your
#   hand size (discard down to your hand size after drawing any cards).
# Alter-Ego Action: Exhaust Shiro Yoshida and discard 1 card from your hand ->
#   remove Shame from the game.
#
# ⚠ EMPLACEMENT DU MODULE : le bandeau imprime dit « SUNFIRE », pas
# « ... NEMESIS ». Son `set_name` est celui du set HEROS, le module vit donc
# ICI. Piege bt019 / nt012 / yd013 / dr010 / bk017 / tt020 / br012 / tg011 /
# sn011 / bc012 — ONZIEME fois, et la septieme ou il est vu AVANT d'ecrire.
#
# ⚠ OBLIGATION QUI RESTE EN JEU, ce qui n'est pas le cas general : la plupart
# se defaussent en se resolvant. Celle-ci a une Action pour s'en debarrasser,
# donc elle demeure. Modele exact : `04165` Martial Law (« Your hand size is
# reduced by 1. Alter-Ego Action: ... -> discard this card »), plus `04166`
# Anti-Hero Propaganda pour la forme du couple bonus continu / action de
# retrait.
#
# TEXTE CONTRE CODE
#  ⚠ « YOU get -1 hand size » -> le litteral `"You"`, donc l'IDENTITE, les
#    deux faces. `04165` ecrit exactement cela.
#  ⚠ « REMOVE Shame FROM THE GAME » et non « discard » : c'est
#    `PlayerActionToRemoveThisFromGame`, pas `PlayerActionToDiscardThis`. La
#    difference est reelle — une obligation defaussee revient dans le deck de
#    rencontre du joueur, une obligation retiree du jeu ne revient jamais.
#    `04165` dit « discard », celle-ci dit « remove » : ne pas recopier la
#    carte modele sans la relire.
#  ⚠ DEUX COUTS : incliner Shiro Yoshida ET defausser 1 carte de la main.
#    « Exhaust SHIRO YOSHIDA » nomme la face ALTER-EGO, ce que garantit deja
#    `AlterEgoAction` ; on vise donc l'identite, qui EST cette face-la.
#  ⚠ « The number of cards in your hand CANNOT EXCEED your hand size » -> cette
#    phrase n'a AUCUN equivalent au depot (verifie sur les 5933 cartes). Elle
#    est rendue par une Reponse forcee sur `Message.AfterCardsMoved`, filtree
#    sur la MAIN du joueur. ⚠ Ce n'est PAS un choix par defaut : le moteur n'a
#    AUCUN message « apres avoir pioche » (seul `WhenPlayerWouldDrawCard`
#    existe, et il part AVANT la pioche, quand la main n'est pas encore trop
#    pleine). `AfterCardsMoved` est le seul message qui parte quand une carte
#    ENTRE dans une zone — c'est celui qu'ecoute `OnEvent.TuckUnder`
#    (on_event.py:410-423), et le meme montage que la regle des 3 cartes de
#    `bc001a`. Il couvre en prime toutes les autres facons de remplir sa main,
#    ce que « any cards » demande.
#  ⚠ PAS DE BOUCLE INFINIE : la defausse fait repartir le message, mais le
#    surplus vaut alors zero et l'operation sort aussitot.


def GetAbilities() -> Sequence['Ability']:

    def la_main_a_bouge(effect: 'Effect', message: 'Message.AfterCardsMoved') -> bool:
        joueur = JoueurDeCetteCarte(effect)
        if joueur is None:
            return False
        return joueur.hand_cards in message.related_decks

    def main_trop_pleine(effect: 'Effect', message: 'Message.AfterCardsMoved') -> None:
        this = effect.this.CastTo(Obligation)
        Unused(this, message)

        joueur = JoueurDeCetteCarte(effect)
        if joueur is None:
            return
        identite = joueur.GetIdentity()
        if identite is None:
            return
        main = list(joueur.hand_cards.Get())
        trop = len(main) - identite.hand_size
        if trop <= 0:
            return
        choisies = joueur.AskChooseFaces(
            main, (trop, trop), effect,
            prompt="Discard down to your hand size")
        if choisies:
            Faces.DiscardAll(list(choisies), effect)

    return [
        *AbilityFactory.GiveKeywordToInPlayWhenApplyThis(
            "You",
            hand_size=-1,
        ),
        # « (discard down to your hand size AFTER DRAWING any cards) »
        AbilityFactory.AfterCardsMoved(
            AbilityType.ForcedResponse,
            None,
            main_trop_pleine,
            conditions=[la_main_a_bouge],
        ),
        AbilityFactory.PlayerActionToRemoveThisFromGame(
            AbilityType.AlterEgoAction,
        ).SetCostFunc(CostFunc.Exhaust("YourIdentity"))
        .SetCostFunc(CostFunc.Discard("YourHandCards", range=(1, 1))),
    ]
