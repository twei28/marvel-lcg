from . import *

# Masque's Minions — sbire nemesis de Hawkeye (Kate Bishop), Guard
# Forced Interrupt: When this minion would be defeated, place 1 minion
#   counter on it and heal all damage from him.
# Forced Interrupt: When this minion has 2 or more counters on it, discard
#   it.
#
# Les deux lignes imprimees se resolvent en SEQUENCE sur le meme
# declencheur (« would be defeated ») : la seconde condition (2+ compteurs)
# ne peut se verifier qu'apres la pose du premier, donc une seule ability qui
# enchaine pose + soin + verification est equivalente et plus simple qu'une
# seconde ability separee qui devrait re-ecouter un evenement de compteur.
# « heal all damage from it » : `this.HealthUnits([this], "All", effect)`,
# modele Biomechanical Upgrades (core/the_doomsday_chair/01185.py).


def GetAbilities() -> Sequence['Ability']:

    def masques_minions(effect: 'Effect', message: 'Message.WhenUnitWouldBeDefeated') -> None:
        this = effect.this.CastTo(Minion)

        message.SetBeInstead(effect)
        Faces.PlaceCountersOn([this], 1, 'minion', effect)
        this.HealthUnits([this], "All", effect)

        if this.GetCounters('minion') >= 2:
            Faces.DiscardAll([this], effect)

    return [
        AbilityFactory.WhenUnitWouldBeDefeated(
            AbilityType.ForcedInterrupt,
            "This",
            masques_minions,
        ),
    ]
