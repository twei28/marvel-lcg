from . import *
def GetAbilities() -> Sequence['Ability']:
    def ae(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Treachery)
        Unused(this)
        player = message.GetToPlayer()
        leader = Worlds.FindCardOnField(effect, name='She-Hulk', card_type=Leader)
        if leader:
            leader.DoSchemes(player, effect)
            Faces.GiveStatus([leader], 'Tough', effect)
    def hero(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Treachery)
        Unused(this)
        player = message.GetToPlayer()
        leader = Worlds.FindCardOnField(effect, name='She-Hulk', card_type=Leader)
        if leader:
            leader.DoAttackYou(player, effect)
            Faces.GiveStatus([leader], 'Tough', effect)
    return [AbilityFactory.WhenThisRevealed('Alter-Ego', ae),
            AbilityFactory.WhenThisRevealed('Hero', hero)]
