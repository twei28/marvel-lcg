from . import *

# hs143 Unleashed Beast
# A_FAIRE_CLAUDE: When Revealed: villain attacks the revealing player; no boost when player is alter-ego. Find the documented no-boost activation method in repository.
# Printed: <b>When Revealed</b>: The villain attacks you. If you are in alter-ego form, do not give the villain a boost card for this activation.
# Printed: <hr />
# Printed: [star] <b>Boost</b>: This card gets +1 boost icon ([boost]) if this activation is an attack.

def GetAbilities() -> Sequence['Ability']:
    def boost(effect, message):
        message.GainBoostIcon(1, effect)
    return [AbilityFactory.WhenCardBecomeBoost("This", boost, during_attack=True)]
