from . import *

# Greater Responsibility

def GetAbilities() -> Sequence['Ability']:

    def marche(effect: 'Effect', message: 'Message.AfterCardsBeSpendAsResource') -> None:
        # « Hero Response: After you spend this card, ready your hero. Then,
        # place 2 threat on a scheme. »
        this = effect.this.CastTo(Resource)
        joueur = effect.GetInitiator()
        Faces.ReadyAll([joueur.GetIdentity()], effect)
        this.PlaceThreatOnSchemes(effect.targets, 2, effect)

    return [
        AbilityFactory.AfterYouSpendThisCard(
            AbilityType.HeroResponse,
            marche
        ).SetTarget(Scheme2),
    ]
