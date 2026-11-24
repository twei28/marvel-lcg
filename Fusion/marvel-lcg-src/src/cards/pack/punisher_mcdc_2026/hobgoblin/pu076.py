from . import *

# * Rabble — SBIRE UNIQUE. AERIAL. CRIMINAL. SCH 2, ATQ 2, 3 PV, Boost 1, Vulnerable 1.
# Vulnerable.
# Rabble enters play with 2 drone counters on her.
# Forced Interrupt : When Rabble would take damage → remove 1 drone counter → prevent that damage and discard 2 cards
#   from the encounter deck instead.
#
# Cartes de reference : tmnt_aspect_dual/ud003.py (`ThisEnterPlayWithCounters(2, 'amp')`), mister_fantastic/mf011.py
# (`WhenUnitWouldTakeDamage` + `PreventDamage`), sm/bad_publicity/27174a.py (`Faces.RemoveCountersOn`).
# Vulnerable : natif. Compteur `drone` ajoute a CardFace.COUNTER (21/10/2026).
#
# ⚠ Le retrait du compteur est le COUT : sans compteur, rien n'est empeche et Rabble prend les degats. « prevent THAT
# damage » : tout le degat du coup, pas 1 seul point ; « instead » : on defausse 2 cartes a la place.

def GetAbilities() -> Sequence['Ability']:

    def eviter(effect: 'Effect', message: 'Message.WhenUnitWouldTakeDamage') -> None:
        this = effect.this.CastTo(Minion)
        if this.GetCounters('drone') <= 0:
            return
        Faces.RemoveCountersOn([this], 1, 'drone', effect)
        message.PreventDamage(message.will_take_damage, effect)
        Worlds.DiscardEncounterCards(2, effect)

    return [
        AbilityFactory.ThisEnterPlayWithCounters(2, 'drone'),
        AbilityFactory.WhenUnitWouldTakeDamage(AbilityType.ForcedInterrupt, "This", eviter),
    ]
