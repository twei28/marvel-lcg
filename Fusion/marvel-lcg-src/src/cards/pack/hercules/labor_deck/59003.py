from . import *
def GetAbilities() -> Sequence['Ability']:
    def when_revealed(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Attachment)
        player = message.GetToPlayer()
        # Meme oubli que 59002, et meme correctif : le set nemesis mis de cote
        # porte 59038 Olympic Feud, un complot annexe de rencontre. Voir le
        # commentaire de 59002 pour la regle « Find ».
        scheme = Search.EncounterCard(effect, player, include_discard_pile=True, include_set_aside=True, card_type=EncounterSideScheme)
        if scheme:
            scheme.Reveal(player, effect)
            this.AttachTo2(scheme, effect)
            this.PlaceThreatOnSchemes([scheme], 6, effect)
    def cannot_remove(effect: 'Effect', message: 'Message.WhenSchemeWouldRemoveThreat') -> None:
        message.SetBeInstead(effect)
    def check_not_hercules(effect: 'Effect', message: 'Message.WhenSchemeWouldRemoveThreat') -> bool:
        this = effect.this
        if (message.trigger != this.bind_face):
            return False
        remover = message.by_effect.GetInitiator() if message.by_effect else None
        if remover and remover.GetIdentity() and remover.GetIdentity().IsName('Hercules'):
            return False
        return True
    def after_leave(effect: 'Effect', message: 'Message.AfterCardLeavePlay') -> None:
        this = effect.this.CastTo(Attachment)
        player = this.GetControlByOrOwner()
        if Player.IsType(player):
            Atonement(effect, player)
    return [AbilityFactory.WhenThisRevealed(None, when_revealed),
            *AbilityFactory.GiveKeywordToAttached(CardFinder(with_attach=True), assault=1),
            AbilityFactory.WhenSchemeWouldRemoveThreat(AbilityType.NonKeyword, None, cannot_remove, conditions=[check_not_hercules]),
            AbilityFactory.AfterCardLeavePlay(AbilityType.ForcedResponse, 'This', after_leave).LimitOncePerPhase()]
