from . import *
def GetAbilities() -> Sequence['Ability']:
    def bodyguard(effect: 'Effect', message: 'Message.WhenPlayerPayingResources') -> None:
        this = effect.this.CastTo(Upgrade)
        player = this.GetControlByPlayer()
        player.DrawUp(1, effect)
        Faces.RemoveAllFromGame([this], effect)
    return [AbilityFactory.CanPlayThisUpgradeCard(),
            AbilityFactory.CanGenerateResources(AbilityType.HeroResource, Resources('GG'), for_card=(CardFinder(card_type=Event, trait='DEFENSE') | CardFinder(card_type=Event, trait='THWART')), is_play_card=True, ex_operation=bodyguard)]
