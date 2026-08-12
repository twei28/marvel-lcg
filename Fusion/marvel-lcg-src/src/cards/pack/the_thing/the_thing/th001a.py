from . import *

# * The Thing — custom « DesignHacker »
# Give 'Er — Action: Discard a tough status card from The Thing.
# Take That! — Response: After you discard a tough status card from The
# Thing, your attacks deal 1 additional damage until the end of the phase.

def GetAbilities() -> Sequence['Ability']:
    return AbilitesFaceHeros()
