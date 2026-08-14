from . import *

# * Electro (sbire, 13/24)

def GetAbilities() -> Sequence['Ability']:

    def complot(effect: 'Effect', message: 'Message.AfterUnitSchemeEnd') -> None:
        # « [star] Forced Response: After Electro schemes, discard the top 7
        # cards of the encounter deck. »
        Worlds.DiscardEncounterCards(7, effect)

    def defaite(effect: 'Effect', message: 'Message.WhenUnitBeDefeated') -> None:
        # « When Defeated: Deal 4 damage to the villain. »
        this = effect.this.CastTo(Minion)
        villain = Worlds.FindVillain(effect)
        if villain:
            this.DealDamage([villain], 4, effect)

    return [
        AbilityFactory.AfterUnitSchemeEnd(
            AbilityType.ForcedResponse,
            "This",
            complot
        ),
        AbilityFactory.WhenUnitBeDefeated(
            AbilityType.WhenDefeated,
            "This",
            defaite
        ),
    ]
