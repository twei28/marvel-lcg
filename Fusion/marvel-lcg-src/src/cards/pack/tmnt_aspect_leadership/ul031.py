from . import *

# Suit Up — EVENEMENT Leadership (TMNT Reskins, Inkwire), cout 2, [physical].
# Alter-Ego Action: Search your deck and discard pile for an ally and an upgrade that can be attached to an
#   ally. Add them to your hand. (Shuffle.)
#
# MODIFIEE (reskin de `45017` Suit Up) : l'officielle dit « an upgrade that can be attached to THAT ally »,
# le scan « ... to AN ally ». QUESTION OUVERTE Q-UL-6 (fichier des questions ul) : coquille probable.
# LECTURE CODEE EN ATTENDANT (option recommandee A) : celle de l'officielle (amelioration attachable A
# L'ALLIE TROUVE). Si l'utilisateur retient la lecture litterale (B), seule la seconde recherche change :
# `CardFinder(card_type=Upgrade, check_effect_fn=<attachable a un allie quelconque>)`.
#
# Script propre copie de 45017 (voir ses commentaires : deux recherches de suite, allies sans amelioration
# attachable ecartes, remelange par la seconde recherche seulement).


def GetAbilities() -> Sequence['Ability']:

    def suit_up(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(this, message)

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
