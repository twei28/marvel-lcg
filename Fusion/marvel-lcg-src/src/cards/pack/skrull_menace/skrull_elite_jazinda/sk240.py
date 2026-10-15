from . import *

# Skrull of Royal Blood — TRAITRISE (Skrull Elite - Jazinda). Surge, aucune icone de boost.
# Surge.
# When Revealed: Shuffle all cards with the highest number of boost icons in the encounter discard
#   pile into the encounter deck.
#
# Cartes de reference :
#  - Surge : natif (`desc.Surge`, fiche mots-cles/surge.md), aucun module pour lui.
#  - « Shuffle ... from the encounter discard pile into the encounter deck » : **`sk157`** Settling Scores
#    (`Worlds.GetEncounterDiscardPileCards` + `Faces.ShuffleAllTo(faces, "EncounterDeck", effect)`).
#  - Compte des icones : **`sk106`** (`FacesCounter.CountTotalBoostIcons`).
#
# ⚠ Mots-pieges : « the HIGHEST number » (le maximum de la defausse : toutes les cartes qui l'atteignent, a
# egalite) ; « boost icons » = icones Y (pas l'etoile) ; defausse vide : rien ; un maximum de 0 (que des cartes
# sans icone) : toutes les cartes de la defausse reviennent (lecture litterale) ; « encounter discard pile »
# (pas la defausse d'un joueur).


def GetAbilities() -> Sequence['Ability']:

    def revele(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        Unused(message)
        defausse = list(Worlds.GetEncounterDiscardPileCards(effect))
        if not defausse:
            return
        icones = {f: FacesCounter.CountTotalBoostIcons([f]) for f in defausse}
        maximum = max(icones.values())
        Faces.ShuffleAllTo([f for f in defausse if icones[f] == maximum], "EncounterDeck", effect)

    return [
        AbilityFactory.WhenThisRevealed(None, revele),
    ]
