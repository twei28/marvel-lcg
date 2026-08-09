from . import *

# * Pepper Potts

def GetAbilities() -> Sequence['Ability']:

    def executive(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(AlterEgo)
        Unused(this)

        def pour_chaque(player: 'Player') -> None:
            main = list(player.hand_cards.Get())
            if not main:
                return

            def defausser_puis_chercher(targets: Sequence['CardFace']) -> None:
                Faces.DiscardAll(list(targets), effect)
                face = Search.PlayerCard(
                    effect,
                    player,
                    include_player_deck=True,
                    card_type=Upgrade,
                    trait="TECH",
                )
                if face:
                    player.GainCard(face, effect)

            # « may » : l'option est proposee, chacun reste libre de refuser.
            player.ChooseAbilities(
                effect,
                AbilityFactory.ForChoiceAbility(
                    "Discard 1 card to search for a TECH upgrade",
                    defausser_puis_chercher
                ).SetTarget(main, range=(1, 1), not_move=True),
            )

        Players.ForEachPlayer(effect, pour_chaque)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.AlterEgoAction,
            executive
        ).LimitOncePerRound(),
    ]
