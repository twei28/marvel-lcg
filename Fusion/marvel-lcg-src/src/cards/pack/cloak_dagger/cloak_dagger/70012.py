from . import *

# Dark Intangibility — custom « DesignHacker »
# Response: After Cloak makes a basic defense, exhaust Dark Intangibility →
#   ready Cloak and he gains retaliate 1 until the end of the phase.


def GetAbilities() -> Sequence['Ability']:

    def dark_intangibility(effect: 'Effect', message: 'Message.AfterUnitDefendEnd') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(this)
        initiator = effect.GetInitiator()

        identite = initiator.GetIdentity()
        if identite is None or not Hero.IsType(identite):
            return
        Faces.ReadyAll([identite], effect)
        identite.GainUntilPhaseEnd(effect, retaliate=1)

    return [
        AbilityFactory.AfterUnitDefendEnd(
            AbilityType.HeroResponse,
            "You",
            dark_intangibility,
        ).SetCostFunc(CostFunc.Exhaust("This")),
    ]
