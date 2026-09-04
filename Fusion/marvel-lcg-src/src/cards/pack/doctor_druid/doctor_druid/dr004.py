from . import *

# Fellow Druid (x2) — SOUTIEN, cout 2, [wild]. MYSTIC. PERSONA.
# While this card is in your hand, you get +1 hand size.
# Resource: Exhaust Fellow Druid -> generate a [wild] resource for a Doctor
#   Druid card.
#
# CARTES DE REFERENCE
#  - `resources.py` `CanGenerateResources(..., for_card=)` pour une ressource
#    RESTREINTE a certaines cartes.
#  - `aa003` / `al011` pour `hand_size=` via
#    `GiveKeywordToInPlayWhenApplyThis`.
#
# TEXTE CONTRE CODE
#  « you get +1 hand size » -> le bonus va au JOUEUR, donc a son identite
#    (`"You"`), pas a la carte.
#  « for a Doctor Druid card » -> `for_card=CardFinder(set_name=SET_HEROS)` :
#    la ressource ne finance QUE les cartes du set. Sans cette restriction la
#    carte serait strictement meilleure qu'une ressource ordinaire.
#  ⚠ LA TENSION DE LA CARTE : le +1 main ne vaut QUE tant qu'elle reste en
#    main, la ressource ne vaut QUE si elle est en jeu. Les deux moities
#    s'excluent, et c'est voulu par l'auteur.


def GetAbilities() -> Sequence['Ability']:
    return [
        AbilityFactory.CanPlayThisSupportCard(),
        # ⚠ La moitie « tant que cette carte est dans votre main » n'est PAS
        # ici : elle est portee par le HEROS (dr001a), seule facon de la faire
        # fonctionner. Raison detaillee dans `__init__.py`.
        AbilityFactory.CanGenerateResources(
            AbilityType.Resource,
            Resources("G"),
            CardFinder(set_name=SET_HEROS),
        ).SetCostFunc(CostFunc.Exhaust("This")),
    ]
