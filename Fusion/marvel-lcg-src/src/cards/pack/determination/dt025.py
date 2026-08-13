from . import *

# * Shang-Chi

def GetAbilities() -> Sequence['Ability']:

    def ready_shang_chi(effect: 'Effect', message: 'Message2') -> None:
        this = effect.this.CastTo(Ally)
        Faces.ReadyAll([this], effect)

    return [
        Fragile(),
        # Deux fenetres pour un seul texte : le moteur separe « retirer la
        # derniere menace » de « vaincre un sbire ».
        AbilityFactory.AfterUnitThwartAndRemoveLastThreat(
            AbilityType.Response,
            "This",
            ready_shang_chi
        ),
        AbilityFactory.AfterUnitDefeatedUnit(
            AbilityType.Response,
            "This",
            Minion,
            ready_shang_chi,
        ),
    ]
