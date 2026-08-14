from . import *

# Aggressive Surveillance

def GetAbilities() -> Sequence['Ability']:

    def aerien(effect: 'Effect', message: 'Message.WhenUnitWouldThwart') -> None:
        # « Characters with the AERIAL trait remove 1 additional threat when
        # thwarting this scheme. » C'est la recompense du Wingsuit : la
        # manigance qui appelle l'helicoptere tombe plus vite si l'on vole.
        message.RemoveAdditionalThreat(1, effect)

    def defaite(effect: 'Effect', message: 'Message.WhenSchemeBeDefeated') -> None:
        # « When Defeated: Search the encounter deck and discard pile for the
        # Fisk Helicopter minion and reveal it. »
        ChercherEtReveler(effect, name="Fisk Helicopter")

    return [
        AbilityFactory.WhenUnitWouldThwart(
            AbilityType.NonKeyword,
            CardFinder(trait="AERIAL", card_type=Friend),
            aerien,
            thwarted_scheme="This",
        ),
        AbilityFactory.WhenSchemeBeDefeated(
            AbilityType.WhenDefeated,
            "This",
            defaite
        ),
    ]
