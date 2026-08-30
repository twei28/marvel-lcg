from . import *

# Bulletproof Chica (2/2) - exemplaire physique 2/2, contenu identique a
# ma011 (voir ce fichier pour le detail des modeles, notamment l'absence
# volontaire de `is_from_attack` : « any amount of damage »).


def GetAbilities() -> Sequence['Ability']:

    def bulletproof_chica(effect: 'Effect',
                          message: 'Message.WhenUnitWouldTakeDamage') -> None:
        this = effect.this.CastTo(Event)
        Unused(this)

        message.PreventDamage("All", effect)

        player = effect.GetInitiator()
        if player is None:
            return
        identite = player.GetIdentity()
        if identite is not None:
            Faces.GiveStatus([identite], "Tough", effect)

    return [
        AbilityFactory.WhenUnitWouldTakeDamage(
            AbilityType.HeroInterrupt,
            "You",
            bulletproof_chica,
        ).SetPlay().SetLabel('defense'),
    ]
