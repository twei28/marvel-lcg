from . import *
# Hepzibah's Spacesuit. Amelioration ARMOR TECH, cout 2.
#
# You can control 1 additional upgrade that has the restricted keyword.
# Hero Resource: Exhaust Hepzibah's Spacesuit -> generate a [wild] resource for an event.
#
# Carte de reference : 48005 Prehensile Tail (MEME paire : `GiveKeywordToAttached(.., control_additional_restricted=..)` +
# `CanGenerateResources(.., for_card=CardFinder(card_type=Event))`), 20001a Venom. « Hero Resource » = `AbilityType.HeroResource`.
def GetAbilities() -> Sequence['Ability']:
    return [
        *AbilityFactory.GiveKeywordToAttached(
            "You",
            control_additional_restricted=CardFinder(card_type=Upgrade),
        ),
        AbilityFactory.CanGenerateResources(
            AbilityType.HeroResource,
            Resources("G"),
            for_card=CardFinder(card_type=Event),
        ).SetCostFunc(CostFunc.Exhaust("This")),
    ]
