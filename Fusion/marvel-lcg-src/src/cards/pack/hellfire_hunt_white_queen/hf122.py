from . import *

# Psionic Fortification (x2). Traitrise SKILL. « When Revealed : If White Queen is in DIAMOND form, heal 1 damage from her and give her a tough
# status card. If she is in PSIONIC form, heal 3 damage from her and remove each stunned and confused status card from her. [star] Boost : Give
# White Queen a tough status card. » Cartes de reference : 04089 Omni-Morph Duplication (`HealthUnits` + `GiveStatus(..., "Tough")`).


def GetAbilities() -> Sequence['Ability']:
    def revelee(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this
        villain = VilainWQ(effect)
        if villain is None:
            return
        if EstDiamant(villain):
            this.HealthUnits([villain], 1, effect)
            Faces.GiveStatus([villain], "Tough", effect)
        elif EstPsionique(villain):
            this.HealthUnits([villain], 3, effect)
            villain.DiscardStunned(effect, rule="All")
            villain.DiscardConfused(effect, rule="All")

    def boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        villain = VilainWQ(effect)
        if villain is not None:
            Faces.GiveStatus([villain], "Tough", effect)

    return [
        AbilityFactory.WhenThisRevealed(None, revelee),
        AbilityFactory.WhenCardBecomeBoost("This", boost),
    ]
