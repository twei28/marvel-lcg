from . import *

# In the Line of Fire

def GetAbilities() -> Sequence['Ability']:

    def in_the_line_of_fire(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)

        initiator = effect.GetInitiator()
        personnages = [x for x in Worlds.FindCardsOnField(effect, card_type=Unit2)
                       if not x.IsDefeated()]
        if not personnages:
            return
        avant = {f: f.CastTo(CanHealth).health for f in personnages}
        initiator.AssignDamage(personnages, this, 5, effect)

        for player in Worlds.GetPlayers(effect):
            touches = sum(1 for f in personnages
                          if f.HasTrait("AERIAL")
                          and f.GetControlByPlayer() == player
                          and f.CastTo(CanHealth).health < avant[f])
            if touches:
                player.DrawUp(touches, effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            in_the_line_of_fire
        ).SetPlay().SetLabel('attack'),
    ]
