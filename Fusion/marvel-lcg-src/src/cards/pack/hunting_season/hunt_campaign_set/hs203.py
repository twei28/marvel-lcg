from . import *

# hs203 * Vulture (allie, recompense du scenario 4)
# Action : incline Vulture et inflige-lui 1 degat -> redresse un personnage ami,
# qui gagne AERIAL jusqu'a la fin de la phase.

def GetAbilities() -> Sequence['Ability']:

    def envoler(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        Faces.ReadyAll(effect.targets, effect)
        for perso in effect.targets:
            perso.GainUntilPhaseEnd(effect, trait=["AERIAL"])

    return [
        AbilityFactory.WhenInYourPlayTurn(AbilityType.Action, envoler)
        .SetCostFunc(CostFunc.Exhaust("This")).SetCostFunc(CostFunc.TakeDamage(1, "This"))
        .SetTarget(Friend),
    ]
