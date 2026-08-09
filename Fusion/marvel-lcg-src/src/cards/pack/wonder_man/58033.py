from . import *
def GetAbilities() -> Sequence['Ability']:
    def disarming_defense(effect: 'Effect', message: 'Message.WhenUnitWouldDefend') -> None:
        this = effect.this.CastTo(Event)
        Unused(this)
        initiator = effect.GetInitiator()
        attacker = message.attacker
        message.GainDEFForThisAttack(2, effect)
        def action():
            attachments = [x for x in attacker.GetAttachedAttachments() if ('Hero Action' in (x.paper.text or '')) or ('Hero Response' in (x.paper.text or ''))]
            if attachments:
                def discard(targets: Sequence['CardFace']):
                    Faces.DiscardAll(list(targets), effect)
                initiator.ChooseAbilities(effect, AbilityFactory.ForChoiceAbility('Discard an attachment', discard).SetTarget(attachments, range=(1, 1), not_move=True))
        message.IfYouTakeNoDamage(action)
    return [AbilityFactory.WhenUnitDefendAgainstAttack(AbilityType.HeroInterrupt, 'YourHero', disarming_defense).SetPlay().SetLabel('defense')]
