from . import *

# * Cable

def GetAbilities() -> Sequence['Ability']:

    def cable(effect: 'Effect', message: 'Message.WhenUnitWouldAttack') -> None:
        this = effect.this.CastTo(Ally)

        initiator = effect.GetInitiator()
        faces = initiator.DiscardHandCards((0, "All"), effect)
        if faces:
            this.GainForThisActive(effect, message, attack=len(faces))

    return [
        Reckless(),
        AbilityFactory.WhenUnitWouldAttack(
            AbilityType.Interrupt,
            "This",
            cable
        ),
    ]
