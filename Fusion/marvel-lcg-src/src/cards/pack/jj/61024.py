from . import *
def GetAbilities() -> Sequence['Ability']:
    def entrapment(effect: 'Effect', message: 'Message.AfterUnitSchemeEnd') -> None:
        this = effect.this.CastTo(Upgrade)
        player = effect.GetInitiator()
        player.GetIdentity().ChangeToForm(Hero, effect)
        villain = Worlds.FindVillain(effect)
        if villain:
            this.DealDamage([villain], message.placed_threat, effect)
    return [
        AbilityFactory.AfterUnitSchemeAgainst(AbilityType.AlterEgoResponse, None, "You", entrapment)
        .SetLabel('attack').SetCostFunc(CostFunc.Discard("This")),
    ]
