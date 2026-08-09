from . import *
def GetAbilities() -> Sequence['Ability']:
    def superior_taste(effect: 'Effect', message: 'Message.AfterUnitThwartScheme') -> None:
        this = effect.this.CastTo(Upgrade)
        target = effect.this.bind_face
        SenseDiscard(this, effect)
        if target:
            this.RemoveThreatFromSchemes([target], 2, effect)
    return [AbilityFactory.CanPlayThisUpgradeCard(CardFinder(card_type=Scheme2)),
            AbilityFactory.AfterUnitThwartScheme(AbilityType.Response, 'YourIdentity', None, superior_taste, conditions=[lambda effect, message: (effect.this.bind_face == message.scheme)])]
