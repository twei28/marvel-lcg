from . import *

# * Conan — allie signature, x1 (1/15). ADVENTURER. Cout 3, ressource [R].
# THW 1 / ATK 1, 3 PV.
# Interrupt: When you use one of Conan's basic powers, exhaust a WEAPON
# upgrade you control -> Conan gets +X to that power for this use, where X
# is equal to that card's printed cost.
#
# CARTES DE REFERENCE
#  - `AbilityFactory.WhenUnitUseBasicPower` (friend.py:339) : declencheur
#    generique, `which_unit="This"` cible Conan lui-meme.
#  - `sender_unit.py:21`, `Message.WhenUnitUseBasicPower.GainValue(value,
#    effect)` : ajoute `value` AU POUVOIR EN COURS (attaque/menee), quel que
#    soit lequel des deux Conan emploie -- exactement « that power ».
#  - `an003` Heven's Fury : `CostFunc.Exhaust(trait="WEAPON")`.
#  - `cap/03017.py`, `effect.cost_func.Get(CostFunc.Exhaust)
#    .return_exhausted_cards` : relit la carte REELLEMENT inclinee pour en
#    lire le cout, pas une valeur fixe.
#
# TEXTE CONTRE CODE
#  ⚠ « Interrupt », sans « Hero » : Conan est un allie, toujours actif quelle
#    que soit la forme du joueur -> `AbilityType.Interrupt`.
#  ⚠ « one of Conan's basic powers » : pas de filtre `powers=`, Conan n'a de
#    toute facon que THW/ATK (un allie n'a jamais DEF ni REC).
#  ⚠ « X is equal to that card's printed cost » : `printed_cost.val` (élément
#    `Cost`, pas un entier brut), lu sur la carte REELLEMENT depensee en
#    cout, jamais une valeur devinee.

def GetAbilities() -> Sequence['Ability']:

    def conan_basic_power(effect: 'Effect', message: 'Message.WhenUnitUseBasicPower') -> None:
        this = effect.this.CastTo(Ally)
        Unused(this)

        exhaustee = effect.cost_func.Get(CostFunc.Exhaust)
        if not exhaustee.return_exhausted_cards:
            return
        arme = exhaustee.return_exhausted_cards[0]
        message.GainValue(arme.printed_cost.val, effect)

    return [
        AbilityFactory.WhenUnitUseBasicPower(
            AbilityType.Interrupt,
            "This",
            conan_basic_power,
        ).SetCostFunc(CostFunc.Exhaust(trait="WEAPON")),
    ]
