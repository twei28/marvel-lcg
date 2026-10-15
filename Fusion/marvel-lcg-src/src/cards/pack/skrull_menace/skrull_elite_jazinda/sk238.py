from . import *

# * Sy-Torak Gem — ATTACHEMENT (Skrull Elite - Jazinda). ARTIFACT. +1 ATQ, 3 icones de boost.
# Attach to Jazinda. If you cannot, attach to the villain.
# Attached character gets +3 hit points.
# Hero Action: Give the villain 1 facedown boost card and spend a [energy] resource → discard Sy-Torak Gem.
#
# Cartes de reference :
#  - « Attach to X. If you cannot, attach to the villain » : `AttachToFaceWhenPutIntoPlay(finder,
#    otherwise_attach_to=Villain)` (attachment.py), modele sk146.
#  - « Attached character gets +3 hit points » : **`nebu/22032`** (`GiveKeywordToAttached(..., health=3)`).
#  - « Hero Action: <cout> → discard this card » : **`sk146`** / **`sk086`** (`PlayerActionToDiscardThis`
#    + `SetCost(Cost("Y"))` + `SetCostFunc(CostFunc.Custom(None, fn))` : le cout a DEUX parties, comme
#    sk148 pour sa ressource ; la carte de boost est la seconde).
#
# ⚠ Mots-pieges : « attached CHARACTER » (sbire OU mechant) ; « +3 hit points » : PV maximum +3 (un
# mechant a PV infinis n'en profite pas : sk070-sk071) ; « AND spend » : les DEUX parties du cout (la carte
# de boost ET une ressource [energy]) sont payees ; le « → » separe COUT et EFFET (la defausse).


def GetAbilities() -> Sequence['Ability']:

    def cout_boost(cibles: Sequence['CardFace'], effect: 'Effect') -> bool:
        Unused(cibles)
        return DonnerBoostAuMechant(effect, 1) > 0

    return [
        AbilityFactory.AttachToFaceWhenPutIntoPlay(
            CardFinder(name=NOM_JAZINDA, card_type=Minion),
            otherwise_attach_to=Villain,
        ),
        *AbilityFactory.GiveKeywordToAttached(Unit2, health=3),
        AbilityFactory.PlayerActionToDiscardThis(AbilityType.HeroAction)
        .SetCost(Cost("Y"))
        .SetCostFunc(CostFunc.Custom(None, cout_boost)),
    ]
