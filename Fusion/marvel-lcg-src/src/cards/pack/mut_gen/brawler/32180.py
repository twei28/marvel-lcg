from . import *
def GetAbilities() -> Sequence['Ability']:
    def war_cry(effect: 'Effect', message: 'Message.WhenPlayerPayingResources') -> None:
        this = effect.this.CastTo(Upgrade)
        player = this.GetControlByPlayer()
        Faces.GiveStatus([player.GetIdentity()], 'Tough', effect)
        Faces.RemoveAllFromGame([this], effect)
    return [AbilityFactory.CanPlayThisUpgradeCard(),
            AbilityFactory.CanGenerateResources(AbilityType.HeroResource, Resources('GG'), for_card=(CardFinder(card_type=Event, trait='ATTACK') | CardFinder(card_type=Event, trait='DEFENSE')), is_play_card=True, ex_operation=war_cry)]
