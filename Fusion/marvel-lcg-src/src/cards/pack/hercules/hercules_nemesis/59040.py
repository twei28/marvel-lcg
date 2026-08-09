from . import *
def GetAbilities() -> Sequence['Ability']:
    def god_of_war(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Treachery)
        Unused(this)
        player = message.GetToPlayer()
        def if_no_activate():
            minion = Worlds.DiscardEncounterCardsUntil(effect, card_type=Minion)
            if minion:
                minion.Reveal(player, effect)
        Enemies.AllMinionActivateAgainstEngagedPlayer(effect, if_no_activate=if_no_activate)
    return [AbilityFactory.WhenThisRevealed(None, god_of_war)]
