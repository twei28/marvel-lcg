from . import *

# Physical Training — custom « Rainy »
# You get +2 hit points.
# Agent 13 gets +1 ATK.
#
# Modele : Adamantium Skeleton (35004, Wolverine), meme idiome « You get +N
# hit points. [Nom du heros] gets +1 ATK. » porte par un Upgrade non attache
# (pas de cible a choisir), via deux appels a GiveKeywordToAttached : un sur
# "You" pour les PV, un sur `CardFinder(name=...)` pour le bonus de
# statistique propre a la face heros nommee.
#
# Traits CONDITION et SKILL sur un Upgrade : verifie contre l'enumeration
# TRAITS (src/game/card/face/card_face.py) le 7/8/2026, les deux y figurent
# deja (lignes "SKILL" et "CONDITION"), rien a signaler.

def GetAbilities() -> Sequence['Ability']:

    return [
        *AbilityFactory.GiveKeywordToAttached(
            "You",
            health=2,
        ),
        *AbilityFactory.GiveKeywordToAttached(
            CardFinder(name="Agent 13"),
            attack=1,
        ),
    ]
