from cards.pack import *

LEADER_BASIC_IDS = ('57032', '57033', '57034', '57035', '57074', '57075', '57076', '57077')
def GetSetAsideLeaderBasics(effect: 'Effect') -> List['CardFace']:
    return [x for x in Worlds.GetSetAsideAreaCards(effect) if (x.paper.card_id in LEADER_BASIC_IDS)]
def EarnLeaderBasicCards(effect: 'Effect', player: 'Player', num: int) -> None:
    pool = GetSetAsideLeaderBasics(effect)
    if not pool:
        return
    num = min(num, len(pool))
    def action(chosen: Sequence['CardFace']):
        for face in chosen:
            face.card.SetOwner(player)
        Faces.AddToHand(list(chosen), player, effect)
    player.ChooseAbilities(effect, AbilityFactory.ForChoiceAbility(f"Add {num} of your leader's basic player cards to your hand", action).SetTarget(pool, range=(num, num), not_move=True))
