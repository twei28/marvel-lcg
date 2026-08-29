from . import *
def GetAbilities() -> Sequence['Ability']:
    def hellcat(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Ally)
        player = effect.GetInitiator()
        this.PutIntoPlay(player, effect)
        this.effect.RegisterTemp(
            AbilityFactory.AfterPhaseEnd(AbilityType.Temp0, None, lambda e, m: Faces.DiscardAll([this], e)),
            unregister_after_exec=True,
        )
    def check_defender(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> bool:
        identity = effect.GetInitiator().GetIdentity()
        return bool(identity and identity.HasTrait('DEFENDER'))
    return [
        AbilityFactory.WhenInYourPlayTurn(AbilityType.Action, hellcat, conditions=[check_defender]).SetPlay(),
    ]
