from . import *
def GetAbilities() -> Sequence['Ability']:
    def when_revealed(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Treachery)
        player = message.GetToPlayer()
        minion = Worlds.DiscardEncounterCardsUntil(effect, card_type=Minion)
        if not minion:
            return
        if player.IsInHeroForm():
            value = int(str(minion.paper.desc.get('ATK', '0')).rstrip('*') or 0)
            if (value > 0):
                this.DealDamage([player.GetIdentity()], value, effect)
        else:
            value = int(str(minion.paper.desc.get('SCH', '0')).rstrip('*') or 0)
            if (value > 0):
                this.PlaceThreatOnSchemes('MainScheme', value, effect)
    return [AbilityFactory.WhenThisRevealed(None, when_revealed)]
