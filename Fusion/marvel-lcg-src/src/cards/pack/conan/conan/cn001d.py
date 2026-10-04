from . import *

# * King Conan — face heros. ADVENTURER. KING. THW 2 / ATK 2 / DEF 3, 11 PV, main 5.
# Crown of Aquilonia — Response: After you use a basic power, place 2 Crom
#   counters on The Cimmerian.
#
# CARTES DE REFERENCE
#  - `AbilityFactory.AfterUnitUseBasicPower(type, "This", op, powers="Hero")`
#    (factory/friend.py) : ATK, THW, DEF de base du heros.
#  - The Scarlet Citadel en vitrine : trait KING -> THW ET ATK, patrouille ET
#    garde (`CapacitesCitadelle`).
#
# TEXTE CONTRE CODE
#  « a basic power » : les trois pouvoirs de base de la face heros (le REC est
#    un pouvoir d'alter-ego, et cette capacite n'existe que sur la face heros).


def GetAbilities() -> Sequence['Ability']:

    def crown_of_aquilonia(effect: 'Effect', message: 'Message.AfterUnitUseBasicPower') -> None:
        Unused(message)
        PoserCrom(JoueurDe(effect), 2, effect)

    return [
        AbilityFactory.AfterUnitUseBasicPower(
            AbilityType.Response,
            "This",
            crown_of_aquilonia,
            powers="Hero",
        ).SetName("Crown of Aquilonia"),
        *CapacitesCitadelle(thw=True, atk=True),
    ]
