from . import *

# Rising Sea Levels — MANIGANCE ANNEXE (ensemble Attuma). ATLANTIS. Hinder 1.
# When Revealed: Place 1 threat on the main scheme for each ATLANTIS card in play.
#
# Cartes de reference :
#  - « Place 1 threat on the main scheme for each X in play » : compte via `Worlds.FindCardsOnField` +
#    `MainScheme.PlaceThreatOnSchemes` (modele gs119 Majestrix's Verdict pour l'appel, decompte adapte).
#
# ⚠ Mots-pieges : « for each ATLANTIS card in play » compte CETTE carte elle-meme (elle porte le trait
# ATLANTIS, contrairement a gs174/gs170 qui disent « ANOTHER ») ; « the main scheme » = Earthfall
# (`Worlds.FindMainScheme`).


def GetAbilities() -> Sequence['Ability']:

    def revelee(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        Unused(message)
        complot = Worlds.FindMainScheme(effect)
        if complot is None:
            return
        n = len(Worlds.FindCardsOnField(effect, CardFinder(trait="ATLANTIS")))
        if n > 0:
            complot.PlaceThreatOnSchemes([complot], n, effect)

    return [
        AbilityFactory.WhenThisRevealed(None, revelee),
    ]
