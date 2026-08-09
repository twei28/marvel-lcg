from . import *
from cards.pack.synthezoid import EarnLeaderBasicCards, GetSetAsideLeaderBasics
def GetAbilities() -> Sequence['Ability']:
    def now_its_personal(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Obligation)
        for player in Worlds.GetPlayers(effect):
            EarnLeaderBasicCards(effect, player, 2)
        Faces.RemoveAllFromGame([this], effect)
    def check_pool(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> bool:
        return (len(GetSetAsideLeaderBasics(effect)) > 0)
    return [AbilityFactory.WhenInYourPlayTurn(AbilityType.Action, now_its_personal, conditions=[check_pool])]
