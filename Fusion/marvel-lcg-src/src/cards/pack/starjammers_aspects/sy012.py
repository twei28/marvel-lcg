from . import *
# * The Starjammer (Basic, soutien 2 [energy]). STARJAMMER. VEHICLE.
# If each of your allies has the STARJAMMER trait, increase your ally limit by 1.
# Hero Interrupt: When a STARJAMMER character uses a basic power, exhaust The Starjammer → that character gets +1 to that power for
# this use.
#
# Cartes de reference : 33020 Utopia (`GiveKeywordToInPlayWhenApplyThis("You", if_each_of_your_allies_has_trait=.., ally_limit=1)`) ;
# 20010 Venom's Pistol / tg009 Frogjolnir (`WhenUnitUseBasicPower(HeroInterrupt, finder, op)` + `Exhaust("This")` +
# `message.GainValue(+1, effect)`, qui route vers ATK / THW / DEF).
# « If EACH of your allies » : sans allie, la condition est vraie (tous les allies, aucun) ; `if_each_of_your_allies_has_trait` recalcule a
# chaque changement de la zone des allies. « a STARJAMMER character » : identite OU allie portant le trait (Honorary Starjammer et
# Captain of the Starjammer le donnent).
def GetAbilities() -> Sequence['Ability']:
    def starjammer(effect: 'Effect', message: 'Message.WhenUnitUseBasicPower') -> None:
        message.GainValue(+1, effect)
    return [
        *AbilityFactory.GiveKeywordToInPlayWhenApplyThis(
            "You",
            if_each_of_your_allies_has_trait="STARJAMMER",
            ally_limit=1,
        ),
        AbilityFactory.WhenUnitUseBasicPower(
            AbilityType.HeroInterrupt,
            CardFinder(trait="STARJAMMER"),
            starjammer,
        ).SetCostFunc(CostFunc.Exhaust("This")),
    ]
