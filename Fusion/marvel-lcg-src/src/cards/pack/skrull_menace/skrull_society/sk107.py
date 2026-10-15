from . import *

# Skrull Scientist — SBIRE (Skrull Society). GENIUS. SKRULL. SCH 3, ATK 0, 3 PV,
# icone Acceleration, ★ + 2 boosts.
# ★ Boost: Heal 2 damage from the villain, after this activation ends.
#
# Carte de reference : `RunAt.AfterEnemyActivationEnd(effect, would_message, op)`
# (operate/run_at.py ; usage dans enemy.py DoAttackYou).
# ⚠ « AFTER this activation ends » : pas tout de suite (sinon le soin pourrait
# annuler un coup fatal deja porte pendant l'attaque). « the villain » : dans
# Skrull Empire, l'environnement (SoignerLeMechantPartout).


def GetAbilities() -> Sequence['Ability']:

    def boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        RunAt.AfterEnemyActivationEnd(effect, message.would_message,
                                      lambda: SoignerLeMechantPartout(effect, 2))

    return [AbilityFactory.WhenCardBecomeBoost("This", boost)]
