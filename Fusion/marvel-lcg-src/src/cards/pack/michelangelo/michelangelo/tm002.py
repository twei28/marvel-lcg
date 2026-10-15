from . import *

# * Slash — allie signature, x1 (1/15). MUTANIMAL. TURTLE.
# Cout 3, ressource [physical]. THW 0 (1 degat consecutif), ATQ 3 (2 degats
# consecutifs), PV 2.
# Retaliate 1. Toughness.
# [star] Slash's attacks gain piercing.
#
# Cartes de reference :
#  - Retaliate et Toughness : BASES AUTOMATIQUES (desc), fiches
#    mots-cles/retaliate.md et toughness.md : RIEN a coder ;
#  - l'etoile : `aos/50098` Machete et `ho016` Bullseye —
#    `AbilityFactory.UnitAttackGainKeyword("This", piercing=True)` (fiche
#    mots-cles/piercing.md).
#
# ⚠ Mots-pieges :
#  - « Slash's attacks » : TOUTES les attaques de Slash (attaque de base ET
#    capacites), `"This"` = cette carte seulement.
#  - Les icones etoilees creuses sous THW/ATQ sont des degats CONSECUTIFS
#    (`desc.ATK = "3**"`, `THW = "0*"`), pas des etoiles de capacite ; l'etoile
#    pleine a cote du 3 est la convention d'impression du [star].

def GetAbilities() -> Sequence['Ability']:

    return [
        AbilityFactory.UnitAttackGainKeyword(
            "This",
            piercing=True,
        ),
    ]
