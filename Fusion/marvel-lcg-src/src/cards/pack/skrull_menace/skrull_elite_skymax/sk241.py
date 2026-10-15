from . import *

# * Skymax — SBIRE (Skrull Elite - Skymax). ELITE. SKRULL. MNG 2, ATQ 3, PV 5[per_hero], Victory 1,
# une etoile de boost (aucune icone chiffree).
# Victory 1.
# When Revealed: Shuffle all minions from the encounter discard pile into the encounter deck.
# [star] Boost: Put Skymax into play engaged with you.
#
# Cartes de reference :
#  - « Shuffle ... from the encounter discard pile into the encounter deck » : **`sk157`** Settling Scores
#    (`Worlds.GetEncounterDiscardPileCards` + `Faces.ShuffleAllTo(faces, "EncounterDeck", effect)`).
#  - Boost qui met la carte en jeu : **`hs007`** Regular Rats ; helper `MettreEnJeuEngage`.
#
# ⚠ Mots-pieges : « ALL minions » (tous les sbires de la defausse, Skrull ou non, Elite ou non ; aucun autre
# type de carte) ; « encounter DISCARD PILE » ; defausse sans sbire : rien (le deck n'est pas melange, aucune carte
# n'a bouge) ; Victory 1 natif ; « engaged with YOU ».


def GetAbilities() -> Sequence['Ability']:

    def revele(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        Unused(message)
        sbires = [f for f in Worlds.GetEncounterDiscardPileCards(effect) if Minion.IsType(f)]
        if sbires:
            Faces.ShuffleAllTo(sbires, "EncounterDeck", effect)

    def boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        MettreEnJeuEngage(effect, effect.this, message.GetToPlayer())

    return [
        AbilityFactory.WhenThisRevealed(None, revele),
        AbilityFactory.WhenCardBecomeBoost("This", boost),
    ]
