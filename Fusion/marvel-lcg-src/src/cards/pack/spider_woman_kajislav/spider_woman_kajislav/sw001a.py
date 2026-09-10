from . import *

# * Spider-Woman — HEROS. CTR 2, ATQ 1, DEF 2, main 5, 10 PV. AVENGER.
# Psionic Webbing — Interrupt: When a boost card on an enemy attacking you is
#   turned face up, for each boost icon ([boost]) on that card, you may remove
#   1 psionic web counter from here to cancel that boost icon ([boost]) and
#   deal 1 damage to that enemy.
#
# ⚠⚠ C'EST LA CARTE QUI DEPENSE LE STOCK, ET ELLE LE FAIT ICONE PAR ICONE.
# « FOR EACH boost icon ... YOU MAY remove 1 counter ... to cancel THAT boost
# icon » : le joueur choisit combien il en paie, de zero a toutes. Une carte de
# boost a 3 icones peut etre annulee d'une seule, de deux, ou des trois.
#
# CARTES DE REFERENCE
#  - `08006` Attacrobatics (pack bkw) : le montage exact de la fenetre —
#    `WhenBoostCardTurnedFaceUp(HeroInterrupt, "BoostIcons", op)`, puis
#    `message.CancelAllBoostIcons(effect)` et des degats au vilain.
#    Attacrobatics annule TOUT d'un coup, contre la defausse de la carte ;
#    Spider-Woman marchande icone par icone, contre ses compteurs.
#  - `as015` * Scarlet Spider : la lecture de `message.would_message`.
#
# ⚠⚠ CORRECTIF MOTEUR DU 10/09/2026 : `Message.WhenBoostCardTurnedFaceUp`
# n'exposait QUE `CancelAllBoostIcons`, qui leve `cancel_boost_icons` — et
# `can_boost.py:84` met alors le compte a ZERO sans relire la carte. Impossible
# d'en annuler UNE. D'ou `CancelBoostIcons(value, by_effect)`, ecrite dans le
# meme fichier, sur le meme modele, qui baisse le compte imprime sans lever le
# drapeau.
#
# TEXTE CONTRE CODE
#  ⚠ « on an enemy attacking YOU » : la carte de boost doit appartenir a une
#    activation dirigee contre CE joueur. `activate_target="YourHero"` le dit a
#    la fabrique ; en multijoueur, la carte ne parle pas des autres.
#    ⚠ PREMIERE ECRITURE FAUSSE, corrigee le 10/09/2026 : `"You"` y avait ete
#    passe. Une CHAINE EST UNE SEQUENCE en Python, et `invoke_check_card`
#    (condition/card_type.py:247) affirme le contraire : la condition levait un
#    AssertionError que le moteur AVALAIT, et l'interruption ne s'ouvrait
#    JAMAIS. Le cas d'harnais ne l'a vu qu'au degat manquant sur Rhino.
#  ⚠ « a boost card ... IS TURNED FACE UP » : la fenetre est
#    `WhenBoostCardTurnedFaceUp`, pas `WhenCardBecomeBoost`. La seconde sert
#    aux capacites « [star] Boost », qui ne sont pas le sujet.
#  ⚠ « remove 1 counter FROM HERE » : de l'identite, pas d'une carte. C'est le
#    stock unique du pack, voir `__init__.py`.
#  ⚠ « deal 1 damage to THAT ENEMY » : l'attaquant, pas une cible au choix.
#  ⚠ Les deux moities vont ENSEMBLE et se paient d'un seul compteur : annuler
#    sans frapper, ou frapper sans annuler, n'est pas offert.
#  ⚠ Stock vide : la boucle ne propose rien, l'attaque garde ses icones.


def GetAbilities() -> Sequence['Ability']:

    def toile_psionique(effect: 'Effect', message: 'Message.WhenBoostCardTurnedFaceUp') -> None:
        this = effect.this.CastTo(Hero)
        joueur = effect.GetInitiator()
        if joueur is None:
            return
        attaquant = message.being_message.attacker
        if attaquant is None:
            return

        # ⚠ On relit `message.boost_icons` A CHAQUE TOUR : chaque annulation
        # accordee le fait baisser, et la carte n'en offre pas plus qu'il n'en
        # reste.
        while message.boost_icons > 0 and ToilesDe(joueur) > 0:
            def annuler(cibles: Sequence['CardFace']) -> None:
                Unused(cibles)
                # Le compteur a deja ete retire par le COUT.
                message.CancelBoostIcons(1, effect)
                this.DealDamage([attaquant], 1, effect)

            choisi = joueur.MayChooseOneAbility(
                effect,
                AbilityFactory.ForChoiceAbility(
                    "Remove 1 psionic web counter to cancel that boost icon and deal 1 damage",
                    annuler,
                ).SetHasNoTargetEffect()
                .SetCostFunc(CostFunc.Counter("YourIdentity", 1, COMPTEUR)),
            )
            if choisi is None:
                return

    return [
        AbilityFactory.WhenBoostCardTurnedFaceUp(
            AbilityType.Interrupt,
            "BoostIcons",
            toile_psionique,
            # ⚠ `while_attack=True` N'EST PAS DECORATIF, il protege
            # `activate_target` : la fabrique lit les cibles dans
            # `would_message.attacked_targets` et fait `assert False` quand
            # l'activation n'est pas une attaque (boost.py:272). Une MANIGANCE
            # de vilain tire aussi des cartes de boost, et la condition
            # explosait alors a chaque fois. Les deux conditions sont evaluees
            # DANS L'ORDRE de la liste (boost.py:293) : `check_while_attack`
            # passe avant, et ecarte la manigance avant l'assert.
            # 8 AssertionError sur 32 parties d'autoplay, le 10/09/2026 ; les
            # 39 cas etaient verts, aucun ne fait manigancer le vilain.
            while_attack=True,
            activate_target="YourHero",
        ),
    ]
