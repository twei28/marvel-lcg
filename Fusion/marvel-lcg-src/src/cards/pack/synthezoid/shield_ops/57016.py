from . import *
def GetAbilities() -> Sequence['Ability']:
    def first_minion_surge(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        minion = message.trigger
        minion.CastTo(CanSurge).GainSurge(1, effect)
    return [AbilityFactory.WhenPlayerRevealCard(AbilityType.NonKeyword, 'AnyPlayer', Minion, None, first_minion_surge, from_encounter=True).LimitOncePerRound()]
