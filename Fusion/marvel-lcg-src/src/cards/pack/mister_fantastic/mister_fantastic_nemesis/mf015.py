from . import *

# Hubris — custom « DesignHacker » (side scheme némésis de Mister Fantastic)
# When Revealed: Place X additional threat here, where X is the combined THW
# of all heroes.

def GetAbilities() -> Sequence['Ability']:

    def hubris(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(EncounterSideScheme)

        valeur = 0
        for player in list(effect.world.players):
            if player.is_eliminated:
                continue
            hero = player.GetHero()
            if hero:
                valeur += hero.thwart

        if valeur > 0:
            this.PlaceThreatOnSchemes([this], valeur, effect)

    return [
        AbilityFactory.WhenThisRevealed(
            None,
            hubris
        ),
    ]
