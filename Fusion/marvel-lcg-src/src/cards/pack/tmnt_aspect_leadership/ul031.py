from . import *

# Suit Up — EVENEMENT Leadership (TMNT Reskins, Inkwire), cout 2, [physical].
# Alter-Ego Action: Search your deck and discard pile for an ally and an upgrade that can be attached to an
#   ally. Add them to your hand. (Shuffle.)
#
# MODIFIEE (reskin de `45017` Suit Up) : l'officielle dit « an upgrade that can be attached to THAT ally »,
# le scan « ... to AN ally ». LECTURE LITTERALE CHOISIE PAR L'UTILISATEUR (17/10/2026), contre la
# recommandation : recherche LARGE. L'allie n'a plus de contrainte ; l'amelioration doit pouvoir s'attacher
# a UN allie quelconque (pas forcement celui trouve) : allies de son deck, de sa defausse ou en jeu
# sous son controle. Les deux recherches sont independantes : s'il n'y a rien d'un cote, l'autre est
# quand meme ajoute (le deck est melange dans tous les cas).
#
# Script propre (45017 liait la 2e recherche a l'allie trouve : `canbe_attach_to=allie`).
# `Upgrade.CanAttachTo(face)` relit le selecteur de la capacite de jeu de l'amelioration (Sidekick,
# « attach to an identity-specific ally you control », n'est attachable qu'a un allie d'identite EN JEU).


def GetAbilities() -> Sequence['Ability']:

    def suit_up(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(this, message)

        initiator = effect.GetInitiator()

        zones = list(initiator.player_deck.Get()) + list(initiator.discard_pile.Get())
        allies_possibles = Filter.ByType(zones, Ally) + list(initiator.allies.Get())

        def attachable_a_un_allie(eff: 'Effect', face: 'CardFace') -> bool:
            Unused(eff)
            upgrade = face.CastTo(Upgrade)
            return any(upgrade.CanAttachTo(ally) for ally in allies_possibles)

        allie = Search.PlayerCard(
            effect,
            initiator,
            include_player_deck=True,
            include_discard_pile=True,
            not_move=True,
            card_type=Ally,
        )

        amelioration = Search.PlayerCard(
            effect,
            initiator,
            include_player_deck=True,
            include_discard_pile=True,
            finder=CardFinder(card_type=Upgrade, check_effect_fn=attachable_a_un_allie),
        )
        if not amelioration:
            # la recherche des ameliorations melange le deck ; sans elle, on melange ici
            initiator.player_deck.Shuffle(effect)

        trouvees = [c for c in (allie, amelioration) if c]
        if trouvees:
            initiator.GainCard(trouvees, effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.AlterEgoAction,
            suit_up,
        ).SetPlay().SetLabel()
    ]
