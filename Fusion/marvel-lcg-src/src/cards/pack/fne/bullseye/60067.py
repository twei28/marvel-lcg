from . import *

# * Bullseye (III) — SCH 1 / ATK 3 / 18[per_hero]
# When Revealed: Find Deranged Bloodlust and reveal it.

def GetAbilities() -> Sequence['Ability']:

    def revele(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        Find.FindAndReveal(effect, message.GetToPlayer(), name="Deranged Bloodlust", card_type=SchemeSide2)

    return [
        AbilityFactory.WhenThisRevealed(None, revele),
        *CapacitesDeBullseye(),
    ]
