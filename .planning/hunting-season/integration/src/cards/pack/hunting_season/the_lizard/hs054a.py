from . import *

# hs054a * Curtis Connors
# A_FAIRE_CLAUDE: Replace attack by shame-counter placement; possibly scheme at 3; flip after scheming; preserve two-sided villain state and all attachments on stage transition.
# Printed: Curtis Connors cannot take damage.
# Printed: [star] <b>Forced Interrupt</b>: When Curtis Connors would attack, place 1 shame counter on the Reptilian Rage environment instead. If there are 3 shame counters there, Curtis Connors schemes.
# Printed: [star] <b>Forced Response</b>: After Curtis Connors schemes, flip Curtis Connors.

def GetAbilities() -> Sequence['Ability']:
    return [AbilityFactory.UnitCannotTakeDamageWhile(
        AbilityType.NonKeyword, "This")]
