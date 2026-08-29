from . import *
def GetAbilities() -> Sequence['Ability']:
    def check_fn(effect: 'Effect', last_value: int):
        identity = effect.GetInitiator().GetIdentity()
        n = identity.tough if identity else 0
        return min(n, 4)
    def process_fn(effect: 'Effect', diff: int, curr: int) -> None:
        effect.this.CastTo(Ally).GainThwart(diff, effect)
    return [
        AbilityFactory.WhileValid(
            OnEvent.CardInPlay(Ally),
            lambda effect, message: True,
            check_fn,
            process_fn,
        ),
    ]
