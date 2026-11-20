from . import *

# Hand Katana — ATTACHEMENT, WEAPON, +2 ATQ (`desc["ATK+"]`), 2 icones de boost. Nemesis 3/5.
# S'attache au sbire HAND aux PV de base les plus eleves, sinon au mechant. Hero Action : depenser 2 ressources -> defausser.
#
# CARTES DE REFERENCE
#  - attache « highest base hit points, otherwise the villain » : `01163`, `62031` (`otherwise_attach_to=Villain`, jamais "EnemyLeader").
#  - « Spend 2 resources of any type -> discard this card » : `31037` Surge in Crime (`PlayerActionToDiscardThis(...).SetCost(Cost("2"))`).


def GetAbilities() -> Sequence['Ability']:

    return [
        AbilityFactory.AttachToFaceWhenPutIntoPlay(
            CardFinder2(TRAIT_MAIN, Minion),
            highest_printed_hp=True,
            otherwise_attach_to=Villain,
        ),
        AbilityFactory.PlayerActionToDiscardThis(AbilityType.HeroAction).SetCost(Cost("2")),
    ]
