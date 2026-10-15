from . import *

# Hy'lt Minor — ENVIRONNEMENT PLANET (Skrull Empire, paquet PLANET). LOCATION. PLANET.
# Each identity gets -1 REC.
#
# Carte(s) de reference : **`st005b`** Sentinel (`GiveKeywordToInPlayWhenApplyThis(..., hand_size=-1)`), ici `recover=-1` sur `Identity`.
#
# ⚠ « Each **identity** » : tous les joueurs ; REC n'existe qu'en alter-ego.
# ⚠ Commun aux 9 planetes : Incite Rebellion (environnement Skrull Empire) peut
# traiter le texte comme VIDE jusqu'a la fin du round ; les capacites continues
# s'eteignent alors (event/manager.py et on_while.py lisent is_treat_as_if_blank).


def GetAbilities() -> Sequence['Ability']:

    return [
        *AbilityFactory.GiveKeywordToInPlayWhenApplyThis(CardFinder(card_type=Identity), recover=-1),
    ]
