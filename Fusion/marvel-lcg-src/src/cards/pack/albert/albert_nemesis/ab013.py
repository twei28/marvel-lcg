from . import *

# Crack in the Multiverse — custom « Kajislav » (side scheme némésis d'Albert)
# Hinder 2 (par joueur — géré par desc.Hinder "2*").
# Forced Response: After the player phase ends, the first player finds a
# WOLVERINE minion and reveals it.

def GetAbilities() -> Sequence['Ability']:

    def crack_in_the_multiverse(effect: 'Effect', message: 'Message.WhenPhaseEnd') -> None:
        this = effect.this.CastTo(EncounterSideScheme)
        Unused(this)

        player = Worlds.GetFirstPlayer(effect)

        Find.FindAndReveal(
            effect,
            player,
            trait="WOLVERINE",
            card_type=Minion,
        )

    return [
        AbilityFactory.WhenPlayerPhaseEnd(
            AbilityType.ForcedResponse,
            crack_in_the_multiverse,
        ),
    ]
