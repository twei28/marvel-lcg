from . import *

# Hardheaded (CONDITION)
# Attach to Hammerhead. (+1 SCH : cle desc "SCH+", base automatique.)
# Hammerhead gains stalwart.
# Hero Action: Spend [energy] [mental] [physical] resources -> discard this card.
# [star] Boost: Give the activating enemy a tough status card.
#
# Modeles : 16064 Drang's Spear (stalwart attache + action a cout), 01118 Sonic
# Converter (Cost("YBR")), 52037 Growing Strong (boost -> tough a l'ennemi actif).

def GetAbilities() -> Sequence['Ability']:

    def robuste(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        Faces.GiveStatus([message.activating_enemy], "Tough", effect)

    return [
        AbilityFactory.AttachToFaceWhenPutIntoPlay(
            CardFinder(name="Hammerhead")
        ),
        *AbilityFactory.GiveKeywordToAttached(
            CardFinder(name="Hammerhead"),
            stalwart=1,
        ),
        AbilityFactory.PlayerActionToDiscardThis(
            AbilityType.HeroAction,
        ).SetCost(Cost("YBR")),
        AbilityFactory.WhenCardBecomeBoost(
            "This",
            robuste,
        ),
    ]
