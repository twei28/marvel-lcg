from . import *

# Satriani — ENVIRONNEMENT PLANET (Skrull Empire, paquet PLANET). LOCATION. PLANET.
# Each SKRULL minion gains guard.
#
# Carte(s) de reference : `GiveKeywordToInPlayWhenApplyThis(..., guard=1)` (parametre natif de la fabrique).
#
# ⚠ « gains guard » : mot-cle (fiche mots-cles/guard.md), valeur 1.
# ⚠ Commun aux 9 planetes : Incite Rebellion (environnement Skrull Empire) peut
# traiter le texte comme VIDE jusqu'a la fin du round ; les capacites continues
# s'eteignent alors (event/manager.py et on_while.py lisent is_treat_as_if_blank).


def GetAbilities() -> Sequence['Ability']:

    return [
        *AbilityFactory.GiveKeywordToInPlayWhenApplyThis(CardFinder2("SKRULL", Minion), guard=1),
    ]
