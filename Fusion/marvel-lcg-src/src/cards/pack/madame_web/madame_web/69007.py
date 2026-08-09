from . import *

# * Life-Support System — custom « Kajislav »
# You get +3 hit points.
# Cassandra Webb gets +1 REC.
# Interrupt: When you would be defeated by discarding this card, set your hit
#   point dial to 1 instead.
#
# Le +1 REC est porte par "You" : seule la face alter-ego (Cassandra Webb)
# possede une valeur REC, le bonus n'a donc d'effet que sous cette forme.

def GetAbilities() -> Sequence['Ability']:

    def systeme_de_survie(effect: 'Effect', message: 'Message.WhenUnitWouldBeDefeated') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(this)

        message.SetBeInstead(effect)
        for target in effect.targets:
            target.SetHealth(1, effect)

    return [
        *AbilityFactory.GiveKeywordToAttached(
            "You",
            health=3,
            recover=1,
        ),
        AbilityFactory.WhenUnitWouldBeDefeated(
            AbilityType.Interrupt,
            "YourIdentity",
            systeme_de_survie
        ).SetCostFunc(CostFunc.Discard("This"))
        .SetTarget("YourIdentity"),
    ]
