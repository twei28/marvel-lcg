from . import *
def GetAbilities() -> Sequence['Ability']:
    def discard_and_flip(effect: 'Effect', message: 'Message.AfterUnitUseBasicPower') -> None:
        this = effect.this.CastTo(Attachment)
        Faces.DiscardAll([this], effect)
        FlipMassForm(effect)
    def check_attacked_vision(effect: 'Effect', message: 'Message.AfterUnitUseBasicPower') -> bool:
        target = effect.this.bind_face
        if not target:
            return False
        return (target in message.end_message.attacked_targets)
    return [AbilityFactory.AttachToFaceWhenPutIntoPlay(CardFinder(name='Vision', card_type=Leader)),
            *AbilityFactory.GiveKeywordToAttached(CardFinder(name='Vision', card_type=Leader), retaliate=1),
            AbilityFactory.AfterUnitUseBasicPower(AbilityType.HeroResponse, 'YourHero', discard_and_flip, powers=['ATK'], conditions=[check_attacked_vision]).SetTarget('Trigger').SetCost(Cost('YB')),
            AbilityFactory.WhenCardBecomeBoost('This', RevealThisCard)]
