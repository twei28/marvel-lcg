from . import *

# Heir to the Throne 2A — complot principal, face A.
# When Revealed: If Lord Kl'rt is in play, deal each player a facedown encounter
#   card. Otherwise, search the encounter deck and discard pile for Lord Kl'rt
#   and attach it to Super-Skrull. Shuffle the encounter deck.
#
# Cartes de reference :
#  - **`04077`** Absorbing Man (stade II) : « If X is in play, deal 1 encounter
#    card to each player. Otherwise, search the encounter deck and discard pile
#    for X and reveal it » — `Players.ForEachPlayer` + `Search.EncounterCard(
#    include_discard_pile=True, name=...)`.
#  - **`hunting_season/vulture` AttacherAVulture** : un attachement « Attach to
#    <vilain> » s'accroche seul quand on le met en jeu (ici `PutIntoPlay`, le
#    `AttachToFaceWhenPutIntoPlay` de sk127 choisit le Super-Skrull).
#
# ⚠ Mots-pieges : « EACH player » (tous les joueurs) ; « FACEDOWN encounter
# card » (distribuee, revelee a l'etape 4) ; « search the encounter deck AND
# discard pile » ; « attach it » = mise en jeu, pas revelation (aucun When
# Revealed ne part) ; « Shuffle the encounter deck » : phrase SEPAREE, donc
# melange dans les DEUX branches (le melange de la recherche ne suffit pas a la
# branche « Lord Kl'rt est deja en jeu »).


def GetAbilities() -> Sequence['Ability']:

    def heritier(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        Unused(message)
        klrt = Worlds.FindCardOnField(effect, name=NOM_KLRT, card_type=Attachment)
        if klrt is not None:
            Players.ForEachPlayer(effect, lambda joueur: joueur.DealEncounterCards(1, effect))
        else:
            premier = Worlds.GetFirstPlayer(effect)
            face = Search.EncounterCard(effect, premier, include_discard_pile=True, name=NOM_KLRT, card_type=Attachment)
            if face is not None:
                face.PutIntoPlay(premier, effect)
        Worlds.GetEncounterDeck(effect).Shuffle(effect)

    return [
        AbilityFactory.WhenThisRevealed(None, heritier),
    ]
