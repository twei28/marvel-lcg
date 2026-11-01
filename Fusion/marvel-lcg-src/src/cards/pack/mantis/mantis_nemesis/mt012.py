from . import *

# Death Blossom's Bloom : MANIGANCE ANNEXE (nemesis de Mantis), menace initiale 2 par joueur, boost 3. Incite 1.
# Enemies cannot be confused.
#
# CARTES DE REFERENCE
#  - `32147` Magneto's Helmet / `tk006b` : `AbilityFactory.UnitCannotBeConfused(CardFinder(..))` (buff `BuffCannotBeConfused`, lu par `CanbeConfused` : aucun nouveau statut ne peut etre pose).
#  - `mots-cles/incite.md` : `desc.Incite` est lu NATIVEMENT (aucun script) ; `mots-cles/stalwart.md` : le mot-cle Stoique, dont la FAQ dit « Similar to the stalwart keyword... ».
#
# TEXTE CONTRE CODE
#  « ENEMIES cannot be confused » : tous les ennemis (vilain ET sbires), tant que la manigance est en jeu. FAQ imprimee : si des ennemis SONT confus quand elle entre en jeu, ils perdent
#  immediatement toutes leurs cartes Desoriente (Stoique a la mise en jeu) : retrait a la revelation, en plus du buff qui bloque les suivantes.
#  Chiffres : menace initiale 2 par joueur (`2*`), boost 3, Incite 1 (lus dans `desc`).


def GetAbilities() -> Sequence['Ability']:

    def retirer_les_confusions(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        for ennemi in Worlds.FindCardsOnField(effect, card_type=Enemy):
            while ennemi.IsConfused() and ennemi.DiscardConfused(effect, rule="All") > 0:
                pass

    return [
        AbilityFactory.UnitCannotBeConfused(Enemy),
        AbilityFactory.WhenThisRevealed(
            None,
            retirer_les_confusions,
        ),
    ]
