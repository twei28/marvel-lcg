from . import *
def GetAbilities() -> Sequence['Ability']:
    def summoned_back(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Treachery)
        Unused(this)
        player = message.GetToPlayer()
        faces = player.set_aside_nemesis_sets.Get()
        minions = Filter.ByType(faces, Minion, CardFinder(is_nemesis=player))
        if not minions:
            minion = Search.EncounterCard(effect, player, include_discard_pile=True, finder=CardFinder(is_nemesis=player, card_type=Minion))
            if minion:
                minions = [minion]
        for minion in minions:
            minion.Reveal(player, effect)
    return [AbilityFactory.WhenThisRevealed(None, summoned_back)]
