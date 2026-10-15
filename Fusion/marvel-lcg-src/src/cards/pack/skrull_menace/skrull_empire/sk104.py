from . import *

# Long Live the Empire — TRAITRISE x2 (Skrull Empire). 1 boost + ★.
# When Revealed: Heal 2 damage from the villain for each SKRULL enemy in play.
#   If no damage was healed this way, this card gains surge.
# ★ Boost: Heal 1 damage from the villain for each SKRULL enemy in play.
#
# Cartes de reference : `36039` (`ThisCardGainSurge`) ; `mf016` (Boost).
# ⚠ « the villain » n'a PAS de PV dans ce scenario : on soigne l'environnement
# Skrull Empire (`SoignerLeMechant`, livret p. 8). « each SKRULL ENEMY » :
# sbires ET mechant (le mechant compte). « If NO damage was healed » : un
# environnement intact => surge.


def GetAbilities() -> Sequence['Ability']:

    def vive(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this
        Unused(message)
        if SoignerLeMechant(effect, this, 2 * len(EnnemisSkrull(effect))) == 0:
            ThisCardGainSurge(effect)

    def boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        Unused(message)
        SoignerLeMechant(effect, effect.this, len(EnnemisSkrull(effect)))

    return [
        AbilityFactory.WhenThisRevealed(None, vive),
        AbilityFactory.WhenCardBecomeBoost("This", boost),
    ]
