from . import *

# Demon Lieutenant — SBIRE MYSTIC. PV 6, ATK 3, SCH 1, Boost 2, Retaliate 1, Teamwork (MYSTIC) (natifs).
# [star] Demon Lieutenant's attacks gain overkill.
# [star] Boost : If this activation is an attack, this attack gains overkill and this card gets +1 boost icon for this activation.
#
# Cartes de reference : mp013 (`WhenUnitWouldAttack` + `GainOverKill`), 56178 (`GainBoostIcons`), sl073 (boost sur `would_atk_message`).
# ⚠ Mots-pieges : « ITS attacks » (celles du Lieutenant, pas celles d'un autre ennemi) ; Boost « IF this activation is an ATTACK » : rien pour une manigance ;
# « +1 boost icon FOR THIS ACTIVATION » : l'icone s'ajoute a l'activation en cours.


def GetAbilities() -> Sequence['Ability']:
    def overkill(effect: 'Effect', message: 'Message.WhenUnitWouldAttack') -> None:
        message.GainOverKill(effect)

    def boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        if hasattr(message, "would_atk_message"):
            message.would_atk_message.GainOverKill(effect)
            effect.this.CastTo(Minion).GainBoostIcons(1, effect)

    return [
        AbilityFactory.WhenUnitWouldAttack(AbilityType.NonKeyword, "This", overkill),
        AbilityFactory.WhenCardBecomeBoost("This", boost),
    ]
