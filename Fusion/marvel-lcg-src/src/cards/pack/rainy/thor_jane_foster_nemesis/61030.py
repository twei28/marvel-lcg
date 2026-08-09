from . import *

# Execute — custom "Rainy" (némésis de Thor Jane Foster)
# When Revealed: Defeat the ally in play with the highest remaining hit
# points. If no ally was defeated this way, this card gains surge.

def GetAbilities() -> Sequence['Ability']:

    def execute(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Treachery)

        allies = list(Worlds.FindCardsOnField(effect, card_type=Ally))
        if allies:
            highest = max(a.health for a in allies)
            candidates = [a for a in allies if a.health == highest]
            player = message.GetToPlayer()

            def defeat(targets: Sequence['CardFace']) -> None:
                for target in targets:
                    target.Defeated(this, effect)

            player.ChooseAbilities(
                effect,
                AbilityFactory.ForChoiceAbility(
                    "Defeat the ally with the highest remaining hit points",
                    defeat
                ).SetTarget(candidates)
            )
        else:
            this.GainSurge(1, effect)

    return [
        AbilityFactory.WhenThisRevealed(
            None,
            execute
        )
    ]
