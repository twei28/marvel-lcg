from . import *
def GetAbilities() -> Sequence['Ability']:
    def blindspot(effect: 'Effect', message: 'Message.AfterUnitThwartEnd') -> None:
        this = effect.this.CastTo(Ally)
        Unused(this)
        Faces.GiveStatus(effect.targets, 'Confused', effect)
    return [AbilityFactory.AfterUnitThwartEnd(AbilityType.Response, 'This', blindspot).SetTarget(Enemy, with_attach=Upgrade, canbe_confused=True)]
