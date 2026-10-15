from . import *

# Zaragz'na — ENVIRONNEMENT PLANET (Skrull Empire, paquet PLANET). LOCATION. PLANET.
# Each ally and support enters play exhausted.
#
# Carte(s) de reference : **`40171`** (Stryfe) : `CardsEnterPlayExhausted(CardFinder(card_type=Ally|Support...), joueur)`.
#
# ⚠ « Each ally and support » : de TOUS les joueurs ("AnyPlayer") ; pas les ameliorations.
# ⚠ Commun aux 9 planetes : Incite Rebellion (environnement Skrull Empire) peut
# traiter le texte comme VIDE jusqu'a la fin du round ; les capacites continues
# s'eteignent alors (event/manager.py et on_while.py lisent is_treat_as_if_blank).


def GetAbilities() -> Sequence['Ability']:

    return [
        AbilityFactory.CardsEnterPlayExhausted(CardFinder(card_type=Ally|Support), "AnyPlayer"),
    ]
