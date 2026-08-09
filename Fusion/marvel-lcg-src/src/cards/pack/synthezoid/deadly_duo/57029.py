from . import *
def GetAbilities() -> Sequence['Ability']:
    def boost_op(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        this = effect.this
        player = message.GetToPlayer()
        minions = list(player.engaged_minions.Get())
        if minions:
            this.CastTo(Attachment).AttachTo2(minions[0], effect)
    # `when_revealed` retire le 4/8/2026 : jamais branche, et le surge est
    # deja rendu par `if_cannot_gain_surge=True` juste en dessous.
    return [AbilityFactory.WhenCardBecomeBoost('This', boost_op), AbilityFactory.AttachToFaceWhenPutIntoPlay(Minion, if_cannot_gain_surge=True),
            *AbilityFactory.GiveKeywordToAttached(CardFinder(with_attach=True), health=4, stalwart=1)]
