from . import *

# * Raksor — SBIRE (Kree-Skrull War). ELITE. SKRULL. SCH 2, ATK 2, 4 PV, 2 icones Y.
# When Revealed: Search the encounter deck and discard pile for Bel-Dann and put
#   him into play engaged with you.
#
# Carte de reference : **`sk136`** Bel-Dann (miroir exact), helper `MettreEnJeuEngage`
# du set ; `sk112` / `27141` pour la recherche, `sk083a` pour `PutIntoPlay`.
#
# ⚠ Mots-pieges : identiques a Bel-Dann (mis en jeu, pas revele ; engage avec
# « you » ; deck ET defausse).


def GetAbilities() -> Sequence['Ability']:

    def renfort(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        MettreEnJeuEngage(effect, message.GetToPlayer(), "Bel-Dann")

    return [
        AbilityFactory.WhenThisRevealed(None, renfort),
    ]
