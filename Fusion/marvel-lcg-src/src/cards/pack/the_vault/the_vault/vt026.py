from . import *

# Burglary — MANIGANCE ANNEXE x2. Menace de depart 2[per_hero]. Crisis. 2 icones de boost.
# When Revealed: If Inspection of the Vault is in play, place 1[per_hero] additional threat here.
# When Defeated: Reveal the top card of the villain deck.
#
# Cartes de reference :
#  - Crisis : natif (desc.Crisis, fiche mots-cles/crisis.md ; icone verifiee sur le glyphe C de ChampionsIcons.ttf).
#  - « place 1[per_hero] additional threat here » : `this.PlaceThreatOnSchemes([this], n, effect)` (modele 01107 Breakin' &
#    Takin' pour la forme ; n = nombre de joueurs).
#  - « When Defeated » : `WhenSchemeBeDefeated(WhenDefeated, "This", ...)` (modele ld011) ; « Reveal the top card of the villain
#    deck » : `RevelerProchainMechant` (helper du set).
#
# ⚠ Mots-pieges : « 1[per_hero] ADDITIONAL » = 1 par joueur EN PLUS de la menace de depart ; deck de vilains vide = rien a reveler.


def GetAbilities() -> Sequence['Ability']:

    def revelee(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        Unused(message)
        this = effect.this.CastTo(EncounterSideScheme)
        if InspectionEnJeu(effect):
            this.PlaceThreatOnSchemes([this], NombreDeJoueurs(effect), effect)

    def vaincue(effect: 'Effect', message: 'Message.WhenSchemeBeDefeated') -> None:
        Unused(message)
        RevelerProchainMechant(effect, Worlds.GetFirstPlayer(effect))

    return [
        AbilityFactory.WhenThisRevealed(None, revelee),
        AbilityFactory.WhenSchemeBeDefeated(AbilityType.WhenDefeated, "This", vaincue),
    ]
