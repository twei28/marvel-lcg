from . import *

# Tech Support

def GetAbilities() -> Sequence['Ability']:

    def tech_support(effect: 'Effect', message: 'Message.AfterCardRemovedCounter') -> None:
        this = effect.this.CastTo(Support)
        Unused(this)

        Faces.ReadyAll(effect.targets, effect)

    def check_a_vous(effect: 'Effect', message: 'Message.AfterCardRemovedCounter') -> bool:
        this = effect.this.CastTo(Support)
        player = this.GetControlByPlayer()
        return player is not None and message.trigger.GetControlByPlayer() == player

    return [
        AbilityFactory.AfterCardRemovedCounter(
            AbilityType.Response,
            None,
            'counter',
            tech_support,
            conditions=[check_a_vous],
        ).SetCostFunc(CostFunc.Exhaust("This"))
        .SetCostFunc(CostFunc.Counter("This", 1, 'stimulant'))
        .SetTarget(CardFinder(trait="S.H.I.E.L.D."), canbe_ready=True),
    ]
