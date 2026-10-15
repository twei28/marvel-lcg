from . import *

# Tarnax VII — ENVIRONNEMENT PLANET (Skrull Empire, paquet PLANET). LOCATION. PLANET.
# Each SKRULL minion gets +1 ATK.
#
# Carte(s) de reference : `GiveKeywordToInPlayWhenApplyThis(..., attack=1)`.
#
# ⚠ « **minion** » seulement.
# ⚠ Commun aux 9 planetes : Incite Rebellion (environnement Skrull Empire) peut
# traiter le texte comme VIDE jusqu'a la fin du round ; les capacites continues
# s'eteignent alors (event/manager.py et on_while.py lisent is_treat_as_if_blank).


def GetAbilities() -> Sequence['Ability']:

    return [
        *AbilityFactory.GiveKeywordToInPlayWhenApplyThis(CardFinder2("SKRULL", Minion), attack=1),
    ]
