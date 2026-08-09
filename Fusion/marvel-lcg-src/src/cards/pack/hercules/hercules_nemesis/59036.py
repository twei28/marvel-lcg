from . import *
def GetAbilities() -> Sequence['Ability']:
    def ares(effect: 'Effect', message: 'Message.AfterUnitSchemeEnd') -> None:
        this = effect.this.CastTo(Minion)
        Unused(this)
        player = message.GetToPlayer()
        if player:
            player.DealEncounterCards(1, effect)
    return [AbilityFactory.AfterUnitSchemeEnd(AbilityType.ForcedResponse, 'This', ares)]
