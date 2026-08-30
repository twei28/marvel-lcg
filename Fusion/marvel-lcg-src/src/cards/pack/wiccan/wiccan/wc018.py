from . import *

# Avoiding the Demiurge — OBLIGATION, give to the Billy Kaplan player.
# You may flip to alter-ego form. Choose:
# - Exhaust your identity -> remove Avoiding the Demiurge from the game.
# - Boost icons cannot be counted for any Wiccan card effects until the end
#   of the next player phase. Discard this obligation.
# [star] Boost: Reveal this card.
#
# Structure -> modele EXACT : ok019 Funeral Rites (okoye) et il017 Shadow of
# the Future (iron_lad, meme auteur), meme triplet
# `WhenThisObligationGiveToYou` + `YouMayFlipToYourAlterEgoForm(player,
# effect)` + `player.ChooseAbilities` a DEUX branches.
#
# `desc.GiveTo = "Billy Kaplan"` : `Obligation.CheckPrintedValue` exige ce
# champ sur toute Obligation (correctif deja paye sur il020). Il porte le nom
# de la face ALTER-EGO, comme toutes les obligations du depot.
#
# Branche 1, « Exhaust your identity » -> `Faces.ExhaustAll([identite],
# effect)` puis `Faces.RemoveAllFromGame([this], effect)`. « your identity »
# (et non « your alter ego » comme ok019) : on incline la face COURANTE, quelle
# qu'elle soit — d'ou `player.GetIdentity()` et non `.GetAlterEgoFace()`.
#
# Branche 2 -> l'interrupteur global du pack, `EteindreLesBoosts(player,
# effect)` (voir wiccan/__init__.py). Il vit dans le `__init__.py` du set et
# non ici, parce qu'il doit eteindre le comptage de TOUTES les cartes du pack,
# pas d'une seule : les neuf cartes qui comptent des icones passent par
# `IconesBoostDuDessus`, qui interroge le meme drapeau.
# « Discard this obligation » -> `Faces.DiscardAll([this], effect)`. Portee de
# la phrase : elle appartient a la SECONDE puce seulement (la premiere se
# termine deja par « remove ... from the game », qui est exclusif d'une
# defausse) — meme lecture que ok019 et il017.
#
# [star] Boost -> `AbilityFactory.WhenCardBecomeBoost("This", RevealThisCard)`,
# l'idiome unique du depot pour « Boost: Reveal this card » (modeles 16140
# Sound the Alarms, 56144 Cap's Helmet, et toutes les cartes `cw` a Boost de
# revelation). `RevealThisCard` est l'aide partagee de `cards/pack/__init__.py`.

def GetAbilities() -> Sequence['Ability']:

    def avoiding_the_demiurge(effect: 'Effect', message: 'Message.WhenObligationGiveToPlayer') -> None:
        this = effect.this.CastTo(Obligation)
        player = message.GetGaveToPlayer()

        YouMayFlipToYourAlterEgoForm(player, effect)

        def retirer_du_jeu(targets: Sequence['CardFace']) -> None:
            Unused(targets)
            identite = player.GetIdentity()
            if identite is not None:
                Faces.ExhaustAll([identite], effect)
            Faces.RemoveAllFromGame([this], effect)

        def eteindre_les_boosts(targets: Sequence['CardFace']) -> None:
            Unused(targets)
            EteindreLesBoosts(player, effect)
            Faces.DiscardAll([this], effect)

        player.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility(
                "Exhaust your identity → remove Avoiding the Demiurge from the game",
                retirer_du_jeu,
            ),
            AbilityFactory.ForChoiceAbility(
                "Boost icons cannot be counted for any Wiccan card effects until the end of the next player phase. Discard this obligation",
                eteindre_les_boosts,
            ),
        )

    return [
        AbilityFactory.WhenThisObligationGiveToYou(
            avoiding_the_demiurge,
        ),
        AbilityFactory.WhenCardBecomeBoost(
            "This",
            RevealThisCard,
        ),
    ]
