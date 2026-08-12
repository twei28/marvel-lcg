from . import *


def GetAbilities() -> Sequence['Ability']:

    def vanishing_act(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        Faces.GiveStatus(effect.targets, "Confused", effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            vanishing_act,
        )# CORRECTIF (4/8/2026) : `SetPlay` marquait cette action comme LA
        # capacite qui joue la carte depuis la main. Une fois l'amelioration
        # posee, elle devenait donc inerte : plus aucune action en jeu.
        # `SetCondition` porte la meme condition de forme sans revendiquer
        # le role de capacite de jeu.
        .SetCondition(only_if_your_identity_has_trait="INVISIBLE")
        .SetLabel()
        .SetCost(Cost("BY"))
        .SetCostFunc(CostFunc.Exhaust("This"))
        .SetTarget(Enemy, canbe_confused=True)
        .SetName("Vanishing Act"),
    ]
