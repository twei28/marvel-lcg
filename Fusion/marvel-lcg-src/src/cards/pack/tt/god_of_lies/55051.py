from . import *
def GetAbilities() -> Sequence['Ability']:
    def when_revealed(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Treachery)
        Unused(this)
        player = message.GetToPlayer()
        avatar = FindAvatarOfLoki(effect)
        others = GetSetAsideAvatars(effect)
        if avatar and others:
            new_avatar = Rand.RandomChoice(others, effect)
            avatar.card.SwapCard(new_avatar, effect)
        avatar = FindAvatarOfLoki(effect)
        if not avatar:
            return
        name = avatar.paper.name
        expert = Worlds.IsExpert(effect)
        if name in ('Loki the Knave', 'Loki the Miscreant'):
            avatar.DoSchemes(player, effect, property=(SchemeProperty(additional_value=1) if expert else None))
            return
        if name in ('Loki the Rascal', 'Loki the Wretch'):
            avatar.DoAttackYou(player, effect, property=(AttackProperty(additional_value=1) if expert else None))
            return
    return [AbilityFactory.WhenThisRevealed(None, when_revealed)]
