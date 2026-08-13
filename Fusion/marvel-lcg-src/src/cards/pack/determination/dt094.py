from . import *

# Diversion Skill

def GetAbilities() -> Sequence['Ability']:

    def diversion_skill(effect: 'Effect', message: 'Message.WhenUnitWouldTakeDamage') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(this)

        initiator = effect.GetInitiator()
        message.IncreaseDamage(1, effect)
        initiator.DrawUp(1, effect)

    def check_votre_identite(effect: 'Effect', message: 'Message.WhenUnitWouldTakeDamage') -> bool:
        this = effect.this.CastTo(Upgrade)
        player = this.GetControlByPlayer()
        return player is not None and message.trigger == player.GetIdentity()

    return [
        AbilityFactory.CanPlayThisUpgradeCard(),
        AbilityFactory.WhenUnitWouldTakeDamage(
            AbilityType.Interrupt,
            None,
            diversion_skill,
            is_from_attack=True,
            conditions=[check_votre_identite],
        ).SetCostFunc(CostFunc.Counter("This", 1, 'diversion')),
    ]
