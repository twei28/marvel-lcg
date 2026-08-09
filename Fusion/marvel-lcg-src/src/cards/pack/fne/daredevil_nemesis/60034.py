from . import *
def GetAbilities() -> Sequence['Ability']:
    def deadliest_man_alive(effect: 'Effect', message: 'Message.WhenUnitWouldAttack') -> None:
        this = effect.this.CastTo(EncounterSideScheme)
        Unused(this)
        message.GiveAdditionalBoostCardForThisActivation(1, effect)
    return [AbilityFactory.WhenUnitWouldAttack(AbilityType.ForcedInterrupt, CardFinder(name='Bullseye'), deadliest_man_alive)]
