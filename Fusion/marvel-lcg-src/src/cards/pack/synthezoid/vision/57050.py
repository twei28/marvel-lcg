from . import *
def GetAbilities() -> Sequence['Ability']:
    def density_control(effect: 'Effect', message: 'Message.WhenEnemyWouldActivate') -> None:
        this = effect.this.CastTo(Attachment)
        target = ('Intangible' if (message.power == 'SCH') else 'Dense')
        face = FindMassForm(effect)
        if face and (face.paper.name != target):
            face.card.Flip(effect)
            Faces.DiscardAll([this], effect)
    def check_vision(effect: 'Effect', message: 'Message.WhenEnemyWouldActivate') -> bool:
        return (message.trigger == effect.this.bind_face)
    return [AbilityFactory.AttachToFaceWhenPutIntoPlay(CardFinder(name='Vision', card_type=Leader)),
            AbilityFactory.WhenEnemyWouldActivate(AbilityType.ForcedInterrupt, None, density_control, conditions=[check_vision])]
