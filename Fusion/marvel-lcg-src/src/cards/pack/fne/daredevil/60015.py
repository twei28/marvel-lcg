from . import *
def GetAbilities() -> Sequence['Ability']:
    def nelson_and_murdock(effect: 'Effect', message: 'Message.WhenSchemeBeDefeated') -> None:
        this = effect.this.CastTo(Support)
        Unused(this)
        def action(targets: Sequence['CardFace']):
            Faces.GiveStatus(targets, 'Confused', effect)
        player = effect.GetInitiator()
        player.ChooseAbilities(effect, AbilityFactory.ForChoiceAbility('Confuse an enemy', action).SetTarget(Enemy, canbe_confused=True))
    def check_attorney(effect: 'Effect', message: 'Message.WhenSchemeBeDefeated') -> bool:
        src = message.by_effect.this if message.by_effect else None
        if src and src.HasTrait('ATTORNEY'):
            return True
        player = message.GetDefeatingPlayer()
        if not player:
            return False
        identity = player.GetIdentity()
        return bool(identity and identity.HasTrait('ATTORNEY'))
    return [AbilityFactory.CanPlayThisSupportCard(),
            AbilityFactory.WhenSchemeBeDefeated(AbilityType.Response, SchemeSide2, nelson_and_murdock, has_defeating_player=True, conditions=[check_attorney])]
