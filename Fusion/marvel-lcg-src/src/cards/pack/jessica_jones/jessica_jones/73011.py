from . import *

# Private Investigator — custom « ekAugust »
# Alter-Ego Action: Exhaust Private Investigator -> move 1 threat from a scheme
#   to here.
# Hero Action: Remove all threat from here -> deal 1 damage to a minion for
#   each threat removed this way.
#
# Meme montage que Beat Cop (10029) : les jetons de menace poses sur une carte
# joueur sont des tokens 'threat', pas de la menace de manigance.

def GetAbilities() -> Sequence['Ability']:

    def stake_out(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Upgrade)

        value = Faces.RemoveTokensOn(effect.targets, 1, 'threat', effect)
        if value:
            Faces.PlaceTokensOn([this], value, 'threat', effect)

    def close_the_file(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Upgrade)

        damage = this.GetTokens('threat')
        if damage:
            Faces.RemoveTokensOn([this], damage, 'threat', effect)
            this.DealDamage(effect.targets, damage, effect)

    def has_threat(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> bool:
        return effect.this.CastTo(Upgrade).GetTokens('threat') > 0

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.AlterEgoAction,
            stake_out,
        ).SetCostFunc(CostFunc.Exhaust("This"))
        .SetTarget(Scheme2),

        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            close_the_file,
            conditions=[has_threat],
        ).SetTarget(Minion),
    ]
