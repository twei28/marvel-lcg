from . import *

# Consolidate Power (side scheme)
# Forced Response: After a minion is defeated, give it to the villain as a
#   facedown boost card.
#
# Modele : 56091 Dangerous Recruits (GiveBoostCard sur le leader ennemi) ; ici
# le vilain actif (Worlds.FindVillain). Le texte dit Forced RESPONSE, on
# s'accroche donc a AfterUnitBeDefeated et non a l'interruption du modele.

def GetAbilities() -> Sequence['Ability']:

    def au_vilain(effect: 'Effect', message: 'Message.AfterUnitBeDefeated') -> None:
        vilain = Worlds.FindVillain(effect)
        if vilain:
            vilain.GiveBoostCard(message.trigger, effect)

    return [
        AbilityFactory.AfterUnitBeDefeated(
            AbilityType.ForcedResponse,
            Minion,
            au_vilain,
        ),
    ]
