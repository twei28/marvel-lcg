from . import *

# * Iron Fist — custom « DesignHacker » (Age of Khonshu)
# Victory 1. Villainous.
# Forced Response: After Iron Fist damages a character you control, stun that
#   character.
# When Defeated: The player who defeated Iron Fist puts The Iron Fist into
#   play under their control.


def GetAbilities() -> Sequence['Ability']:

    def sonner_la_victime(effect: 'Effect', message: 'Message.AfterUnitTookDamage') -> None:
        this = effect.this.CastTo(Minion)
        Unused(this)
        victime = message.trigger
        Faces.GiveStatus([victime], "Stunned", effect)

    return [
        AbilityFactory.AfterUnitTookDamage(
            AbilityType.ForcedResponse,
            Friend,
            sonner_la_victime,
            who_dealt_damage="This",
        ),
        CapaciteArtefactLie("76024"),
    ]
