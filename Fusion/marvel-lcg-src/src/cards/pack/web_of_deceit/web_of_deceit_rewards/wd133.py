from . import *

# Spider-Sense

def GetAbilities() -> Sequence['Ability']:

    def alerte(effect: 'Effect', message: 'Message.WhenUnitWouldAttack') -> None:
        # « Hero Interrupt: When the villain initiates an attack against you,
        # draw 1 card. »
        effect.GetInitiator().DrawUp(1, effect)

    return [
        AbilityFactory.WhenUnitMakeAttack(
            AbilityType.HeroInterrupt,
            Villain,
            alerte
        ),
    ]
