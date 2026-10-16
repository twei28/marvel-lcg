from . import *

# Auto Defense Bots — SBIRE (Security Protocol 1/7, x4). ROBOT. SWARM. SCH 0, ATK 1, PV 1, 1 boost.
# Guard. Patrol.
# Enters play with 1 shield counter on them.
# Forced Interrupt: When this minion would be defeated, heal all damage from this minion, and remove 1
#   shield counter from here instead.
#
# Cartes de reference : `ss021` / `lj015` (`WhenUnitWouldBeDefeated(ForcedInterrupt, "This", ...)` +
# `SetBeInstead`) ; `sk287` (soin + « instead » sur une defaite evitee) ; `HealthUnits(..., "All")`.
# Guard et Patrol : natifs (`desc`). Compteur maison `shield`.
#
# Mots-pieges : « would be DEFEATED » (l'interruption part quand le sbire va tomber, quelle que soit la cause) ;
# « heal ALL damage » ; « remove 1 shield counter » : UN seul compteur ; « INSTEAD » : le sbire n'est pas vaincu.
# TODO-QUESTION (tx017-Q3) : texte muet quand il ne reste AUCUN compteur shield. Lecture provisoire : le
# sbire n'a plus de bouclier, il est vaincu normalement (sans cela il serait immortel). Voir baxter-questions.md.


def GetAbilities() -> Sequence['Ability']:

    def a_un_bouclier(effect: 'Effect', message: 'Message.WhenUnitWouldBeDefeated') -> bool:
        return effect.this.CastTo(Minion).GetCounters("shield") > 0

    def survivre(effect: 'Effect', message: 'Message.WhenUnitWouldBeDefeated') -> None:
        this = effect.this.CastTo(Minion)
        message.SetBeInstead(effect)
        this.HealthUnits([this], "All", effect)
        Faces.RemoveCountersOn([this], 1, "shield", effect)

    return [
        AbilityFactory.ThisEnterPlayWithCounters(1, "shield"),
        AbilityFactory.WhenUnitWouldBeDefeated(
            AbilityType.ForcedInterrupt,
            "This",
            survivre,
            conditions=[a_un_bouclier],
        ),
    ]
