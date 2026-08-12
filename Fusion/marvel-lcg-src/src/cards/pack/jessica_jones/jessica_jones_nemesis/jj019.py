from . import *

# * Purple Man — custom « ekAugust » (sbire nemesis de Jessica Jones)
# Forced Interrupt: When Purple Man would attack, place 2 threat on each side
#   scheme instead. If there are no side schemes in play, reveal the top card
#   of the encounter deck.
# Boost: You are confused.

def GetAbilities() -> Sequence['Ability']:

    def purple_man(effect: 'Effect', message: 'Message.WhenUnitWouldAttack') -> None:
        this = effect.this.CastTo(Minion)

        message.SetBeInstead(effect)

        manigances = Worlds.GetSideSchemes(effect)
        if manigances:
            for manigance in manigances:
                this.PlaceThreatOnSchemes([manigance], 2, effect)
        else:
            player = this.GetEngagedPlayer() or Worlds.GetFirstPlayer(effect)
            # `RevealEncounterDeckTopCard`, comme Under Fire 01193 : il n'existe
            # pas de `Worlds.RevealEncounterCard` (erreur trouvee le 4/8/2026
            # par introspection, la carte n'est pas atteignable par le harnais).
            Worlds.RevealEncounterDeckTopCard(player, effect)

    def you_are_confused(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        this = effect.this.CastTo(Minion)
        Unused(this)

        identity = message.GetToPlayer().GetIdentity()
        Faces.GiveStatus([identity], "Confused", effect)

    return [
        AbilityFactory.WhenUnitWouldAttack(
            AbilityType.ForcedInterrupt,
            "This",
            purple_man,
        ),

        AbilityFactory.WhenCardBecomeBoost(
            "This",
            you_are_confused,
        ),
    ]
