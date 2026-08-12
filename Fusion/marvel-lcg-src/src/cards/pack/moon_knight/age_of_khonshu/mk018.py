from . import *

# * Ghost Rider — custom « DesignHacker » (Age of Khonshu)
# Victory 1. Villainous.
# [star] Ghost Rider's attacks gain piercing and overkill.
# When Defeated: The player who defeats Ghost Rider puts The Hell Charger into
#   play under their control.


def GetAbilities() -> Sequence['Ability']:

    def percant_et_deferlant(effect: 'Effect', message: 'Message.WhenUnitWouldAttack') -> None:
        message.GainPiercing(effect)
        message.GainOverKill(effect)

    return [
        AbilityFactory.WhenUnitMakeAttack(
            AbilityType.ForcedInterrupt,
            "This",
            percant_et_deferlant,
        ),
        CapaciteArtefactLie("mk023"),
    ]
