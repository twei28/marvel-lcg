from . import *

# Infected — custom « DesignHacker » (attachement)
# Attach to the minion with the highest printed hit points. If there are no
#   minions in play, this card gains surge.
# Attached minion's attacks gain overkill.
#
# Le +1 ATK est porte par la cle `ATK+` de cards.json, comme Concussion
# Blasters (01153) ; l'attachement lui-meme suit Genetically Enhanced (01163).

def GetAbilities() -> Sequence['Ability']:

    return [
        AbilityFactory.AttachToFaceWhenPutIntoPlay(
            Minion,
            highest_printed_hp=True,
            if_cannot_gain_surge=True,
        ),

        AbilityFactory.UnitAttackGainKeyword(
            "AttachedMinion",
            overkill=True,
        ),
    ]
