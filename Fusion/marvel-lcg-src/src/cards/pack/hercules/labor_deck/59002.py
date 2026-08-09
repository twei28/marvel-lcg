from . import *
def GetAbilities() -> Sequence['Ability']:
    def when_revealed(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Attachment)
        player = message.GetToPlayer()
        def has_6hp(effect2: 'Effect', face: 'CardFace') -> bool:
            try:
                return (int(str(face.paper.desc.get('HP', '0')).rstrip('*')) >= 6)
            except ValueError:
                return False
        minion = Worlds.FindCardOnField(effect, finder=CardFinder(non_trait='ELITE', card_type=Minion, check_effect_fn=has_6hp))
        if not minion:
            minion = Search.EncounterCard(effect, player, include_discard_pile=True, finder=CardFinder(non_trait='ELITE', card_type=Minion, check_effect_fn=has_6hp))
            if minion:
                minion.Reveal(player, effect)
        if minion:
            minion.CastTo(CanHealth).HealHealth('All', effect)
            this.AttachTo2(minion, effect)
    def check_not_hercules(effect: 'Effect', message: 'Message.WhenUnitWouldTakeDamage') -> bool:
        this = effect.this
        if (message.trigger != this.bind_face):
            return False
        source = message.source
        if source and (source.paper.name == 'Hercules'):
            return False
        return True
    def after_leave(effect: 'Effect', message: 'Message.AfterCardLeavePlay') -> None:
        this = effect.this.CastTo(Attachment)
        player = this.GetControlByOrOwner()
        if Player.IsType(player):
            Atonement(effect, player)
    return [AbilityFactory.WhenThisRevealed(None, when_revealed),
            *AbilityFactory.GiveKeywordToAttached(CardFinder(with_attach=True), health=6, trait='ELITE'),
            AbilityFactory.UnitCannotTakeDamageWhile(AbilityType.NonKeyword, None, conditions=[check_not_hercules]),
            AbilityFactory.AfterCardLeavePlay(AbilityType.ForcedResponse, 'This', after_leave).LimitOncePerPhase()]
