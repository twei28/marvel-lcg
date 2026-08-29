from . import *

# Finding the Perfect LMD — side scheme nemesis de Hawkeye (Kate Bishop)
# Madame Masque has managed to get her hands on more Life Model Decoys and is
#   causing havoc with your image!
# While this scheme is in play, threat cannot be prevented from being placed
#   on a scheme and Madame Masque cannot take damage.
#
# « Madame Masque cannot take damage » : AbilityFactory.UnitCannotTakeDamageWhile
# (damage.py:262), cible par CardFinder(name=...).
#
# TODO connu (limite moteur) : « threat cannot be prevented from being
# placed on a scheme » n'a pas d'equivalent moteur -- aucune carte du depot
# n'empeche une prevention de menace de s'appliquer (contrairement aux
# degats, ou `UnitCannotTakeDamageWhile` existe). Implementer proprement
# demanderait d'intercepter en priorite absolue tous les Interrupts qui
# appellent `WhenSchemeWouldPlaceThreat.PreventThreat` -- hors budget de
# cette session. Seul le texte de la carte porte cette clause pour l'instant.


def GetAbilities() -> Sequence['Ability']:

    return [
        AbilityFactory.UnitCannotTakeDamageWhile(
            AbilityType.NonKeyword,
            CardFinder(name="Madame Masque"),
        ),
    ]
