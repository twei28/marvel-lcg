from . import *

# * Mark VII-A — SBIRE NEMESIS. ELITE. SENTINEL. CTR 2 / ATQ 2[star] / 5 PV,
# 3 icones de boost.
# [star] Forced Response: After Mark VII-A makes an undefended attack against
#   you, flip a [[COMPONENT]] upgrade ([[INTACT]] side up) to its [[DESTROYED]]
#   side. If you cannot, discard 1 upgrade you control.
#
# Cartes de reference :
#  - `04080` Dense Forest : `AfterUnitAttackUnit(..., is_undefended_attack=True)`,
#    le seul declencheur « after X makes an UNDEFENDED attack against you ».
#  - `dz017a` : `Faces.FlipAllTo(cibles, None, effect)`.
#
# ⚠ « FLIP », PAS « DESTROY ». Le mot-cle maison ferait subir 2 degats
# imblocables EN PLUS (fiche docs/reference/mots-cles/destroy.md) ; l'auteur a
# volontairement ecrit « flip ... to its DESTROYED side ». Cette carte
# n'appelle donc PAS `Detruire()`, et c'est la seule du pack a retourner un
# Component sans en payer le prix. A ne surtout pas « harmoniser ».
#
# ⚠ Mots-pieges (PROCESSUS-CARTE etape 5) :
#  - « **against you** » : l'attaque doit viser le joueur attaque, pas un
#    allie. C'est ce que porte le second argument `"You"`.
#  - « **If you cannot** » : la defausse d'amelioration n'est PAS un choix,
#    c'est le repli quand aucun Component intact n'existe. Deux branches
#    exclusives, testees dans cet ordre.
#  - « discard 1 upgrade **you control** » : n'importe laquelle... SAUF une
#    PERMANENTE, que la regle du jeu interdit de defausser. Les quatre
#    Component en sont, des deux cotes : quand ils sont tous detruits, cette
#    branche ne trouve donc une cible que si le joueur controle une autre
#    amelioration (Propulsion Array, Reinforced Plating, Targeting Protocol).
#    Sinon rien ne se passe, et c'est bien ce que dit « if you cannot ».


def GetAbilities() -> Sequence['Ability']:

    def surcharge(effect: 'Effect', message: 'Message.AfterUnitAttackUnit') -> None:
        this = effect.this.CastTo(Minion)
        Unused(this)

        joueur = message.GetToPlayer()
        if joueur is None:
            return

        intacts = [f for f in Worlds.FindCardsOnField(
            effect, card_type=Upgrade, trait=TRAIT_INTACT)
            if f.GetControlBy() == joueur]

        if intacts:
            cible = joueur.AskChooseFace(intacts, effect)
            if cible is not None:
                Faces.FlipAllTo([cible], None, effect)
                return

        # ⚠ LES QUATRE COMPONENT SONT PERMANENTS, DONC INDEFAUSSABLES. Sans ce
        # filtre, un robot entierement demonte n'avait plus que des permanentes
        # a proposer, et `DiscardInternal` tombait sur son assertion
        # « controller.is_eliminated » (card_face.py:626) — quatre tracebacks
        # sur seize parties d'autoplay, le 13/09/2026. Le moteur pose la meme
        # regle dans son filtre `canbe_discard` (checker.py:170), on la reprend
        # ici mot pour mot.
        ameliorations = [
            a for a in joueur.GetControlUpgrade()
            if not (HasPermanent.IsType(a) and a.permanent)
        ]
        if ameliorations:
            a_defausser = joueur.AskChooseFace(ameliorations, effect)
            if a_defausser is not None:
                Faces.DiscardAll([a_defausser], effect)

    return [
        AbilityFactory.AfterUnitAttackUnit(
            AbilityType.ForcedResponse,
            "This",
            "You",
            surcharge,
            is_undefended_attack=True,
        ),
    ]
