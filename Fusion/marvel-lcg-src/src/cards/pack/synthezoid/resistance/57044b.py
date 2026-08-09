from . import *
def GetAbilities() -> Sequence['Ability']:
    def discard_tops(effect: 'Effect', message: 'Message.AfterResolveVillainPhaseStep') -> None:
        def action(player: 'Player'):
            for _ in range(3):
                top = player.player_deck.GetTop()
                if top:
                    Faces.DiscardAll([top], effect)
        Players.ForEachPlayer(effect, action)
    def hinder_value(effect: 'Effect', ui: List['CardFace']) -> int:
        num = len(effect.world.players)
        if (num <= 1):
            return 0
        return (2 * num)
    return [AbilityFactory.ThisGainKeyword(hinder_value, hinder=1),
            AbilityFactory.AfterResolveVillainPhaseStep(AbilityType.ForcedResponse, 1, discard_tops)]
