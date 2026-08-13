from . import *

# * Captain Universe

def GetAbilities() -> Sequence['Ability']:

    def captain_universe(effect: 'Effect', message: 'Message.WhenAllyWouldTakeConsequentialDamage') -> None:
        this = effect.this.CastTo(Ally)

        player = this.GetControlByPlayer()
        if player is None:
            return
        valeur = len(player.dealt_encounter_cards.Get())
        if valeur > 0:
            message.PreventDamage(valeur, effect)

    def check_this(effect: 'Effect', message: 'Message.WhenAllyWouldTakeConsequentialDamage') -> bool:
        return effect.this == message.trigger

    return [
        *Alias(),
        Ability(
            AbilityType.Interrupt,
            Message.WhenAllyWouldTakeConsequentialDamage,
            [check_this],
            captain_universe,
            is_local=True
        ),
    ]
