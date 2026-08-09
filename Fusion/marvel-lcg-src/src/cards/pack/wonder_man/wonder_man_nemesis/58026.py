from . import *
def GetAbilities() -> Sequence['Ability']:
    def grim_reaper(effect: 'Effect', message: 'Message.AfterUnitDefeatedUnit') -> None:
        this = effect.this.CastTo(Minion)
        Unused(this)
        ally = message.trigger
        player = ally.GetControlByPlayer()
        if player:
            player.DealEncounterCards(1, effect)
    return [AbilityFactory.AfterUnitAttackAndDefeatUnit(AbilityType.ForcedResponse, 'This', Ally, grim_reaper)]
