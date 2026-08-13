from . import *

# Bounty

def GetAbilities() -> Sequence['Ability']:

    def bounty(effect: 'Effect', message: 'Message.AfterUnitBeDefeated') -> None:
        this = effect.this.CastTo(Upgrade)

        joueur = this.GetOwnerPlayer()
        if joueur is None:
            return
        joueur.DrawUp(2, effect)

        attaquant = message.killer
        if attaquant is not None and attaquant.HasTrait("HERO FOR HIRE"):
            this.HealthUnits([attaquant], 1, effect)

    return [
        AbilityFactory.CanPlayThisUpgradeCard(
            CardFinder(card_type=Enemy)
        ),
        AbilityFactory.AfterUnitBeDefeated(
            AbilityType.Response,
            "AttachedEnemy",
            bounty,
            by_attack=True,
        ),
    ]
