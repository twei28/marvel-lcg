from . import *

# Tidal Surge — custom « DesignHacker » (traîtrise némésis de Human Torch)
# Surge (desc).
# When Revealed: If Hydro-Man is in play, each player must choose to either
# exhaust their identity or take 3 indirect damage.

def GetAbilities() -> Sequence['Ability']:

    def tidal_surge(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Treachery)

        if not Worlds.FindCardOnField(effect, name="Hydro-Man", card_type=Minion):
            return

        for player in list(effect.world.players):
            if player.is_eliminated:
                continue

            def degats(targets: Sequence['CardFace'], player=player) -> None:
                player.GetIdentity().TakeIndirectDamage(this, 3, effect)

            player.ChooseAbilities(
                effect,
                AbilityFactory.ForChoiceAbility(
                    "Exhaust your identity",
                    lambda targets: None
                ).SetCostFunc(CostFunc.Exhaust("YourIdentity")),
                AbilityFactory.ForChoiceAbility(
                    "Take 3 indirect damage",
                    degats
                ),
            )

    return [
        AbilityFactory.WhenThisRevealed(
            None,
            tidal_surge
        ),
    ]
