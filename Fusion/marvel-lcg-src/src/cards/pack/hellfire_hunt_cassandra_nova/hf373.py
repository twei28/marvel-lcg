from . import *

# Mind Maze (ATTACHEMENT ILLUSION PSIONIC). Boost 1. « Attach to your identity. Forced Interrupt : When you would thwart, discard this card instead.
# Then, you are confused. Action : Spend [mental][mental] resources -> discard this card. »
# Cartes de reference : sk147 Distracted (`WhenUnitWouldThwart(ForcedInterrupt, "AttachedIdentity")`, Cost("BB")), `message.SetBeInstead`
# (hf324 / 90129), `AttachToFaceWhenPutIntoPlay("YourIdentity")`.
# ⚠ « instead » : la poursuite est REMPLACEE (le thwart n'a pas lieu) ; « When YOU thwart » : l'identite attachee ; la desorientation vient APRES la
# defausse.


def GetAbilities() -> Sequence['Ability']:
    def au_thwart(effect: 'Effect', message: 'Message.WhenUnitWouldThwart') -> None:
        this = effect.this
        joueur = this.GetBindFace().GetControlByOrOwner()
        message.SetBeInstead(effect)
        Faces.DiscardAll([this], effect)
        if Player.IsType(joueur):
            Faces.GiveStatus([joueur.GetIdentity()], "Confused", effect)

    return [
        AbilityFactory.AttachToFaceWhenPutIntoPlay("YourIdentity"),
        AbilityFactory.WhenUnitWouldThwart(AbilityType.ForcedInterrupt, "AttachedIdentity", au_thwart),
        AbilityFactory.PlayerActionToDiscardThis(AbilityType.Action).SetCost(Cost("BB")),
    ]
