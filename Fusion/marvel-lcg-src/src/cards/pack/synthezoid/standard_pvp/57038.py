from . import *
def GetAbilities() -> Sequence['Ability']:
    def boost_op(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        message.GainBoostIcon(Worlds.GetPlayerNumIcon(effect), effect)
    def when_revealed(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Treachery)
        Unused(this)
        player = message.GetToPlayer()
        player.DealEncounterCards(1, effect)
    return [AbilityFactory.WhenCardBecomeBoost('This', boost_op), AbilityFactory.WhenThisRevealed(None, when_revealed)]
