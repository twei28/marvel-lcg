from . import *

# False Reality (ATTACHEMENT ILLUSION PSIONIC). Boost 1. « Attach to the main scheme. Forced Interrupt : When a player would remove threat from the
# main scheme, prevent 2 of that threat from being removed. Then, confuse that player. (Limit once per phase.) Hero Action : Spend [mental][mental]
# resource -> discard this card. »
# Cartes de reference : `WhenSchemeWouldRemoveThreat` (scheme.py ; modele sk194), sk147 (Hero Action `PlayerActionToDiscardThis` a cout BB),
# ar007 (`LimitOncePerPhase` + temoin d'epuisement), `AttachToFaceWhenPutIntoPlay(MainScheme)`.
# ⚠ ENGINE (additif) : `WhenSchemeWouldRemoveThreat.PreventRemoval(n)` (sender_scheme.py) ; « that player » : celui qui retire (le joueur qui
# controle le thwart, sinon l'initiateur) ; « Then » : la desorientation APRES la prevention ; la prevention ne s'applique que si de la menace
# est retiree (value > 0).


def GetAbilities() -> Sequence['Ability']:
    def retrait(effect: 'Effect', message: 'Message.WhenSchemeWouldRemoveThreat') -> None:
        message.PreventRemoval(2, effect)
        joueur = JoueurQuiRetire(message)
        if joueur is not None:
            Faces.GiveStatus([joueur.GetIdentity()], "Confused", effect)

    return [
        AbilityFactory.AttachToFaceWhenPutIntoPlay(MainScheme),
        AbilityFactory.WhenSchemeWouldRemoveThreat(AbilityType.ForcedInterrupt, "AttachedScheme", retrait).LimitOncePerPhase(),
        AbilityFactory.PlayerActionToDiscardThis(AbilityType.HeroAction).SetCost(Cost("BB")),
    ]
