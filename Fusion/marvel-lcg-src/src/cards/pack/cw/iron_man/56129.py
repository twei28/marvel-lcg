from . import *
def GetAbilities() -> Sequence['Ability']:
    def the_futurist(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(this)
        initiator = effect.GetInitiator()
        leader = Worlds.FindCardOnField(effect, name='Iron Man', card_type=Leader)
        if leader:
            leader.DoSchemes(initiator, effect, property=SchemeProperty(do_not_give_boost=True))
    return [AbilityFactory.WhenInYourPlayTurn(AbilityType.Action, the_futurist).SetPlay().SetLabel()]
