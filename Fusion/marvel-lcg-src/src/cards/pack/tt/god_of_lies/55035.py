from . import *
def GetAbilities() -> Sequence['Ability']:
    def when_revealed(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Attachment)
        Unused(this)
        player = message.GetToPlayer()
        Faces.ExhaustAll([player.GetIdentity()], effect)
    def discard_this(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Attachment)
        Faces.DiscardAll([this], effect)
        PlaceShatterCountersOnTheAvatarOfLokivillain(1, effect)
    return [AbilityFactory.AttachToFaceWhenPutIntoPlay('YourIdentity'),
            AbilityFactory.WhenThisRevealed(None, when_revealed),
            *AbilityFactory.PlayersCannotReadyCardWhile('AnyPlayer', 'AttachedIdentity', 'AnyPlayer'),
            AbilityFactory.WhenInYourPlayTurn(AbilityType.HeroAction, discard_this).SetCost(Cost('2', same_type=True))]
