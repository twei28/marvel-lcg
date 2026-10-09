from . import *

# hs222 Rabid Rodents (environnement du mode Hunter, scenario 1)
# Vermin et Vermin Clone gagnent +1 ATK.
# Forced Response : apres l'entree en jeu d'un sbire RAT, place 1 menace sur ce sbire.

def GetAbilities() -> Sequence['Ability']:

    def menace(effect: 'Effect', message: 'Message.AfterCardEnterPlay') -> None:
        Faces.PlaceTokensOn([message.trigger], 1, 'threat', effect)

    return [
        *AbilityFactory.GiveKeywordToInPlayWhenApplyThis(CardFinder(name="Vermin", card_type=Villain), attack=1),
        *AbilityFactory.GiveKeywordToInPlayWhenApplyThis(CardFinder(name="Vermin Clone", card_type=Minion), attack=1),
        AbilityFactory.AfterCardEnterPlay(AbilityType.ForcedResponse, CardFinder(trait="RAT", card_type=Minion), menace),
    ]
