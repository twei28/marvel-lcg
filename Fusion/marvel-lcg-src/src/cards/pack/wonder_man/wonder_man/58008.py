from . import *
def GetAbilities() -> Sequence['Ability']:
    class BeltState:
        for_event = False
    def check_mode(effect: 'Effect', message: 'Message.CheckPlayerCanPayCost') -> bool:
        BeltState.for_event = Event.IsType(message.paying_for_effect.this)
        if BeltState.for_event:
            return True
        player = message.GetToPlayer()
        if (player != effect.this.GetControlByPlayer()):
            return False
        return (len(GetTuckedCards(effect, player)) > 0)
    def pay_tucked(targets: Sequence['CardFace'], effect: 'Effect') -> bool:
        if BeltState.for_event:
            return True
        player = effect.GetInitiator()
        tucked = GetTuckedCards(effect, player)
        if not tucked:
            return False
        done = {'ok': False}
        def action(chosen: Sequence['CardFace']):
            Faces.DiscardAll(list(chosen), effect)
            done['ok'] = True
        player.ChooseAbilities(effect, AbilityFactory.ForChoiceAbility('Discard a card tucked under Ionic Physiology', action).SetTarget(list(tucked), range=(1, 1), not_move=True))
        return done['ok']
    return [AbilityFactory.CanPlayThisUpgradeCard(),
            AbilityFactory.CanGenerateResources(AbilityType.HeroResource, Resources('Y'), is_play_card=True, conditions=[check_mode]).SetCostFunc(CostFunc.Exhaust('This')).SetCostFunc(CostFunc.Custom(None, pay_tucked))]
