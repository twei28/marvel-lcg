from . import *

# Morlock Rescue Mission (POTENTIAL ALLY, Marrow). Victory 1.
# When Revealed: Place 1 threat here for each ally in play.
# When Defeated : Marrow.
#
# Carte de reference : 32157 Magnetically Sealed (`Worlds.GetOnFieldAllies(effect)` + `this.PlaceThreatOnSchemes([this], n, effect)`).
# ⚠ « each ally in play » : TOUS les allies en jeu (de tous les joueurs).
def GetAbilities() -> Sequence['Ability']:
    def morlock(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(EncounterSideScheme)
        allies = Worlds.GetOnFieldAllies(effect)
        this.PlaceThreatOnSchemes([this], len(allies), effect)

    return [
        AbilityFactory.WhenThisRevealed(None, morlock),
        AbilitePotentialAlly("Marrow"),
    ]
