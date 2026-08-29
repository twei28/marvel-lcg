from . import *
def GetAbilities() -> Sequence['Ability']:
    def check_fn(effect: 'Effect', last_value: int):
        return 2 if effect.this.tough > 0 else 0
    def process_atk(effect: 'Effect', diff: int, curr: int) -> None:
        effect.this.CastTo(Ally).GainAttack(diff, effect)
    def process_thw(effect: 'Effect', diff: int, curr: int) -> None:
        effect.this.CastTo(Ally).GainThwart(diff, effect)
    return [
        AbilityFactory.WhileValid(OnEvent.CardInPlay(Ally), lambda e, m: True, check_fn, process_atk),
        AbilityFactory.WhileValid(OnEvent.CardInPlay(Ally), lambda e, m: True, check_fn, process_thw),
    ]
