from . import *

# Runic Magician — amelioration signature. SKILL. Cout 3. x1
# Resource: Exhaust Runic Magician -> generate a [wild] resource for a SPELL
#   or MYSTIC card.
# Hero Interrupt: When you resolve Agatha Harkness's "Power Absorption"
#   ability, ignore the SPELL trait requirement.
#
# Cartes de reference (RECETTES §4) :
#  - la ressource ciblee : 54002 * Cybernetic Arm (`CanGenerateResources(
#    Resource, Resources("G"), for_card=...)` + `CostFunc.Exhaust("This")`) ;
#    le « SPELL ou MYSTIC » passe par un CardFinder a deux traits en OU ;
#  - l'interrupt : implemente DANS aa001a (helper `RunicMagicianEnJeu` du
#    __init__ du pack) — quand Runic Magician est en jeu, Power Absorption
#    propose TOUTES les cartes defaussees, pas seulement les SPELL. Meme
#    montage que ho006/aa001a : la capacite vit ou elle agit, le commentaire
#    des DEUX fichiers pointe l'autre.

def GetAbilities() -> Sequence['Ability']:

    def spell_ou_mystic(effect: 'Effect', face: 'CardFace') -> bool:
        Unused(effect)
        return face is not None and (face.HasTrait("SPELL")
                                     or face.HasTrait("MYSTIC"))

    return [
        AbilityFactory.CanPlayThisUpgradeCard(),
        AbilityFactory.CanGenerateResources(
            AbilityType.Resource,
            Resources("G"),
            # `check_effect_fn` : le seul crochet OU du CardFinder (finder.py:217)
            for_card=CardFinder(check_effect_fn=spell_ou_mystic),
        ).SetCostFunc(CostFunc.Exhaust("This")),
    ]
