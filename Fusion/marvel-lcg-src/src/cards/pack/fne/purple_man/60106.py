from . import *

# "Protect." (obligation, Uses 3 command) — Forced Action: ... -> give the
# villain a tough status card.

def GetAbilities() -> Sequence['Ability']:

    def proteger(effect: 'Effect', joueur: 'Player', this: 'Obligation') -> None:
        vilain = Worlds.FindVillain(effect)
        if vilain:
            Faces.GiveStatus([vilain], "Tough", effect)

    return [
        *ObligationCommandee("Protect.", proteger),
    ]
