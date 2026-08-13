from . import *

# Incentivized

def GetAbilities() -> Sequence['Ability']:

    def incentivized(effect: 'Effect', message: 'Message.WhenUnitWouldAttackUnit') -> None:
        this = effect.this.CastTo(Upgrade)

        allie = this.GetBindFace()
        if allie is None:
            return
        # X = le nombre de cartes attachees a l'ennemi attaque. L'inventaire
        # d'une face porte ses ameliorations ET ses attachements (note de
        # methode du 28/07).
        valeur = len(message.target.GetInventoryDeck().GetAll())
        if valeur > 0:
            allie.CastTo(Unit2).GainForThisActive(effect, message, attack=valeur)

    return [
        AbilityFactory.CanPlayThisUpgradeCard(
            CardFinder(card_type=Ally)
        ),
        AbilityFactory.WhenUnitWouldAttackUnit(
            AbilityType.Interrupt,
            "AttachedAlly",
            Enemy,
            incentivized,
        ),
    ]
