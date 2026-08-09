from . import *
def GetAbilities() -> Sequence['Ability']:
    def the_rez(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Support)
        Unused(this)
        initiator = effect.GetInitiator()
        identity = initiator.GetIdentity()
        value = 0
        for face in identity.GetPlacedCardArea().Get():
            value = max(value, GetPrintedCostValue(face))
        if (value > 0):
            identity.HealHealth(value, effect)
    return [AbilityFactory.CanPlayThisSupportCard(),
            AbilityFactory.WhenInYourPlayTurn(AbilityType.AlterEgoAction, the_rez).SetCostFunc(CostFunc.Exhaust('This'))]
