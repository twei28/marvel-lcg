from . import *
def GetAbilities() -> Sequence['Ability']:
    def ghost_rider(effect: 'Effect', message: 'Message.WhenUnitWouldAttack') -> None:
        this = effect.this.CastTo(Ally)
        Unused(this)
        Faces.GiveStatus(list(message.targets), 'Confused', effect)
    def check_villain(effect: 'Effect', message: 'Message.WhenUnitWouldAttack') -> bool:
        return any(Villain.IsType(t) for t in message.targets)
    def check_not_villain(effect: 'Effect', message: 'Message.WhenUnitWouldAttack') -> bool:
        return not any(Villain.IsType(t) for t in message.targets)
    return [AbilityFactory.WhenUnitMakeAttack(AbilityType.Interrupt, 'This', ghost_rider, conditions=[check_not_villain]).SetCost(Cost('Y')),
            AbilityFactory.WhenUnitMakeAttack(AbilityType.Interrupt, 'This', ghost_rider, conditions=[check_villain]).SetCost(Cost('YY'))]
