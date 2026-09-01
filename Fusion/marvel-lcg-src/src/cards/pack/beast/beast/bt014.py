from . import *

# * Peter Parker — Lab Assistant. Allie Discovery (1/5). CIVILIAN. GENIUS.
# Cout 2, 3 PV, CTR 2*, ATQ 0.
# Action: Exhaust this card -> generate a [wild] resource.
#
# Carte de reference : ab007 * Donald Pierce (pack albert), « Resource:
# Exhaust Donald Pierce -> generate a [wild] resource », soit
# `CanGenerateResources(AbilityType.Resource, Resources("G"))
# .SetCostFunc(CostFunc.Exhaust("This"))` (recette moteur §4). Comparable
# parce que c'est le meme geste exact : incliner sa propre carte pour produire
# une ressource joker.
#
# ⚠ ARBITRAGE : le texte imprime dit « **Action** », pas « Resource ». Le
# moteur ne sait pas faire autrement — `CanGenerateResources` n'accepte que
# `AbilityType.Resource | HeroResource | AlterEgoResource` (factory/
# resources.py:277) — et une ressource produite hors du paiement d'une carte
# ne servirait a rien. Codee en « Resource ». Consigne au §6 du journal de
# portage, point 8, pour l'auteur.
#
# ⚠ UNE SEULE `CanGenerateResources` par carte (assert du moteur, recette §4).
# Ce n'est pas un probleme ici : Peter Parker n'a que cette capacite.
#
# ⚠ ATQ 0 sans etoile, CTR 2 AVEC etoile : lu sur le scan, coin par coin. Un
# allie a ATQ 0 ne sert donc qu'a contrer et a produire des ressources — c'est
# voulu, il est « Lab Assistant ».

def GetAbilities() -> Sequence['Ability']:

    return [
        AbilityFactory.CanGenerateResources(
            AbilityType.Resource,
            Resources("G"),
        ).SetCostFunc(CostFunc.Exhaust("This")),
    ]
