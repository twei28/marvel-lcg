from . import *
def GetAbilities() -> Sequence['Ability']:
    def when_revealed(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Treachery)
        player = message.GetToPlayer()
        avatar = FindAvatarOfLoki(effect)
        if avatar:
            counters = avatar.CastTo(CanPlaceCounter).GetCounters('shatter')
            if (counters > 0):
                avatar.CastTo(CanPlaceCounter).SetCounters((counters - 1), 'shatter', effect)
        damage = (3 if Worlds.IsExpert(effect) else 2)
        this.DealDamage([player.GetIdentity()], damage, effect)
    def dirty_trick_boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        this = effect.this.CastTo(Treachery)
        player = message.GetToPlayer()
        characters = [player.GetIdentity()] + list(player.allies.Get())
        player.GetIdentity().TakeIndirectDamage(this, len(characters), effect)
    return [AbilityFactory.WhenThisRevealed(None, when_revealed),
            AbilityFactory.WhenCardBecomeBoost('This', dirty_trick_boost)]
