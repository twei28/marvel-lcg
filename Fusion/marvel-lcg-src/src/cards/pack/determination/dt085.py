from . import *

# * ForgetMeNot

def GetAbilities() -> Sequence['Ability']:

    def check_degats_determination(effect: 'Effect', message: 'Message.AfterUnitTookDamage') -> bool:
        this = effect.this.CastTo(Ally)
        player = this.GetControlByPlayer()
        if player is None or message.trigger != player.GetIdentity():
            return False
        source = message.source
        return source is not None and source.paper.card_class == "Determination"

    def forget_me_not(effect: 'Effect', message: 'Message.AfterUnitTookDamage') -> None:
        this = effect.this.CastTo(Ally)

        player = this.GetControlByPlayer()
        if player:
            this.HealthUnits([player.GetIdentity()], 2, effect)

    return [
        *AbilityFactory.ThisNotCountAllyLimit(),
        AbilityFactory.AfterUnitTookDamage(
            AbilityType.Response,
            None,
            forget_me_not,
            conditions=[check_degats_determination],
        ).SetCostFunc(CostFunc.DealDamage(1, "This")),
    ]
