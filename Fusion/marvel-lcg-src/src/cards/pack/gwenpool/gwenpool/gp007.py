from . import *

# * Gwen's Room — custom « ekAugust »
# You get +1 REC.
# Alter-Ego Action: Exhaust Gwen's Room -> heal 1 damage from Gwendolyn
# Poole. Then, find Unbelievable Gwenpool and add it to your hand.
# Bulle : « Heal 1 damage from Gwenpool. »

def GetAbilities() -> Sequence['Ability']:

    def gwens_room(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Support)

        initiator = effect.GetInitiator()
        this.HealthUnits([initiator.GetIdentity()], 1, effect)

        face = Search.PlayerCard(
            effect,
            initiator,
            include_player_deck=True,
            include_discard_pile=True,
            name="Unbelievable Gwenpool",
        )
        if face:
            initiator.GainCard(face, effect)

    return [
        *AbilityFactory.GiveKeywordToAttached(
            "You",
            recover=1,
        ),
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.AlterEgoAction,
            gwens_room
        ).SetCostFunc(CostFunc.Exhaust("This")),
    ]
