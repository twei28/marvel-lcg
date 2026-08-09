from . import *
def GetAbilities() -> Sequence['Ability']:
    def discard_this(effect: 'Effect', message: 'Message.WhenPlayerRevealCard') -> None:
        this = effect.this.CastTo(Attachment)
        Faces.DiscardAll([this], effect)
    return [AbilityFactory.AttachToFaceWhenPutIntoPlay(CardFinder(trait=AVATAR_TRAIT, card_type=Villain)),
            *AbilityFactory.GiveKeywordToAttached(CardFinder(trait=AVATAR_TRAIT, card_type=Villain), stalwart=1),
            AbilityFactory.WhenPlayerRevealCard(AbilityType.HeroResponse, 'You', Treachery, 'WhenRevealed', discard_this, from_encounter=True).SetTarget('Trigger').SetCost(Cost('2', same_type=True))]
