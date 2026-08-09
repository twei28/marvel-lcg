from . import *
def GetAbilities() -> Sequence['Ability']:
    def alpha_flight_recruit(effect: 'Effect', message: 'Message.AfterCardPlacedCounter') -> None:
        this = effect.this.CastTo(Upgrade)
        target = this.bind_face
        if target:
            this.HealthUnits([target], 1, effect)
    def check_energy_channel(effect: 'Effect', message: 'Message.AfterCardPlacedCounter') -> bool:
        if (message.name != 'energy'):
            return False
        return (message.trigger.paper.name == 'Energy Channel')
    return [AbilityFactory.CanPlayThisUpgradeCard(CardFinder(card_type=Ally)),
            AbilityFactory.AfterCounterPlacedOn(AbilityType.Response, None, 'energy', alpha_flight_recruit, conditions=[check_energy_channel]).SetTarget('Trigger')]
