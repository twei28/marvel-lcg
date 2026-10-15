from . import *

# Aks'Lo — ENVIRONNEMENT PLANET (Skrull Empire, paquet PLANET). LOCATION. PLANET.
# Each SKRULL minion gets +2 hit points.
#
# Carte(s) de reference : **`as012`** (pack meme auteur) / `GiveKeywordToInPlayWhenApplyThis(CardFinder2(trait, Minion), health=2)`.
#
# ⚠ « Each SKRULL **minion** » : pas le mechant (lui n'a pas de PV).
# ⚠ Commun aux 9 planetes : Incite Rebellion (environnement Skrull Empire) peut
# traiter le texte comme VIDE jusqu'a la fin du round ; les capacites continues
# s'eteignent alors (event/manager.py et on_while.py lisent is_treat_as_if_blank).


def GetAbilities() -> Sequence['Ability']:

    return [
        *AbilityFactory.GiveKeywordToInPlayWhenApplyThis(CardFinder2("SKRULL", Minion), health=2),
    ]
