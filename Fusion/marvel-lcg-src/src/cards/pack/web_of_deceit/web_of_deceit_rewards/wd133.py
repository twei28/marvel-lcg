from . import *

# Spider-Sense

def GetAbilities() -> Sequence['Ability']:

    def alerte(effect: 'Effect', message: 'Message.WhenUnitWouldAttack') -> None:
        # « Hero Interrupt: When the villain initiates an attack against you,
        # draw 1 card. »
        effect.GetInitiator().DrawUp(1, effect)

    return [
        # ⚠ « against YOU » : sans `against_player`, le Spider-Sense sonnait
        # aussi quand le vilain frappait un AUTRE joueur. Sans effet en solo,
        # faux des qu'on est deux.
        AbilityFactory.WhenUnitWouldAttack(
            AbilityType.HeroInterrupt,
            Villain,
            alerte,
            against_player="You",
        ),
    ]
