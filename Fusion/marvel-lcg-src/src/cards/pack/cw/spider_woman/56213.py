from . import *
def GetAbilities() -> Sequence['Ability']:
    def enter_play(effect: 'Effect', message: 'Message.WhenCardEnterPlay') -> None:
        this = effect.this.CastTo(Upgrade)
        target = this.bind_face
        if target:
            Faces.GiveStatus([target], 'Tough', effect)
    def after_attack(effect: 'Effect', message: 'Message.AfterUnitAttackEnd') -> None:
        this = effect.this.CastTo(Upgrade)
        face = Worlds.FindCardOnField(effect, name='Finesse', card_type=Attachment)
        if face:
            Faces.PlaceCountersOn([face], 2, 'skill', effect)
        Faces.DiscardAll([this], effect)
    return [AbilityFactory.CanPlayThisUpgradeCard(CardFinder(name='Spider-Woman', card_type=Leader)),
            AbilityFactory.WhenCardEnterPlay(AbilityType.ForcedResponse, 'This', enter_play),
            AbilityFactory.AfterUnitAttackEnd(AbilityType.ForcedResponse, 'AttachedCharacter', after_attack)]
