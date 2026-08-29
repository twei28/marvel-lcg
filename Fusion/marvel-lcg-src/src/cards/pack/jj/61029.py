from . import *

# * Defend Our City
# [star] Hinder 1[per_hero]. Prerequisite ([[Defender]]). Victory 0.
# When Defeated: Each player may search their deck and discard pile for a
# Team-Up card and add it to their hand. Until the end of the phase, reduce the
# cost to play each Team-Up card by 1.
#
# Une carte Team-Up se reconnait a son mot-cle imprime, que le moteur stocke
# dans `team_up` (has_teamup.py) : plus fiable que de lire le texte.

def EstTeamUp(face: 'CardFace') -> bool:
    equipe = getattr(face, 'team_up', None)
    return bool(equipe) and any(equipe)


def GetAbilities() -> Sequence['Ability']:

    def when_defeated(effect: 'Effect', message: 'Message.WhenSchemeBeDefeated') -> None:
        this = effect.this.CastTo(PlayerSideScheme)
        Unused(this)

        # « Each player MAY search ... and add it to their hand. »
        for player in Worlds.GetPlayers(effect):
            pool = Search.SearchForCards(
                effect, player,
                include_player_deck=True, include_player_discard_pile=True)
            faces = [f for f in pool if EstTeamUp(f)]
            if not faces:
                continue

            def prendre(cibles: Sequence['CardFace'], player: 'Player'=player):
                for face in cibles:
                    player.GainCard(face, effect)
                player.player_deck.Shuffle(effect)

            def refuser(_cibles: Sequence['CardFace']):
                pass

            player.ChooseAbilities(
                effect,
                AbilityFactory.ForChoiceAbility('Prendre une carte Team-Up', prendre)
                .SetTarget(faces, range=(1, 1)),
                AbilityFactory.ForChoiceAbility('Ne rien prendre', refuser),
            )

        # « Until the end of the phase, reduce the cost to play each Team-Up
        # card by 1. » Clause qui manquait entierement.
        this.effect.RegisterTemp(
            AbilityFactory.ReduceCostToPlayFaceWhen(
                CardFinder(card_type=Event),
                1,
                "EachPlayer",
                conditions=[lambda e, m: EstTeamUp(m.effect.this)],
            ),
            unregister_after_exec=False,
            until_phase_end=True,
        )

    return [
        AbilityFactory.WhenSchemeBeDefeated(AbilityType.WhenDefeated, 'This', when_defeated),
    ]
