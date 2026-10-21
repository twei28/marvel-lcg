from . import *

# * Beetle — SBIRE UNIQUE. AERIAL. CRIMINAL. SYNDICATE. SCH 2, ATQ 2, 5 PV, Boost 3.
# Reduce the amount of damage Beetle takes from non-AERIAL attacks by 1.
# When Defeated : voir __init__.py (`DefaiteSyndicate`).
#
# Cartes de reference : mister_fantastic/mf011.py (`WhenUnitWouldTakeDamage` + `PreventDamage`).
# ⚠ « NON-AERIAL ATTACKS » : seulement les degats d'ATTAQUE (`is_from_attack`) dont l'attaquant n'a pas le trait
# AERIAL ; « by 1 » : au plus 1 point (un coup de 1 est annule, un coup de 3 passe a 2) ; pas d'effet sur les degats
# d'un evenement ou indirects.

def GetAbilities() -> Sequence['Ability']:

    def reduire(effect: 'Effect', message: 'Message.WhenUnitWouldTakeDamage') -> None:
        message.PreventDamage(1, effect)

    return [
        AbilityFactory.WhenUnitWouldTakeDamage(
            AbilityType.ForcedInterrupt, "This", reduire,
            is_from_attack=True,
            conditions=[lambda effect, message: not message.source.HasTrait("AERIAL")],
        ),
        DefaiteSyndicate(),
    ]
