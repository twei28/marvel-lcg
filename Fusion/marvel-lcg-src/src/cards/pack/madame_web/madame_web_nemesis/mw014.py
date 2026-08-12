from . import *

# Spider-Women Hunt — custom « Kajislav », complot secondaire nemesis
# When Revealed: Place 2 additional threat here for each character with
#   "Spider" in its title in play.

def GetAbilities() -> Sequence['Ability']:

    def chasse(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(EncounterSideScheme)

        nombre = 0
        for face in Worlds.GetOnFieldCards(effect):
            if Unit2.IsType(face) and face.IsInPlay() and "Spider" in face.name:
                nombre += 1

        if nombre > 0:
            this.PlaceThreatOnSchemes([this], 2 * nombre, effect)

    return [
        AbilityFactory.WhenThisRevealed(
            None,
            chasse
        ),
    ]
