from . import *
def GetAbilities() -> Sequence['Ability']:
    def jarvis(effect: 'Effect', message: 'Message.AfterUnitChangeForm') -> None:
        this = effect.this.CastTo(Support)
        Unused(this)
        identity = message.trigger
        player = identity.GetControlByPlayer()
        def rec_bonus(targets: Sequence['CardFace']):
            identity.CastTo(Unit2).TemporaryGain(effect, None, Message.WhenPhaseEnd, recover=2)
        def discard_status(targets: Sequence['CardFace']):
            status = list(identity.components.status.GetDeck().Get(True))
            if not status:
                return
            def act(chosen: Sequence['CardFace']):
                Faces.DiscardAll(list(chosen), effect)
            player.ChooseAbilities(effect, AbilityFactory.ForChoiceAbility('Discard a status card', act).SetTarget(status, range=(1, 1), not_move=True))
        player.ChooseAbilities(effect,
            AbilityFactory.ForChoiceAbility('That identity gets +2 REC until the end of the phase', rec_bonus),
            AbilityFactory.ForChoiceAbility('Discard a status card from that identity', discard_status))
    def check_avenger(effect: 'Effect', message: 'Message.AfterUnitChangeForm') -> bool:
        player = message.trigger.GetControlByPlayer()
        if not player:
            return False
        for face in player.GetAllIdentityFace():
            if Hero.IsType(face) and face.HasTrait('AVENGER'):
                return True
        return False
    return [AbilityFactory.CanPlayThisSupportCard(),
            AbilityFactory.AfterUnitChangeForm(AbilityType.Response, None, jarvis, to_form=AlterEgo, conditions=[check_avenger]).SetCostFunc(CostFunc.Exhaust('This'))]
