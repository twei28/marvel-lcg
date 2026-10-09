from . import *

# Rats, Rats and More Rats 2A
# When Revealed: Search the encounter deck and discard pile for Bringer of
# Plague and reveal it. Advance to stage 2B (retournement automatique du moteur).

def GetAbilities() -> Sequence['Ability']:

    def bringer(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        Find.FindAndReveal(effect, Worlds.GetFirstPlayer(effect), name="Bringer of Plague", card_type=EncounterSideScheme)

    return [
        AbilityFactory.WhenThisRevealed(None, bringer),
    ]
