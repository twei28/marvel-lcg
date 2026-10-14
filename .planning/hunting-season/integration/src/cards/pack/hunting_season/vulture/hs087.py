from . import *

# hs087 * Gibbon

def GetAbilities() -> Sequence['Ability']:
    def prevent(effect, message):
        message.PreventDamage(1, effect)
    return [AbilityFactory.WhenUnitWouldTakeDamage(
        AbilityType.ForcedInterrupt, "This", prevent)]
