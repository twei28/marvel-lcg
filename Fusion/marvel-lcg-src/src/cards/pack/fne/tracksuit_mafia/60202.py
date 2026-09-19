from . import *

# * Tracksuit Mafioso (CRIMINAL, TRACKSUIT) — Retaliate 2, Teamwork (TRACKSUIT),
#   Vulnerable : bases desc.
# When Defeated: Tuck this card under the Tracksuit Mafia side scheme.
#   Otherwise, stun and confuse the character that defeated Tracksuit Mafioso.
# « the character that defeated » = message.killer.

def GetAbilities() -> Sequence['Ability']:

    def vaincu(effect: 'Effect', message: 'Message.WhenUnitBeDefeated') -> None:
        this = effect.this.CastTo(Minion)
        manigance = TrouverTracksuitMafia(effect)
        if manigance is not None:
            manigance.TuckCardUnderHere(this, effect)
            return
        tueur = message.killer
        if tueur is not None and Unit2.IsType(tueur) and tueur.IsInPlay():
            Faces.GiveStatus([tueur], "Stunned", effect)
            Faces.GiveStatus([tueur], "Confused", effect)

    return [
        AbilityFactory.WhenUnitBeDefeated(AbilityType.WhenDefeated, "This", vaincu),
    ]
