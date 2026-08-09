from . import *
def GetAbilities() -> Sequence['Ability']:
    def starting(effect: 'Effect', message: 'Message.WhenGameBeginSetup') -> None:
        this = effect.this.CastTo(Upgrade)
        if not this.card.area.flags.is_player_deck:
            return
        player = this.GetControlByOrOwner()
        Faces.AddToHand([this], player, effect)
    return [AbilityFactory.CanPlayThisUpgradeCard(),
            *AbilityFactory.GiveKeywordToAttached(Hero, defense=1),
            AbilityFactory.WhenGameBeginSetup(starting).NoOutOfPlayLimit()]
