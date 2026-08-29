from . import *
def GetAbilities() -> Sequence['Ability']:
    def check_fn(effect: 'Effect', last_value: int):
        return effect.this.GetCounters('rage')
    def process_fn(effect: 'Effect', diff: int, curr: int) -> None:
        effect.this.CastTo(Ally).GainAttack(diff, effect)
    def villain_attacks(effect: 'Effect', message: 'Message.AfterUnitAttackUnit') -> None:
        this = effect.this.CastTo(Ally)
        this.PlaceCountersInternal(1, 'rage', effect)
    def check_villain(effect: 'Effect', message: 'Message.AfterUnitAttackUnit') -> bool:
        return Villain.IsType(message.attacker)
    return [
        AbilityFactory.WhileValid(OnEvent.CardInPlay(Ally), lambda e, m: True, check_fn, process_fn),
        AbilityFactory.AfterUnitAttackUnit(AbilityType.Response, None, "You", villain_attacks, conditions=[check_villain]),
    ]
