from . import *

# Psychic Entanglement (manigance annexe PSIONIC, Victory 1, Boost 2). « Threat cannot be removed from other side schemes. When Defeated : Deal each player a
# facedown encounter card. » Victory 1 : natif.
# Cartes de reference : `AbilityFactory.ThreatCannotBeRemovedFromWhile` (scheme.py : refuse TOUT retrait, thwart compris), 27107 Brute Force Barricade (EXACTE : `ThreatCannotBeRemovedFromWhile(SchemeSide2, conditions=[effect.this != message.trigger])`), 04141 Prison Camps / hf029 (`WhenSchemeBeDefeated`).
# ⚠ « OTHER side schemes » : toute manigance annexe SAUF celle-ci ; la manigance PRINCIPALE n'est pas visee (la menace peut en partir).


def GetAbilities() -> Sequence['Ability']:
    def vaincue(effect: 'Effect', message: 'Message.WhenSchemeBeDefeated') -> None:
        Unused(message)
        DonnerUneCarteFaceCachee(effect)

    return [
        AbilityFactory.ThreatCannotBeRemovedFromWhile(SchemeSide2, conditions=[lambda effect, message: effect.this != message.trigger]),
        AbilityFactory.WhenSchemeBeDefeated(AbilityType.WhenDefeated, "This", vaincue),
    ]
