from . import *

# Burning — AMELIORATION, aucun cout, aucune icone de ressource.
#   CONDITION. FIRE. SIX exemplaires, MIS DE COTE a la mise en place.
# Permanent.
# Forced Response: After the player phase ends, deal 1 damage to attached
#   enemy. Set this card aside.
# Forced Response: After attached enemy leaves play, set this card aside.
#
# ⚠⚠ LA CARTE QUI PORTE TOUT LE PACK, ET LA BRIQUE 6 DU PLAN DE PORTAGE : une
# amelioration JOUEUR attachee a un ENNEMI. Huit cartes sur seize la posent, la
# lisent ou la recyclent. Elle n'est JAMAIS jouee depuis la main : elle vit
# dans la reserve et fait des allers-retours.
#
# ⚠⚠ « PERMANENT » N'EST PAS UN OBSTACLE, C'EST LE MECANISME.
# `HasPermanent.OnWhenCardLeavePlay` (has_permanent.py:34) refuse la sortie de
# jeu d'une carte Permanente **SAUF si l'effet qui la sort vient du MEME
# `set_name`**. Burning porte `set_name = "Sunfire"` : aucune carte du VILAIN
# ne peut donc l'arracher, et toutes les cartes de Sunfire le peuvent — a
# commencer par elle-meme. C'est exactement ce que le mot-cle veut dire ici, et
# le moteur le rend NATIVEMENT. Sans lui, `sd018`/`sd020` rappellent qu'une
# carte Permanente qu'on force a partir fait PLANTER la partie
# (`card_face.py:473-483`, assert explicite).
#
# CARTES DE REFERENCE
#  - `bk009` Portal (pack blink) et `yd012` Yaka Arrow (pack yondu) : les deux
#    autres ameliorations JOUEUR attachees a un ennemi. Elles se DEFAUSSENT,
#    celle-ci se REMET DE COTE — d'ou `RemettreDeCote` et non `DiscardAll`.
#  - `04080` Dense Forest : le squelette d'une carte a Reponse forcee de phase.
#
# TEXTE CONTRE CODE
#  ⚠ « After the PLAYER phase ends » -> `AfterPhaseEnd(..., "Player", ...)`.
#    PAS la phase du vilain : la brulure mord une fois par round, entre le tour
#    des joueurs et celui du mechant.
#  ⚠ « deal 1 damage to ATTACHED ENEMY » -> l'hote, lu par `Hote()`. Une
#    brulure sans hote (impossible en pratique, elle n'entre en jeu qu'attachee)
#    ne frappe rien.
#  ⚠ « Set this card aside » APRES les degats, et dans les DEUX Reponses. La
#    carte revient donc dans la reserve et pourra etre reposee : c'est ce qui
#    fait tenir six exemplaires toute la partie.
#  ⚠ « After attached enemy LEAVES PLAY » -> la seconde Reponse. Sans elle, une
#    brulure posee sur un sbire vaincu resterait accrochee a un fantome et
#    serait perdue pour la partie, ce qui viderait la reserve en quelques tours.
#  ⚠ AUCUN COUT ET AUCUNE ICONE DE RESSOURCE sur le scan, verifie par decoupe
#    d'image : `desc` n'a ni `Cost` ni `RES`. La carte n'est pas jouable depuis
#    la main, et n'a donc pas besoin de `CanPlayThisUpgradeCard`.


def GetAbilities() -> Sequence['Ability']:

    def bruler_lhote(effect: 'Effect', message: 'Message.AfterPhaseEnd') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(message)

        hote = Hote(this)
        if hote is not None and Enemy.IsType(hote):
            this.DealDamage([hote], 1, effect)
        # « Set this card aside. » — apres les degats, toujours.
        RemettreDeCote(effect, this)

    def lhote_a_quitte_le_jeu(effect: 'Effect', message: 'Message.AfterCardLeavePlay') -> bool:
        this = effect.this
        return Hote(this) is message.trigger

    def ranger_la_brulure(effect: 'Effect', message: 'Message.AfterCardLeavePlay') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(message)
        RemettreDeCote(effect, this)

    return [
        AbilityFactory.AfterPhaseEnd(
            AbilityType.ForcedResponse,
            "Player",
            bruler_lhote,
        ),
        AbilityFactory.AfterCardLeavePlay(
            AbilityType.ForcedResponse,
            Enemy,
            ranger_la_brulure,
            conditions=[lhote_a_quitte_le_jeu],
        ),
    ]
