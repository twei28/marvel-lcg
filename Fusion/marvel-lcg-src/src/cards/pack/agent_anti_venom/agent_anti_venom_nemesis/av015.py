from . import *

# * Infected Scorpion — custom « DesignHacker » (sbire nemesis)
# Quickstrike.
# Forced Interrupt: When Infected Scorpion attacks an ally, prevent all damage
#   to that ally. That ally gains traitor.
#
# ⚠ PAS `WhenUnitWouldAttack` : a ce moment-la l'attaque vise le joueur, le
# defenseur n'est pas encore designe, et `attacked_targets` ne contient jamais
# d'allie. La capacite ne partait donc JAMAIS (constate le 4/8/2026, des que
# Puzzle.Attack a rendu la carte testable). `WhenUnitWouldAttackUnit` est envoye
# une fois par unite reellement attaquee, defenseur compris.
#
# La prevention passe par une interruption temporaire posee sur l'allie et
# bornee a CETTE attaque (`is_from_attack=message.would_atk_message`) : c'est le
# montage decrit en commentaire dans `Message.WhenUnitWouldAttackUnit`, qui n'a
# pas de `PreventDamage` a lui.

def GetAbilities() -> Sequence['Ability']:

    def infected_scorpion(effect: 'Effect', message: 'Message.WhenUnitWouldAttackUnit') -> None:
        this = effect.this.CastTo(Minion)
        Unused(this)

        cible = message.target
        if cible is None or not Ally.IsType(cible):
            return

        def prevenir(effect2: 'Effect', message2: 'Message.WhenUnitWouldTakeDamage') -> None:
            message2.PreventDamage("All", effect2)

        cible.effect.RegisterTemp(
            AbilityFactory.WhenUnitWouldTakeDamage(
                AbilityType.Temp0,
                "This",
                prevenir,
                is_from_attack=message.would_atk_message,
            ),
            unregister_after_exec=True,
        )

        GainTraitor(cible, effect)

    return [
        AbilityFactory.WhenUnitWouldAttackUnit(
            AbilityType.ForcedInterrupt,
            "This",
            Ally,
            infected_scorpion,
        ),
    ]
