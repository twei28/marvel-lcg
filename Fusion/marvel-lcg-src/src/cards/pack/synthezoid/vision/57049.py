from . import *
def GetAbilities() -> Sequence['Ability']:
    def mass_increase(effect: 'Effect', message: 'Message.WhenUnitWouldAttack') -> None:
        this = effect.this.CastTo(Attachment)
        attacker = message.trigger
        message.SetBeInstead(effect)
        Faces.GiveStatus([attacker], 'Stunned', effect)
        Faces.DiscardAll([this], effect)
    def check_dense(effect: 'Effect', message: 'Message.WhenUnitWouldAttack') -> bool:
        target = effect.this.bind_face
        if not target:
            return False
        if (Worlds.FindCardOnField(effect, name='Dense', card_type=Attachment) == None):
            return False
        if not message.HasTarget(target):
            return False
        return (Hero.IsType(message.trigger) or Ally.IsType(message.trigger))
    return [AbilityFactory.AttachToFaceWhenPutIntoPlay(CardFinder(name='Vision', card_type=Leader)),
            AbilityFactory.WhenUnitWouldAttack(AbilityType.ForcedInterrupt, None, mass_increase, conditions=[check_dense])]
