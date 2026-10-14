from . import *

# hs110 * Chameleon
# A_FAIRE_CLAUDE: When an enemy would be defeated, discard Chameleon instead. Booklet FAQ: heal the defeating damage instance from that enemy, not its full HP. Use actual defeat/damage payload.
# Printed: Chameleon cannot take damage.
# Printed: <b>Forced Interrupt</b>: When Chameleon would attack, he schemes instead.
# Printed: <b>Forced Interrupt</b>: When an enemy would be defeated, discard Chameleon instead.

def GetAbilities() -> Sequence['Ability']:
    def scheme_instead(effect, message):
        message.DoSchemeInstead(effect)
    return [AbilityFactory.UnitCannotTakeDamageWhile(AbilityType.NonKeyword, "This"),
            AbilityFactory.WhenUnitWouldAttack(AbilityType.ForcedInterrupt,
                                               "This", scheme_instead)]
