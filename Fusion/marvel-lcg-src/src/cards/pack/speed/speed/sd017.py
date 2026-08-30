from . import *

# No Outrunning This — OBLIGATION, give to the Thomas Shepherd player.
# 2 icones de bonus. Set « Speed » (numerotee « SPEED » sur le scan, sans
# mention nemesis) : elle vit donc dans la cle `obligations` du deck de
# depart, PAS dans le `nemesis_set` — a la difference de sd022 Conflicted
# Feelings, qui est « SPEED NEMESIS (5/5) ».
#
# You may flip to alter-ego form. Choose:
# - Exhaust Thomas Shepherd -> remove No Outrunning This from the game.
# - You cannot resolve Speed's Hyperkinetic Fuel Interrupt until the end of
#   the next round. Discard this obligation.
#
# ---------------------------------------------------------------------------
# STRUCTURE -> modele EXACT : `wc018` Avoiding the Demiurge (meme auteur, meme
# pack frere) et `09027` Physical Toll (Doctor Strange, le precedent officiel).
# Meme triplet `AbilityFactory.WhenThisObligationGiveToYou` +
# `YouMayFlipToYourAlterEgoForm(player, effect)` + `player.ChooseAbilities` a
# DEUX branches.
#
# `desc.GiveTo = "Thomas Shepherd"` : `Obligation.CheckPrintedValue`
# (obligation.py:50-52) exige ce champ sur toute Obligation. Il porte le nom de
# la face ALTER-EGO, comme toutes les obligations du depot.
#
# ---------------------------------------------------------------------------
# BRANCHE 1, « Exhaust Thomas Shepherd -> remove ... from the game ».
#
# Le texte NOMME l'alter-ego (« Exhaust THOMAS SHEPHERD »), pas « your
# identity » comme wc018 : on incline donc la face ALTER-EGO. Comme la premiere
# phrase invite deja a basculer en identite civile, la face courante est
# normalement la bonne ; on passe malgre tout par `player.GetIdentity()`, qui
# rend la face EN JEU, et la branche n'est proposee que si le joueur est bien
# en alter-ego (`condition=player.IsAlterEgo()`, exactement comme 09027).
# Sans cette condition, un joueur qui refuse la bascule pourrait « incliner
# Thomas Shepherd » alors que Thomas Shepherd n'est pas sur la table.
#
# ---------------------------------------------------------------------------
# BRANCHE 2, l'interrupteur.
#
# `EteindreHyperkineticFuel(player, effect)` (speed/speed/__init__.py) : le
# drapeau est pose sur `effect.world` et rabaisse par une capacite TEMPORAIRE
# enregistree sur l'IDENTITE du joueur — jamais sur l'obligation, qui part a la
# defausse dans la foulee et emporterait ses capacites temporaires avec elle.
#
# ⚠ DIFFERENCE AVEC wc018 : ici c'est « until the end of the NEXT ROUND », pas
# « until the end of the next player phase ». Un round de PLUS. L'obligation
# est revelee pendant la phase du vilain du round N : la premiere fin de round
# rencontree est celle du round N (elle ne compte pas), la seconde celle du
# round N+1 — c'est elle que le texte vise. D'ou le compteur interne de
# `EteindreHyperkineticFuel`, qui laisse passer la premiere.
#
# « Discard this obligation » -> `Faces.DiscardAll([this], effect)`. Portee de
# la phrase : elle appartient a la SECONDE puce seulement (la premiere se
# termine deja par « remove ... from the game », qui est exclusif d'une
# defausse) — meme lecture que wc018, ok019 et il017.
#
# ⚠ Le pilote de `tools/test_capacites.py` prend TOUJOURS la premiere option
# d'un `ChooseAbilities` : la seconde branche n'est testable qu'avec la cle de
# cas `preferer_option`, qui filtre sur le libelle de la `ForChoiceAbility`.
#
# ---------------------------------------------------------------------------
# PAS DE CAPACITE « Boost » ici : le scan n'imprime aucun `[star] Boost:`,
# seulement les deux icones de bonus, qui sont lues nativement depuis
# `desc.Boost`. Ne pas coder de capacite fantome.


def GetAbilities() -> Sequence['Ability']:

    def no_outrunning_this(effect: 'Effect', message: 'Message.WhenObligationGiveToPlayer') -> None:
        this = effect.this.CastTo(Obligation)
        player = message.GetGaveToPlayer()

        YouMayFlipToYourAlterEgoForm(player, effect)

        def retirer_du_jeu(targets: Sequence['CardFace']) -> None:
            Unused(targets)
            identite = player.GetIdentity()
            if identite is not None:
                Faces.ExhaustAll([identite], effect)
            Faces.RemoveAllFromGame([this], effect)

        def eteindre_hyperkinetic_fuel(targets: Sequence['CardFace']) -> None:
            Unused(targets)
            EteindreHyperkineticFuel(player, effect)
            Faces.DiscardAll([this], effect)

        player.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility(
                "Exhaust Thomas Shepherd → remove No Outrunning This from the game",
                retirer_du_jeu,
                condition=player.IsAlterEgo(),
            ),
            AbilityFactory.ForChoiceAbility(
                "You cannot resolve Speed's Hyperkinetic Fuel Interrupt until the end of the next round. Discard this obligation",
                eteindre_hyperkinetic_fuel,
            ),
        )

    return [
        AbilityFactory.WhenThisObligationGiveToYou(
            no_outrunning_this,
        ),
    ]
