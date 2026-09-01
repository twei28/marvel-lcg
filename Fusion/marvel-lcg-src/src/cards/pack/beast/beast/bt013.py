from . import *

# Hunter Gear — amelioration signature. ITEM. ARMOR. Cout 2. RES [physical]
# Beast gets +1 DEF.
# Action: Exhaust Hunter Gear -> generate a [physical] resource if you have no
#   cards marked with a [physical] resource in your hand.
#
# Cartes de reference :
#  - le +1 DEF continu : an008 / ho011 / bt018, meme
#    `GiveKeywordToAttached("You", defense=1)` (recette moteur §3). Le bonus
#    n'a ni declencheur ni duree, il vit avec la carte.
#  - la generation de ressource : ab007 * Donald Pierce, via bt014 du meme
#    pack, `CanGenerateResources(AbilityType.Resource, Resources("R"))
#    .SetCostFunc(CostFunc.Exhaust("This"))` (recette moteur §4).
#  - la condition « si tu n'as aucune carte X en main » : mf009 Stretched Thin
#    / mf012 Mental Gymnastics (pack mister_fantastic), « if you have no cards
#    remaining in your hand ». Comparable par la forme, mais Beast compte les
#    cartes portant une ICONE precise, pas la main entiere : le comptage passe
#    par `FacesCounter.GetPrintedResources`, comme ho009 (recette §4).
#
# ⚠ ARBITRAGE : « **Action** » qui genere une ressource, meme cas que bt014 —
# le moteur n'accepte que Resource / Hero Resource / Alter-Ego Resource.
# Consigne au §6 du journal de portage, point 8, pour l'auteur.
#
# ⚠ « cards MARKED WITH a [physical] resource » : on regarde l'icone IMPRIMEE
# au coin des cartes en main, pas ce qu'elles pourraient generer par capacite.
# Alien Materials (bt009), qui porte [energy][mental], ne bloque donc PAS
# Hunter Gear ; un exemplaire de Primal Rage (bt008), qui porte [physical],
# le bloque.
#
# ⚠ `HasColorPrinted`, PAS `HasColor` : `HasColor` convertit le [wild] en la
# couleur demandee (resources.py:139), donc une main ne contenant qu'une carte
# [wild] serait vue comme « marquee physique » et bloquerait Hunter Gear a
# tort. « MARKED WITH » designe l'icone reellement imprimee.
#
# ⚠ La condition est evaluee AU PAIEMENT, pas a l'annonce : d'ou
# `resources_fn` plutot qu'une `Resources` figee. Une main qui se vide au
# cours du paiement d'une carte peut donc debloquer Hunter Gear — c'est le
# comportement attendu, et c'est le meme piege que ho009 (le `res` fige avant
# `PayCost`), contourne ici parce qu'on relit la main a chaque appel.

def GetAbilities() -> Sequence['Ability']:

    def ressource_si_main_sans_physique(effect: 'Effect',
                                        message: 'Message.CheckPlayerCanPayCost') -> 'Resources|None':
        Unused(message)
        initiator = effect.GetInitiator()
        if initiator is None:
            return None

        res = FacesCounter.GetPrintedResources(initiator.hand_cards.Get())
        if res.HasColorPrinted("R"):
            return None

        return Resources("R")

    return [
        AbilityFactory.CanPlayThisUpgradeCard(),
        *AbilityFactory.GiveKeywordToAttached(
            "You",
            defense=1,
        ),
        AbilityFactory.CanGenerateResources(
            AbilityType.Resource,
            resources_fn=ressource_si_main_sans_physique,
        ).SetCostFunc(CostFunc.Exhaust("This")),
    ]
