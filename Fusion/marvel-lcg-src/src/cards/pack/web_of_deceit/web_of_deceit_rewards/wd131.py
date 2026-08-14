from . import *

# Camouflage

def GetAbilities() -> Sequence['Ability']:

    def disparaitre(effect: 'Effect', message: 'Message.AfterPlayerPlayedCard') -> None:
        # « Response: After you play a SUPERPOWER card, remove 1 energy counter
        # from Camouflage → confuse an enemy and give your identity a tough
        # status card. »
        joueur = effect.GetInitiator()
        Faces.GiveStatus(effect.targets, "Confused", effect)
        Faces.GiveStatus([joueur.GetIdentity()], "Tough", effect)

    return [
        AbilityFactory.AfterPlayerPlayedCard(
            AbilityType.Response,
            "You",
            CardFinder(trait="SUPERPOWER"),
            disparaitre
        ).SetCostFunc(CostFunc.Counter("This", 1, 'energy'))
        .SetTarget(Enemy),
    ]
