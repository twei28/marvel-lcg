from . import *

# * Scorpion

def GetAbilities() -> Sequence['Ability']:

    def scorpion(effect: 'Effect', message: 'Message.AfterMinionEngagePlayer') -> None:
        # « Forced Response (Hero): After Scorpion engages you, stun your hero. »
        joueur = message.GetToPlayer()
        Faces.GiveStatus([joueur.GetIdentity()], "Stunned", effect)

    return [
        AbilityFactory.AfterMinionEngagePlayer(
            AbilityType.ForcedResponse,
            "This",
            "YouHero",
            scorpion
        ),
    ]
