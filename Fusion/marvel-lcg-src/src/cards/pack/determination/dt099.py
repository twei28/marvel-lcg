from . import *

# * Marrow

def GetAbilities() -> Sequence['Ability']:

    def marrow(effect: 'Effect', message: 'Message.WhenUnitWouldAttack') -> None:
        this = effect.this.CastTo(Ally)
        Unused(this)

        initiator = effect.GetInitiator()
        face = initiator.DiscardDeckTopCard(effect)
        if face is None:
            return
        res = FacesCounter.GetPrintedResources([face])
        if res.y or res.r:
            message.GainPiercing(effect)
            message.GainRanged(effect)

    return [
        Reckless(),
        AbilityFactory.WhenUnitWouldAttack(
            AbilityType.Interrupt,
            "This",
            marrow
        ),
    ]
