from . import *
def GetAbilities() -> Sequence['Ability']:
    def reactive_defense(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Obligation)
        enemies = Worlds.FindCardsOnField(effect, card_type=Enemy)
        if enemies:
            this.DealDamage(enemies, 5, effect)
        Faces.RemoveAllFromGame([this], effect)
    return [AbilityFactory.WhenInYourPlayTurn(AbilityType.AlterEgoAction, reactive_defense).SetCost(Cost('YBR'))]
