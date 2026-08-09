from . import *
def GetAbilities() -> Sequence['Ability']:
    def no_allies(effect: 'Effect', attach: 'CardFace', ui: List['CardFace']) -> int:
        player = attach.GetControlByPlayer()
        return (player.allies.FindCard(card_type=Ally) == None)
    return [AbilityFactory.CanPlayThisUpgradeCard(),
            *AbilityFactory.GiveKeywordToAttached(Hero, get_new_value=no_allies, defense=1, retaliate=1, ex_change_on_event=OnEvent.CardInPlay(Ally))]
