from . import *

# Jagerbombs

def GetAbilities() -> Sequence['Ability']:

    def revelee(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        joueur = message.GetToPlayer()
        identite = joueur.GetIdentity()
        joueur.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility("Stun your identity",
                lambda targets: Faces.GiveStatus([identite], "Stunned", effect)),
            AbilityFactory.ForChoiceAbility("Confuse your identity",
                lambda targets: Faces.GiveStatus([identite], "Confused", effect)),
        )

    return [
        AbilityFactory.WhenThisRevealed(None, revelee),
    ]
