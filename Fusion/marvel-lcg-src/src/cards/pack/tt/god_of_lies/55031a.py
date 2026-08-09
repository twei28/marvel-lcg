from . import *
def GetAbilities() -> Sequence['Ability']:
    def knave(effect: 'Effect', message: 'Message.WhenPlayerRevealCard') -> None:
        this = effect.this.CastTo(Villain)
        player = message.GetToPlayer()
        identity = player.GetIdentity()
        this.DealDamage([identity], 1, effect)
        ally = player.allies.FindCard(card_type=Ally)
        if ally:
            this.DealDamage([ally], 1, effect)
    return [AbilityFactory.WhenUnitWouldBeDefeated(AbilityType.ForcedInterrupt, 'This', AvatarWouldBeDefeated),
            AbilityFactory.WhenPlayerRevealCard(AbilityType.ForcedResponse, 'AnyPlayer', Treachery, 'WhenRevealed', knave, from_encounter=True)]
