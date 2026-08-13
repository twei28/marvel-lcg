from . import *

# Push Your Luck

def GetAbilities() -> Sequence['Ability']:

    def push_your_luck(effect: 'Effect', message: 'Message.WhenEnemyWouldActivate') -> None:
        this = effect.this.CastTo(Event)

        message.SetBeInstead(effect)

        # `message.power` dit ce qui a ete annule : "ATK" en forme heros, "SCH"
        # en alter-ego (sender_enemy.py). C'est la distinction que demande la
        # carte, et le moteur la porte deja.
        if message.power == "ATK":
            this.DealDamage([message.trigger], 3, effect)
        else:
            this.RemoveThreatFromSchemes("MainScheme", 2, effect)

    return [
        AbilityFactory.WhenEnemyWouldActivate(
            AbilityType.HeroInterrupt,
            None,
            push_your_luck
        ).SetPlay().SetLabel('attack', 'defense', 'thwart')
        .SetCostFunc(CostFunc.DealPlayerEncounterCard(1, "Initiator")),
    ]
