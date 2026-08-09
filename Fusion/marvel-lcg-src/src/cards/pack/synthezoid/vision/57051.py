from . import *
def GetAbilities() -> Sequence['Ability']:
    def ae(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Treachery)
        Unused(this)
        player = message.GetToPlayer()
        leader = Worlds.FindCardOnField(effect, name='Vision', card_type=Leader)
        if leader:
            prop = None
            if Worlds.FindCardOnField(effect, name='Intangible', card_type=Attachment):
                prop = SchemeProperty(additional_value=1)
            leader.DoSchemes(player, effect, property=prop)
    def hero(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Treachery)
        Unused(this)
        player = message.GetToPlayer()
        leader = Worlds.FindCardOnField(effect, name='Vision', card_type=Leader)
        if leader:
            prop = None
            if Worlds.FindCardOnField(effect, name='Dense', card_type=Attachment):
                prop = AttackProperty(additional_value=1)
            leader.DoAttackYou(player, effect, property=prop)
    return [AbilityFactory.WhenThisRevealed('Alter-Ego', ae),
            AbilityFactory.WhenThisRevealed('Hero', hero)]
