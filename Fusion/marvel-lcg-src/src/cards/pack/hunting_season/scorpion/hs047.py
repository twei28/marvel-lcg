from . import *

# hs047 A Mess of Things

def GetAbilities() -> Sequence['Ability']:
    def revelee(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this
        etourdis = [f for f in Worlds.GetOnFieldFriendlyCharacters(effect) if f.IsStunned()]
        if etourdis:
            Faces.PlaceTokensOn([this], 2 * len(etourdis), 'threat', effect)
    return [AbilityFactory.WhenThisRevealed(None, revelee)]
