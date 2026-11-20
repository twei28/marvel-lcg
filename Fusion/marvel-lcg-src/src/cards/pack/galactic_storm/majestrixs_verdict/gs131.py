from . import *

# Jailor of Chandilar — SBIRE (Majestrix's Verdict), 4 exemplaires. SHI'AR. MNG 1, ATQ 2, PV 6. 1 icone de boost.
# Retaliate 1.
# When Defeated: Remove 2 threat from Imprisoned on Chandilar.
# [star] Boost: Place 1 threat on Imprisoned on Chandilar.
#
# Cartes de reference :
#  - Retaliate : BASE AUTOMATIQUE (`desc.Retaliate`).
#  - When Defeated : `WhenUnitBeDefeated(WhenDefeated, "This")` (modele sk155) + `RemoveThreatFromSchemes([prison], 2)`
#    (RECETTES §2, modele an004).
#  - Boost : `WhenCardBecomeBoost("This")` + `PlaceThreatOnSchemes([prison], 1)`.
#
# ⚠ Mots-pieges : la menace retiree/posee vise la PRISON (rien si elle n'est pas en jeu) ; retirer la derniere
# menace de la prison declenche sa propre Interruption forcee (liberation d'un STARJAMMER).


def GetAbilities() -> Sequence['Ability']:

    def vaincu(effect: 'Effect', message: 'Message.WhenUnitBeDefeated') -> None:
        Unused(message)
        prison = Prison(effect)
        if prison is not None:
            effect.this.RemoveThreatFromSchemes([prison], 2, effect)

    def boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        Unused(message)
        prison = Prison(effect)
        if prison is not None:
            effect.this.PlaceThreatOnSchemes([prison], 1, effect)

    return [
        AbilityFactory.WhenUnitBeDefeated(AbilityType.WhenDefeated, "This", vaincu),
        AbilityFactory.WhenCardBecomeBoost("This", boost),
    ]
