from . import *

# Greater Power
#
# Le marche du symbiote : ce qu'il rend au heros, il le prend sur la table.

def GetAbilities() -> Sequence['Ability']:

    def marche(effect: 'Effect', message: 'Message.AfterCardsBeSpendAsResource') -> None:
        # « Hero Response: After you spend this card, heal 2 damage from your
        # hero. Then, place 2 threat on a scheme. »
        this = effect.this.CastTo(Resource)
        joueur = effect.GetInitiator()
        this.HealthUnits([joueur.GetIdentity()], 2, effect)
        this.PlaceThreatOnSchemes(effect.targets, 2, effect)

    return [
        AbilityFactory.AfterYouSpendThisCard(
            AbilityType.HeroResponse,
            marche
        ).SetTarget(Scheme2),
    ]
