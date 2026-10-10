from . import *

# Torrential Rain

def GetAbilities() -> Sequence['Ability']:

    def torrential_rain(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(this)

        # CORRECTIF (10/10/2026, audit Storm) : « Remove 3 threat from AMONG
        # schemes in play ». Une seule manigance visee perdait le reste des 3.
        # Modele : 34018 Mutant Peacekeepers (chaque designation = 1 menace).
        this.RemoveThreatFromSchemesTotal(effect.targets, 3, effect)

        initiator = effect.GetInitiator()
        hurricane = Worlds.FindCardOnField(
            effect,
            name="Hurricane",
            card_type=Support
        )
        if hurricane:
            hurricane.ResolveSpecialAbility(initiator, effect)


    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            torrential_rain
        ).SetPlay().SetLabel('thwart')
        .SetTarget(Scheme2, range=(1, 3), repeat_rules="Threat"),
    ]

