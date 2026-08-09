from . import *
def GetAbilities() -> Sequence['Ability']:
    def fortitude(effect: 'Effect', message: 'Message.WhenPlayerPayingResources') -> None:
        this = effect.this.CastTo(Upgrade)
        player = this.GetControlByPlayer()
        def stun(targets: Sequence['CardFace']):
            Faces.GiveStatus(list(targets), 'Stunned', effect)
        player.ChooseAbilities(effect, AbilityFactory.ForChoiceAbility('Stun an enemy', stun).SetTarget(Enemy))
        Faces.RemoveAllFromGame([this], effect)
    return [AbilityFactory.CanPlayThisUpgradeCard(),
            AbilityFactory.CanGenerateResources(AbilityType.HeroResource, Resources('GG'), for_card=(CardFinder(card_type=Event, trait='TACTIC') | CardFinder(card_type=Event, trait='THWART')), is_play_card=True, ex_operation=fortitude)]
