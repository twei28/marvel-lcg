from . import *

# Queen of the Frozen Wastes — SIDE SCHEME, RED SONJA NEMESIS (1/5). Menace
# de depart 2 par joueur.
# Players cannot ready WEAPON upgrades.
#
# CARTE DE REFERENCE : `deadpool/44032.py` The Merc with the Mouth,
# `AbilityFactory.WhenCardWouldReady(AbilityType.NonKeyword, ...,
# lambda effect, message: message.SetBeInstead(effect))` pour empecher
# TOUT redressement d'une carte filtree.
#
# TEXTE CONTRE CODE : « Players » (pas « you ») : `control_by="AnyPlayer"`
# (valeur par defaut de la fabrique), aucune restriction de joueur.

def GetAbilities() -> Sequence['Ability']:

    return [
        AbilityFactory.WhenCardWouldReady(
            AbilityType.NonKeyword,
            CardFinder(card_type=Upgrade, trait="WEAPON"),
            lambda effect, message: message.SetBeInstead(effect),
        ),
    ]
