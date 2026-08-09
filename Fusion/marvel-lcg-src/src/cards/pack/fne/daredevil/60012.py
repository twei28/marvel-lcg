from . import *
def GetAbilities() -> Sequence['Ability']:
    def when_defeated(effect: 'Effect', message: 'Message.WhenSchemeBeDefeated') -> None:
        this = effect.this.CastTo(PlayerSideScheme)
        Unused(this)
        player = message.GetDefeatingPlayer()
        if not player:
            player = effect.GetInitiator()
        PlaySenseUpgradeFree(player, effect, any_number=True)
    def check_remover(effect: 'Effect', message: 'Message.WhenSchemeWouldRemoveThreat') -> bool:
        remover = message.by_effect.GetInitiator() if message.by_effect else None
        if remover and Player.IsType(remover):
            for face in remover.GetAllIdentityFace():
                if (face.paper.name in ('Daredevil', 'Matt Murdock')):
                    return False
        return True
    def cannot_remove(effect: 'Effect', message: 'Message.WhenSchemeWouldRemoveThreat') -> None:
        message.SetBeInstead(effect)
    return [AbilityFactory.CanPlayThisSchemeCard(),
            AbilityFactory.WhenSchemeWouldRemoveThreat(AbilityType.NonKeyword, 'This', cannot_remove, conditions=[check_remover]),
            AbilityFactory.WhenSchemeBeDefeated(AbilityType.WhenDefeated, 'This', when_defeated, has_defeating_player=True)]
