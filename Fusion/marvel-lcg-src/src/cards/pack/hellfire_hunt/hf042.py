from . import *

# Emma Frost's Redemption (manigance annexe de campagne). Victory 1. Icone Amplify (desc).
# When Defeated: The player who defeated this scheme searches the Emma Frost ally from the set-aside area and put it into play.
def GetAbilities() -> Sequence['Ability']:
    return [AbilitePotentialAlly("Emma Frost")]
