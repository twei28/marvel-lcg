from . import *

# Suit Up
#
# « Alter-Ego Action: Search your deck and discard pile for an ally and an
#   upgrade that can be attached to that ally. Add them to your hand.
#   (Shuffle.) »
#
# DEUX RECHERCHES DE SUITE, PAS UN CHOIX DE DEUX CARTES (18/09/2026)
#
# La carte demande un allie PUIS une amelioration attachable A CET ALLIE. La
# version precedente posait UNE seule question a deux cibles
# (`SetTarget(range=(2, 2), select_rule="DifferentType")`) avec un
# `check_again_fn` qui verifiait le couple apres coup. Trois defauts, signales
# en jeu par l'utilisateur (partie Laura Kinney contre Crossbones) :
#
#  1. `select_rule="DifferentType"` n'est applique NULLE PART (ni par le
#     moteur, `selector_rule.py:AfterSelectTargets`, ni par le plateau, qui
#     lit `select_rule` sans s'en servir) : on pouvait prendre DEUX
#     ameliorations ;
#  2. le couple illegal n'etait refuse qu'au dernier moment, par
#     `check_again_fn` : l'action echouait, et Suit Up partait A LA DEFAUSSE
#     sans rien faire ;
#  3. les ameliorations proposees etaient celles attachables a N'IMPORTE QUEL
#     allie du deck, pas a l'allie retenu.
#
# Le moteur sait poser la vraie question : `CardFinder(canbe_attach_to=<allie>)`
# appelle `Upgrade.CanAttachTo` (card_type/upgrade.py:83), qui relit le
# selecteur de la capacite « Play » de l'amelioration examinee. C'est le patron
# du pack `patriot` (`pt002` Hawkingbird, `AmeliorationAttachableA`), et c'est
# aussi ce que faisait le brouillon `45017_.py` reste dans le pack en amont.
# Une amelioration qui se pose sur l'identite (Danger Room Training) ou sur un
# allie particulier (`45015` Sidekick, « attach to an identity-specific ally »)
# est donc ecartee, sans que le joueur ait a le deviner.
#
# ⚠ LES ALLIES SANS AUCUNE AMELIORATION ATTACHABLE SONT ECARTES AUSSI : sinon
# le joueur choisit un allie, la seconde recherche ne propose rien, et la carte
# est perdue pour rien. « for an ally AND an upgrade » : les deux ou aucun.
#
# ⚠ « Search your deck AND discard pile » : les deux zones. Le remelange est
# fait par la SECONDE recherche (`not_move=True` sur la premiere, sinon le deck
# serait melange deux fois pour un seul « (Shuffle.) »).


def GetAbilities() -> Sequence['Ability']:

    def suit_up(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(this)

        initiator = effect.GetInitiator()

        zones = list(initiator.player_deck.Get()) + list(initiator.discard_pile.Get())
        ameliorations = Filter.ByType(zones, Upgrade)

        def allie_equipable(eff: 'Effect', face: 'CardFace') -> bool:
            return any(u.CanAttachTo(face) for u in ameliorations)

        allie = Search.PlayerCard(
            effect,
            initiator,
            include_player_deck=True,
            include_discard_pile=True,
            not_move=True,
            finder=CardFinder(card_type=Ally, check_effect_fn=allie_equipable),
        )
        if not allie:
            return

        amelioration = Search.PlayerCard(
            effect,
            initiator,
            include_player_deck=True,
            include_discard_pile=True,
            finder=CardFinder(card_type=Upgrade, canbe_attach_to=allie),
        )
        if not amelioration:
            return

        initiator.GainCard([allie, amelioration], effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.AlterEgoAction,
            suit_up,
        ).SetPlay().SetLabel()
    ]
