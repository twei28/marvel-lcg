from . import *

# * Deadpool

def GetAbilities() -> Sequence['Ability']:

    def deadpool(effect: 'Effect', message: 'Message.AfterCardEnterPlay') -> None:
        this = effect.this.CastTo(Ally)
        Unused(this)

        initiator = effect.GetInitiator()
        initiator.DealEncounterCards(1, effect)

    return [
        AbilityFactory.AfterCardEnterPlay(
            AbilityType.ForcedResponse,
            "This",
            deadpool
        ),
    ]
