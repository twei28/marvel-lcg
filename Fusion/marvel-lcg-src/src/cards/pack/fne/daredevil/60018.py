from . import *
def GetAbilities() -> Sequence['Ability']:
    def man_without_fear(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Upgrade)
        initiator = effect.GetInitiator()
        identity = initiator.GetIdentity()
        identity.CastTo(Unit2).TakeDamage(this, 1, effect)
        def play_sense(targets: Sequence['CardFace']):
            PlaySenseUpgradeFree(initiator, effect)
        def ready_dd(targets: Sequence['CardFace']):
            Faces.ReadyAll([initiator.GetIdentity()], effect)
        initiator.ChooseAbilities(effect,
            AbilityFactory.ForChoiceAbility('Choose any upgrade from the Sense deck and play it, ignoring its resource cost', play_sense),
            AbilityFactory.ForChoiceAbility('Ready Daredevil', ready_dd))
    return [AbilityFactory.CanPlayThisUpgradeCard(),
            AbilityFactory.WhenInYourPlayTurn(AbilityType.HeroAction, man_without_fear).SetCostFunc(CostFunc.Exhaust('This'))]
