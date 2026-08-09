from . import *
def GetAbilities() -> Sequence['Ability']:
    def after_scheme(effect: 'Effect', message: 'Message.AfterUnitSchemeEnd') -> None:
        this = effect.this.CastTo(Attachment)
        Faces.DiscardAll([this], effect)
    return [AbilityFactory.AttachToFaceWhenPutIntoPlay(CardFinder(name='She-Hulk', card_type=Leader)),
            *AbilityFactory.GiveKeywordToAttached(CardFinder(name='She-Hulk', card_type=Leader), stalwart=1),
            AbilityFactory.AfterUnitSchemeEnd(AbilityType.ForcedResponse, None, after_scheme, conditions=[lambda effect, message: (message.trigger == effect.this.bind_face)]),
            AbilityFactory.WhenCardBecomeBoost('This', RevealThisCard)]
