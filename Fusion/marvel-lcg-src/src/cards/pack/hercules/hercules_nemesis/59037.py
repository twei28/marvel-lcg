from . import *
def GetAbilities() -> Sequence['Ability']:
    def hydra_response(effect: 'Effect', message: 'Message2') -> None:
        this = effect.this.CastTo(Minion)
        attacker = message.attacker
        player = attacker.GetControlByPlayer()
        def heal(targets: Sequence['CardFace']):
            this.HealthUnits([this], 2, effect)
        player.ChooseAbilities(effect,
                               AbilityFactory.ForChoiceAbilityWithCost(Cost('R')),
                               AbilityFactory.ForChoiceAbility('Lernean Hydra heals 2 damage', heal))
    return [AbilityFactory.AfterUnitAttackAndDamageUnit(AbilityType.ForcedResponse, (CardFinder(card_type=Hero) | CardFinder(card_type=Ally)), 'This', hydra_response)]
