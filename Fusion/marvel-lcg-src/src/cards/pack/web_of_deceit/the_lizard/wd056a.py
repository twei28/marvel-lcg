from . import *

# The Cure (2A)

def GetAbilities() -> Sequence['Ability']:

    def revelation(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        # « When Revealed: Place 1 formula counter on The Lizard. Search the
        # encounter deck and discard pile for Regenerative Research and reveal
        # it. Place 2[per_hero] threat on Regenerative Research. »
        this = effect.this.CastTo(MainScheme)

        lizard = Worlds.FindVillain(effect)
        if lizard:
            Faces.PlaceCountersOn([lizard], 1, 'formula', effect)

        recherche = ChercherEtReveler(effect, name="Regenerative Research")
        if recherche:
            this.PlaceThreatOnSchemes([recherche], "2*", effect)

    return [
        AbilityFactory.WhenThisRevealed(
            None,
            revelation
        ),
    ]
