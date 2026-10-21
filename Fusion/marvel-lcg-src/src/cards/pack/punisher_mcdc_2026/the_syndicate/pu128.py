from . import *

# * Lady Octopus — SBIRE UNIQUE. CRIMINAL. GENIUS. SYNDICATE. SCH 2, ATQ 1★, 4 PV, Boost 1, Incite 2, Toughness.
# Incite 2. Toughness.
# ★ Forced Response : After Lady Octopus attacks, place 2 threat on the main scheme.
# When Defeated : voir __init__.py.
#
# Cartes de reference : jigsaw/pu056a.py (`PlaceThreatOnSchemes` sur la principale), `AfterUnitAttackUnit`.
# Incite et Toughness : natifs (fiches mots-cles/incite.md, toughness.md).
# ⚠ « After Lady Octopus ATTACKS » : toute attaque (sur un joueur, un allie...), pas seulement « you » ; 2 menaces
# fixes, pas par joueur.

def GetAbilities() -> Sequence['Ability']:

    def apres_attaque(effect: 'Effect', message: 'Message.AfterUnitAttackUnit') -> None:
        this = effect.this
        schemes = Worlds.GetMainSchemes(effect)
        if schemes:
            this.PlaceThreatOnSchemes(schemes[:1], 2, effect)

    return [
        AbilityFactory.AfterUnitAttackUnit(AbilityType.ForcedResponse, "This", None, apres_attaque),
        DefaiteSyndicate(),
    ]
