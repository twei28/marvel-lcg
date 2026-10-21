from . import *

# Bank Robbery — MANIGANCE ANNEXE. Menace 3 par joueur, Acceleration, Boost 2.
# When Revealed : Each player tucks a random card from their hand under this scheme.
# When Defeated : Return each card tucked here to its owner's hand.
#
# Cartes de reference : `01166` Highway Robbery (meme mecanique exacte : `Players.ForEachPlayer(effect, action, [])` + `PlaceCardHere` + `ReturnToHand
# ("Owner")`), tuck.md. Icone Acceleration : desc.
# ⚠ « each player » : tous les joueurs de la partie, pas ceux de la zone ; la carte glissee est TIREE AU HASARD ; rendue a SON PROPRIETAIRE.

def GetAbilities() -> Sequence['Ability']:

    def revele(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(EncounterSideScheme)
        faces: List['CardFace'] = []
        for joueur in TousLesJoueurs(effect):
            faces += list(joueur.GetRandomHandCards(1))
        this.PlaceCardHere(faces, False, effect)

    def vaincue(effect: 'Effect', message: 'Message.WhenSchemeBeDefeated') -> None:
        this = effect.this.CastTo(EncounterSideScheme)
        Faces.ReturnToHand(this.GetPlacedCardArea().Get(True), "Owner", effect)

    return [
        AbilityFactory.WhenThisRevealed(None, revele),
        AbilityFactory.WhenSchemeBeDefeated(AbilityType.WhenDefeated, "This", vaincue),
    ]
