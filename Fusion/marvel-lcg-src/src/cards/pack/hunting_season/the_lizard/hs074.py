from . import *

# Shed Skin

def GetAbilities() -> Sequence['Ability']:

    def reveler(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        v = Vilain(effect)
        if v is None:
            return
        v.HealHealth(3, effect)
        for etat in ("Confused", "Stunned", "Exposed", "Tough"):
            v.LoseState(etat, effect, "All")
        Faces.GiveStatus([v], "Tough", effect)

    def boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        v = Vilain(effect)
        if v is not None:
            Faces.GiveStatus([v], "Tough", effect)

    return [
        AbilityFactory.WhenThisRevealed(None, reveler),
        AbilityFactory.WhenCardBecomeBoost("This", boost),
    ]
