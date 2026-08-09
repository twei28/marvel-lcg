from . import *
def GetAbilities() -> Sequence['Ability']:
    def radar_sense(effect: 'Effect', message: 'Message.AfterUnitAttackUnit') -> None:
        this = effect.this.CastTo(Upgrade)
        target = effect.this.bind_face
        SenseDiscard(this, effect)
        if target:
            this.DealDamage([target], 3, effect)
    return [AbilityFactory.CanPlayThisUpgradeCard(CardFinder(card_type=Enemy)),
            AbilityFactory.AfterUnitAttackUnit(AbilityType.Response, 'YourIdentity', None, radar_sense, conditions=[lambda effect, message: (effect.this.bind_face == message.attacked)])]
