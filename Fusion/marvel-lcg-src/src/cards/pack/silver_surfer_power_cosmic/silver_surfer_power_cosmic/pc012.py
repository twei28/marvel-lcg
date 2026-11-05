from . import *

# Psionic Bond — AMELIORATION. POWER COSMIC. PSIONIC. Cout 2, ressource
# [wild].
#
# Texte imprime : « Action: Exhaust this card and spend a resource of any
# type → ready Cosmic Surfboard. »
#
# CARTES DE REFERENCE
#  - `Worlds.FindCardOnField(effect, name="Cosmic Surfboard")` (modele
#    `cd006.py` pure_lightforce : `Worlds.FindCardOnField(effect2,
#    card_type=Villain)`) : pas de cible a choisir, une seule Cosmic
#    Surfboard possible (Max 1 par joueur, carte signature unique).
#  - `CostFunc.Exhaust("This")` + `Cost("1")` (ressource de n'importe quel
#    type) : deux couts cumules sur la meme Action, modele `dy003` Mystique.


def GetAbilities() -> Sequence['Ability']:

    def psionic_bond(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        Unused(message)
        surfboard = Worlds.FindCardOnField(effect, name="Cosmic Surfboard")
        if surfboard is not None:
            Faces.ReadyAll([surfboard], effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.Action,
            psionic_bond,
        ).SetCostFunc(CostFunc.Exhaust("This"))
        .SetCost(Cost("1")),
    ]
