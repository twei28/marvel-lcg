from . import *

# * Death — sbire nemesis. COSMIC ENTITY. ELITE. SCH 2 / ATK 2 / PV « INF ».
# [star] Death cannot be defeated.
# Vulnerable. (Discard this character if it is stunned or confused.)
#
# Cartes de reference (RECETTES-MOTEUR) :
#  - « cannot be defeated » : 16080b * Collector, MEME phrase — desc HP
#    « INF » + `UnitCannotBeDefeatedWhile(NonKeyword, "This")`
#    (defeated.py:520) ;
#  - Vulnerable : desc, base automatique (fiche vulnerable.md) — c'est la
#    SEULE sortie, et aa015 la verrouille avec Robuste.
#
# ⚠ La carte n'imprime AUCUN PV : « INF » est l'encodage moteur du Collector
# pour la meme mecanique, pas une invention. L'etoile est codee toujours
# active (convention 04125 Red Skull).

def GetAbilities() -> Sequence['Ability']:

    return [
        *AbilityFactory.UnitCannotBeDefeatedWhile(
            AbilityType.NonKeywordStar,
            "This",
        ),
    ]
