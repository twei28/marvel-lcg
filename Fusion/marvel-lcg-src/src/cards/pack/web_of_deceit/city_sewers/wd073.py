from . import *

# We're Totally Lost

def GetAbilities() -> Sequence['Ability']:

    def revelation(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        # « When Revealed: You are confused. If you are already confused, choose
        # and discard 1 card you control. »
        joueur = message.GetToPlayer()
        identite = joueur.GetIdentity()
        if Faces.HasStatus([identite], "Confused"):
            joueur.AskDiscardFaces(joueur.GetControlCards(), (1, 1), effect)
        else:
            Faces.GiveStatus([identite], "Confused", effect)

    return [
        Negate(1),
        AbilityFactory.WhenThisRevealed(
            None,
            revelation
        ),
    ]
