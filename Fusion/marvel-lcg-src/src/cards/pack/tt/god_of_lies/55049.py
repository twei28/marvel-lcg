from . import *
def GetAbilities() -> Sequence['Ability']:
    def when_revealed(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Treachery)
        player = message.GetToPlayer()
        minion = Worlds.GetEncounterDiscardPile(effect).FindCard(card_type=Minion)
        if minion:
            minion.Reveal(player, effect)
            return
        this.PlaceThreatOnSchemes('MainScheme', 3, effect)
    def boost_op(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        this = effect.this.CastTo(Treachery)
        player = message.GetToPlayer()
        if not player:
            return
        num = len(player.GetControlCharacters())
        if (num > 0):
            this.PlaceThreatOnSchemes('MainScheme', num, effect)
    return [AbilityFactory.IfExpertModeThisGainKeyword(incite=1),
            AbilityFactory.WhenCardBecomeBoost('This', boost_op),
            AbilityFactory.WhenThisRevealed(None, when_revealed)]
