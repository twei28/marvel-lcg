from . import *

# System Relaunch — custom « Kajislav »
# Alter-Ego Action: Heal damage from Albert equal to your REC and change to
# hero form -> resolve Albert's "Initiate Protocol" ability.

def GetAbilities() -> Sequence['Ability']:

    def system_relaunch(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(this)

        initiator = effect.GetInitiator()

        value = initiator.GetAlterEgo().recover
        this.HealthUnits(effect.targets, value, effect)

        initiator.GetIdentity().ChangeToForm(Hero, effect)

        ResolveInitiateProtocol(effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.AlterEgoAction,
            system_relaunch
        ).SetPlay().SetLabel()
        .SetTarget("YourAlterEgo", canbe_heal=True),
    ]
