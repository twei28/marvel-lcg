from . import *

# * Reaper

def GetAbilities() -> Sequence['Ability']:

    def reaper(effect: 'Effect', message: 'Message.WhenUnitWouldAttack') -> None:
        this = effect.this.CastTo(Minion)
        Unused(this)

        player = message.property.against_player
        if player:
            identity = player.GetIdentity()
            b = FacesCounter.GetPrintedResourcesCount(player.hand_cards.Get(), "B")
            if b >= 2:
                Faces.GiveStatus([identity], "Stunned", effect)
            if b >= 4:
                Faces.ExhaustAll([identity], effect)


    return [
        # CORRECTIF : le texte est un « Forced Interrupt: WHEN Reaper attacks
        # you ». C'etait accroche a AfterUnitAttackEnd en ForcedResponse, donc
        # le comptage des ressources mentales et le Sonne/inclinaison arrivaient
        # APRES l'attaque : la main avait pu changer entre-temps, et incliner
        # l'identite trop tard la laissait defendre alors qu'elle ne devrait
        # plus pouvoir.
        AbilityFactory.WhenUnitWouldAttack(
            AbilityType.ForcedInterrupt,
            "This",
            reaper,
            against_player="You",
        ),
    ]

