from . import *

# * Thor — custom « DesignHacker » (Age of Khonshu)
# Victory 1. Villainous.
# Forced Response: After Thor damages a character you control, deal yourself
#   1 encounter card.
# When Defeated: The player who defeated Thor puts Mjolnir into play under
#   their control.


def GetAbilities() -> Sequence['Ability']:

    def carte_rencontre(effect: 'Effect', message: 'Message.AfterUnitTookDamage') -> None:
        this = effect.this.CastTo(Minion)
        Unused(this)
        victime = message.trigger
        player = victime.GetControlByPlayer()
        if player is not None:
            player.DealEncounterCards(1, effect)

    return [
        AbilityFactory.AfterUnitTookDamage(
            AbilityType.ForcedResponse,
            Friend,
            carte_rencontre,
            who_dealt_damage="This",
        ),
        CapaciteArtefactLie("mk021"),
    ]
