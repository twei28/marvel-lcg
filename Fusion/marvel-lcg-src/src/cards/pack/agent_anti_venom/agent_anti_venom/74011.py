from . import *

# One Man Army — custom « DesignHacker »
# Interrupt: When Agent Anti-Venom uses a basic power, if there are no allies
#   under your control, draw 1 card and heal 1 damage from Agent Anti-Venom.
#   (Limit once per round.)

def GetAbilities() -> Sequence['Ability']:

    def one_man_army(effect: 'Effect', message: 'Message.WhenUnitUseBasicPower') -> None:
        this = effect.this.CastTo(Upgrade)

        initiator = effect.GetInitiator()
        initiator.DrawUp(1, effect)

        identity = GetAgentAntiVenom(effect)
        if identity is not None:
            this.HealthUnits([identity], 1, effect)

    def sans_allie(effect: 'Effect', message: 'Message.WhenUnitUseBasicPower') -> bool:
        initiator = effect.GetInitiator()
        return initiator is not None and not initiator.GetControlAllies()

    return [
        AbilityFactory.WhenUnitUseBasicPower(
            AbilityType.Interrupt,
            "You",
            one_man_army,
            conditions=[sans_allie],
        ).LimitOncePerRound(),
    ]
