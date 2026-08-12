from . import *

# * Doctor Strange — custom « DesignHacker » (Age of Khonshu)
# Victory 1. Villainous.  (clés desc, gérées nativement)
# Forced Response: After Doctor Strange damages your hero, discard 1 card at
#   random from your hand.
# When Defeated: The player who defeated Doctor Strange puts The Eye of
#   Agamotto into play under their control.


def GetAbilities() -> Sequence['Ability']:

    def defausse_aleatoire(effect: 'Effect', message: 'Message.AfterUnitTookDamage') -> None:
        this = effect.this.CastTo(Minion)
        Unused(this)
        victime = message.trigger
        player = victime.GetControlByPlayer()
        if player is not None:
            player.DiscardRandomHandCards(1, effect)

    return [
        AbilityFactory.AfterUnitTookDamage(
            AbilityType.ForcedResponse,
            Hero,
            defausse_aleatoire,
            who_dealt_damage="This",
        ),
        CapaciteArtefactLie("mk022"),
    ]
