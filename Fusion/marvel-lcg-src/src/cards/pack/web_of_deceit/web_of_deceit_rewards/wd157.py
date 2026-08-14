from . import *

# Spider-Mobile

def GetAbilities() -> Sequence['Ability']:

    def reduction(effect: 'Effect') -> int:
        # « Reduce the cost to play this card by 1 for each WEB-WARRIOR card you
        # control. »
        joueur = effect.GetInitiator()
        return len(joueur.GetControlCards(CardFinder(trait="WEB-WARRIOR")))

    def demarrer(effect: 'Effect', message: 'Message.AfterUnitDefendAgainstAttack') -> None:
        # « Hero Response: After you defend against an attack, exhaust
        # Spider-Mobile → ready your identity. »
        joueur = effect.GetInitiator()
        Faces.ReadyAll([joueur.GetIdentity()], effect)

    return [
        AbilityFactory.ReduceCostToPlayThis(
            reduction,
        ),
        AbilityFactory.AfterUnitDefendAgainstAttack(
            AbilityType.HeroResponse,
            "YourHero",
            demarrer
        ).SetCostFunc(CostFunc.Exhaust("This")),
    ]
