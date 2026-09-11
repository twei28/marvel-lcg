from . import *

# The Mother of Night (manigance annexe, 1 menace, boost 3, alea)
# When Revealed: Each player search their deck and discard pile for 2 cards
# with printed [energy] icons and place them facedown under here. Place 1
# additional threat here for each facedown card placed this way.
# When Defeated: Return each facedown card here to its owner's discard pile.
#
# Modeles : 01166 Highway Robbery (cartes face cachee sous une manigance,
# `PlaceCardHere` + `GetPlacedCardArea`, rendu a la defaite), 03001b pour
# `Search.PlayerCard` deck + defausse. `Hazard` est une base automatique.
#
# ⚠ Etape 8 bis de PROCESSUS-CARTE : cette carte GLISSE des cartes sous elle,
# ce que le plateau doit DESSINER (lecon Contingency Plan). Cas plateau exige.

def GetAbilities() -> Sequence['Ability']:

    def mother_of_night_revealed(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(EncounterSideScheme)

        def chercher(joueur: 'Player') -> List['CardFace']:
            trouvees: List['CardFace'] = []
            for _ in range(2):
                face = Search.PlayerCard(
                    effect,
                    joueur,
                    include_player_deck=True,
                    include_discard_pile=True,
                    has_printed_res="Y",
                )
                if face is None:
                    break
                trouvees.append(face)
            return trouvees

        faces: List['CardFace'] = Players.ForEachPlayer(effect, chercher, [])
        if faces:
            this.PlaceCardHere(faces, False, effect)
            this.PlaceThreatOnSchemes([this], len(faces), effect)

    def mother_of_night_defeated(effect: 'Effect', message: 'Message.WhenSchemeBeDefeated') -> None:
        this = effect.this.CastTo(EncounterSideScheme)
        faces = this.GetPlacedCardArea().Get(True)
        if faces:
            Faces.DiscardAll(faces, effect)

    return [
        AbilityFactory.WhenThisRevealed(
            None,
            mother_of_night_revealed,
        ),
        AbilityFactory.WhenSchemeBeDefeated(
            AbilityType.WhenDefeated,
            "This",
            mother_of_night_defeated,
        ),
    ]
