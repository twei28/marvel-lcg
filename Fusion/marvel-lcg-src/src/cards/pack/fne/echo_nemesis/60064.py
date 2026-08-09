from . import *
def GetAbilities() -> Sequence['Ability']:
    def pawn_alter_ego(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Treachery)
        Unused(this)
        player = message.GetToPlayer()
        kingpin = Worlds.FindCardOnField(effect, name='Kingpin', card_type=Minion)
        if kingpin:
            kingpin.DoSchemes(player, effect)
            return
        ThisCardGainSurge(effect, message)
    def pawn_hero(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Treachery)
        player = message.GetToPlayer()
        value = player.GetHero().attack
        if (value <= 0):
            return
        heroes = [p.GetIdentity() for p in Worlds.GetPlayers(effect) if Hero.IsType(p.GetIdentity())]
        if not heroes:
            return
        if (len(heroes) == 1):
            this.DealDamage(heroes, value, effect)
            return
        def act(chosen: Sequence['CardFace']):
            this.DealDamage(list(chosen), value, effect)
        player.ChooseAbilities(effect, AbilityFactory.ForChoiceAbility('Deal the damage to a hero', act).SetTarget(heroes, range=(1, 1), not_move=True))
    return [AbilityFactory.WhenThisRevealed('Alter-Ego', pawn_alter_ego),
            AbilityFactory.WhenThisRevealed('Hero', pawn_hero)]
