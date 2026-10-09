from . import *

# hs184 * Savage Land (Experience Cost 4)
# Hero Action : incline Savage Land et inflige 1 degat a un heros ou un allie
# -> ce personnage gagne +1 THW et +1 ATK jusqu'a la fin du round.

def GetAbilities() -> Sequence['Ability']:

    def endurcir(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this
        for perso in effect.targets:
            this.DealDamage([perso], 1, effect)
            perso.GainUntilRoundEnd(effect, thwart=1, attack=1)

    return [
        AbilityFactory.WhenInYourPlayTurn(AbilityType.HeroAction, endurcir)
        .SetCostFunc(CostFunc.Exhaust("This")).SetTarget(Hero | Ally),
    ]
