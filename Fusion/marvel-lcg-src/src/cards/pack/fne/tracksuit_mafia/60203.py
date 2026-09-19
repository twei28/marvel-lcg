from . import *

# Tracksuit Bro (CRIMINAL, TRACKSUIT) — Teamwork (TRACKSUIT), Vulnerable : bases.
# When Defeated: Tuck this card under the Tracksuit Mafia side scheme.
#   Otherwise, shuffle this card into the encounter deck.

def GetAbilities() -> Sequence['Ability']:

    def vaincu(effect: 'Effect', message: 'Message.WhenUnitBeDefeated') -> None:
        this = effect.this.CastTo(Minion)
        manigance = TrouverTracksuitMafia(effect)
        if manigance is not None:
            manigance.TuckCardUnderHere(this, effect)
        else:
            Faces.ShuffleAllTo([this], "EncounterDeck", effect)

    return [
        AbilityFactory.WhenUnitBeDefeated(AbilityType.WhenDefeated, "This", vaincu),
    ]
