from . import *

# Evasive Shot
# Hero Interrupt (defense): When you would take any amount of damage from an
#   attack, prevent 4 of that damage. Then, deal 1 damage to the attacker for
#   each arrow counter on Kate's Bow (to a maximum of 5).
#
# Modele du prevent+riposte : Energy Barrier (msm/05017.py), meme
# `message.PreventDamage(x, effect)` puis `this.DealDamage(...)`. La cible
# n'est pas un choix du joueur mais « the attacker » : `message.attacker`
# (AttackerNoneMessage, message_type.py:145), comme Parting Shots
# (agent_13/ag005.py).


def GetAbilities() -> Sequence['Ability']:

    def evasive_shot(effect: 'Effect', message: 'Message.WhenUnitWouldTakeDamage') -> None:
        this = effect.this.CastTo(Event)

        message.PreventDamage(4, effect)

        attaquant = message.attacker
        if attaquant is None:
            return

        arc = TrouverArcEnJeu(effect)
        degats = min(5, arc.GetCounters('arrow')) if arc else 0
        if degats > 0:
            this.DealDamage([attaquant], degats, effect)

    return [
        AbilityFactory.WhenUnitWouldTakeDamage(
            AbilityType.HeroInterrupt,
            "You",
            evasive_shot,
            is_from_attack=True,
        ).SetPlay().SetLabel('defense'),
    ]
