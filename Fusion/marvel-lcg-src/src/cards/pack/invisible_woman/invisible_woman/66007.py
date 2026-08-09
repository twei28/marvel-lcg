from . import *


def GetAbilities() -> Sequence['Ability']:

    def force_shields(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        Faces.GiveStatus(effect.targets, "Tough", effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            force_shields,
        )# CORRECTIF (4/8/2026) : `SetPlay` marquait cette action comme LA
        # capacite qui joue la carte depuis la main. Une fois l'amelioration
        # posee, elle devenait donc inerte : plus aucune action en jeu.
        # `SetCondition` porte la meme condition de forme sans revendiquer
        # le role de capacite de jeu.
        .SetCondition(only_if_your_identity_has_trait="PSIONIC")
        .SetCostFunc(CostFunc.Exhaust("This"))
        .SetTarget(Friend, range=(1, "All"), canbe_status="Tough")
        .SetName("Force Shields"),
    ]
