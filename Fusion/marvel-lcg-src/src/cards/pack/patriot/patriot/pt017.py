from . import *

# MGH Addiction — OBLIGATION, give to the Elijah Bradley player.
# 2 icones de bonus. Set « Patriot » (numerotee sans mention nemesis sur le
# scan) : elle vit donc dans la cle `obligations` du deck de depart, PAS dans
# le `nemesis_set`.
#
# You may flip to alter-ego form. Choose:
# - Discard the Isaiah Bradley support card -> remove MGH Addiction from the
#   game.
# - Exhaust all allies under your control. If no allies were exhausted this
#   way, this card gains surge. Discard this obligation.
#
# ---------------------------------------------------------------------------
# STRUCTURE -> modeles EXACTS : `wc018` Avoiding the Demiurge et `sd017` No
# Outrunning This (meme auteur, packs freres), et `09027` Physical Toll
# (Doctor Strange, le precedent officiel). Meme triplet
# `AbilityFactory.WhenThisObligationGiveToYou` +
# `YouMayFlipToYourAlterEgoForm(player, effect)` + `player.ChooseAbilities` a
# DEUX branches.
#
# `desc.GiveTo = "Elijah Bradley"` : `Obligation.CheckPrintedValue`
# (obligation.py:50-52) exige ce champ sur toute Obligation. Il porte le nom
# de la face ALTER-EGO, comme toutes les obligations du depot.
#
# ---------------------------------------------------------------------------
# BRANCHE 1 : LA FLECHE EST UN COUT -> UN EFFET
#
# « DISCARD THE ISAIAH BRADLEY SUPPORT CARD -> remove MGH Addiction from the
# game. » Le cout est la defausse de `pt007`. **Sans Isaiah Bradley en jeu
# sous le controle du joueur, cette option est INDISPONIBLE** : elle porte
# donc une `condition=` (idiome de `09027` et de `cd014`), et le
# `ChooseAbilities` ne la propose pas. Cout impayable = rien ne se passe, et
# le joueur est renvoye sur la seconde branche.
#
# Le soutien est cherche parmi les cartes CONTROLEES PAR LE JOUEUR
# (`player.GetControlCards()`), pas dans tout le terrain : un `Worlds
# .FindCardOnField(name=...)` attraperait l'exemplaire d'un autre joueur.
# Le nom est ecrit SANS l'etoile d'unicite (`NOM_ISAIAH`, voir le piege du
# `*` en tete du set).
#
# ---------------------------------------------------------------------------
# BRANCHE 2 : LE SURGE EST **CONDITIONNEL**
#
# « Exhaust all allies under your control. IF NO ALLIES WERE EXHAUSTED THIS
# WAY, this card gains surge. Discard this obligation. »
#
# « exhausted THIS WAY » : ce ne sont pas « les allies en jeu » mais ceux que
# CETTE phrase a reellement inclines. Un allie deja incline ne compte donc
# pas, et un joueur qui n'a que des allies inclines declenche le surge. On
# lit le retour de `Faces.ExhaustAll`, qui rend la liste effectivement
# traitee, plutot que de compter les allies avant l'appel.
#
# Le filtre `canbe_exhaust` est fait a la main : `Faces.ExhaustAll` accepte
# n'importe quelle liste, et on veut precisement savoir lesquels ETAIENT
# redressables.
#
# « Discard this obligation » -> `Faces.DiscardAll([this], effect)`. Portee de
# la phrase : elle appartient a la SECONDE puce seulement (la premiere se
# termine deja par « remove ... from the game », qui est exclusif d'une
# defausse) — meme lecture que `wc018`, `sd017`, `ok019` et `il017`.
#
# ⚠ Le pilote de `tools/test_capacites.py` prend TOUJOURS la premiere option
# d'un `ChooseAbilities` : la seconde branche n'est testable qu'avec la cle
# de cas `preferer_option`, qui filtre sur le libelle de la
# `ForChoiceAbility`.
#
# ---------------------------------------------------------------------------
# PAS DE CAPACITE « Boost » ICI : le scan n'imprime aucun `[star] Boost:`,
# seulement les DEUX icones de bonus, lues nativement depuis `desc.Boost`.
# Ne pas coder de capacite fantome (PROCESSUS-CARTE §5).


def GetAbilities() -> Sequence['Ability']:

    def isaiah_en_jeu(player: 'Player') -> 'CardFace|None':
        for face in player.GetControlCards():
            if Support.IsType(face) and face.name == NOM_ISAIAH:
                return face
        return None

    def mgh_addiction(effect: 'Effect', message: 'Message.WhenObligationGiveToPlayer') -> None:
        this = effect.this.CastTo(Obligation)
        player = message.GetGaveToPlayer()

        YouMayFlipToYourAlterEgoForm(player, effect)

        isaiah = isaiah_en_jeu(player)

        def defausser_isaiah(targets: Sequence['CardFace']) -> None:
            Unused(targets)
            soutien = isaiah_en_jeu(player)
            if soutien is None:
                # Le cout n'est plus payable (la carte a quitte le jeu entre
                # la proposition et la resolution) : rien ne se passe.
                return
            Faces.DiscardAll([soutien], effect)
            Faces.RemoveAllFromGame([this], effect)

        def epuiser_les_allies(targets: Sequence['CardFace']) -> None:
            Unused(targets)
            candidats = [allie for allie in player.allies.Get()
                         if not allie.card.IsExhaust()]
            epuises = Faces.ExhaustAll(candidats, effect) if candidats else []
            if not epuises:
                ThisCardGainSurge(effect)
            Faces.DiscardAll([this], effect)

        player.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility(
                "Discard the Isaiah Bradley support card → remove MGH Addiction from the game",
                defausser_isaiah,
                condition=(isaiah is not None),
            ),
            AbilityFactory.ForChoiceAbility(
                "Exhaust all allies under your control. If no allies were exhausted this way, this card gains surge. Discard this obligation",
                epuiser_les_allies,
            ),
        )

    return [
        AbilityFactory.WhenThisObligationGiveToYou(
            mgh_addiction,
        ),
    ]
