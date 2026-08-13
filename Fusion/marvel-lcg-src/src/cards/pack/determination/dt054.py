from . import *

# * Morbius

def GetAbilities() -> Sequence['Ability']:

    def morbius(effect: 'Effect', message: 'Message.AfterCardEnterPlay') -> None:
        this = effect.this.CastTo(Ally)

        identity = effect.GetInitiator().GetIdentity()
        this.DealDamage([identity], 2, effect)

    return [
        AbilityFactory.AfterCardEnterPlay(
            AbilityType.ForcedResponse,
            "This",
            morbius
        ),
    ]
