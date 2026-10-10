from . import *
def GetAbilities() -> Sequence['Ability']:
    def check_fn(effect: 'Effect', last_value: int):
        return 2 if effect.this.tough > 0 else 0
    def process_atk(effect: 'Effect', diff: int, curr: int) -> None:
        effect.this.CastTo(Ally).GainAttack(diff, effect)
    def process_thw(effect: 'Effect', diff: int, curr: int) -> None:
        effect.this.CastTo(Ally).GainThwart(diff, effect)
    return [
        # CORRECTIF (10/10/2026) : « while SHE has a tough status card ». Sur
        # `CardInPlay` seul, le bonus pose a l'entree (Toughness) n'etait jamais
        # retire quand son Tenace tombait. Meme defaut que 62002 (rapport n75).
        AbilityFactory.WhileValid([OnEvent.CardInPlay(Ally), OnEvent.Status("This", 'Tough')], lambda e, m: True, check_fn, process_atk),
        AbilityFactory.WhileValid([OnEvent.CardInPlay(Ally), OnEvent.Status("This", 'Tough')], lambda e, m: True, check_fn, process_thw),
    ]
