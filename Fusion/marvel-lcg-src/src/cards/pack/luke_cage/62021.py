from . import *
def GetAbilities() -> Sequence['Ability']:
    def she_hulk(effect: 'Effect', message: 'Message.AfterCardEnterPlay') -> None:
        this = effect.this.CastTo(Ally)
        Unused(this)
        identity = effect.GetInitiator().GetIdentity()
        if identity:
            Faces.GiveStatus([identity], "Tough", effect)
    return [
        AbilityFactory.AfterCardEnterPlay(AbilityType.Response, "This", she_hulk),
    ]
