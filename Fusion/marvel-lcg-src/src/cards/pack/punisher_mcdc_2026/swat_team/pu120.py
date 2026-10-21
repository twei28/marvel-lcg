from . import *

# * Cole North — SBIRE UNIQUE. DETECTIVE. POLICE. SCH 2★, ATQ 2★, 4 PV, Boost 3, Patrol.
# Patrol.
# ★ When Cole North schemes, place that threat on SWAT, if able.
# ★ Forced Interrupt : When Cole North would attack, if there are fewer than 3 wanted counters on SWAT, remove 2 threat
#   from the main scheme instead.
#
# Cartes de reference : `MenaceSurSwat()` (__init__.py), jigsaw/pu059.py (`WhenUnitWouldAttack` + `SetBeInstead`),
# `RemoveThreatFromSchemes` (fne/drive/60189.py). Patrol : natif.
# ⚠ « INSTEAD » : pas d'attaque (ni degats ni boost) ; « fewer than 3 wanted counters » : 0, 1 ou 2 ; a 3 ou plus il
# attaque normalement.

def GetAbilities() -> Sequence['Ability']:

    def au_lieu_d_attaquer(effect: 'Effect', message: 'Message.WhenUnitWouldAttack') -> None:
        this = effect.this
        schemes = Worlds.GetMainSchemes(effect)
        message.SetBeInstead(effect)
        if schemes:
            this.RemoveThreatFromSchemes(schemes[:1], 2, effect)

    return [
        MenaceSurSwat(),
        AbilityFactory.WhenUnitWouldAttack(
            AbilityType.ForcedInterrupt, "This", au_lieu_d_attaquer,
            conditions=[lambda effect, message: CompteursRecherche(effect) < 3],
        ),
    ]
