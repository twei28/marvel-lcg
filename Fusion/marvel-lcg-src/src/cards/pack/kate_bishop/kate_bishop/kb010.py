from . import *

# Athletic Agility — SKILL
# You gain Agile 1. (Reduce damage taken from undefended attacks by 1, to a
#   minimum of 1.)
# Interrupt: When you prevent any amount of damage from an attack, deal 1
#   damage to an enemy.
#
# « Agile » n'existe pas comme mot-cle moteur (aucune carte du depot ne
# l'utilise) : implemente directement en code plutot qu'en `desc`, sur le
# modele de `while_defending=False` (damage.py:44, "l'unite qui prend ces
# degats n'est pas la defenseuse" = attaque non defendue) pour cibler
# precisement les attaques non defendues.
#
# La seconde ligne reagit a TOUTE prevention de degats subie pendant une
# attaque (la sienne ou celle d'une autre carte, ex. Evasive Shot) :
# `AbilityFactory.AfterDamageBePrevented` sans `prevent_by`, deja utilisee
# telle quelle par kb008.
#
# CORRECTIF (test de comportement) : `.SetTarget(Enemy)` ne declenche jamais
# `riposte` (meme defaut que kb001a/kb008 -- une capacite passive, sans Play
# ni CostFunc, ne peut pas s'appuyer sur la resolution de cible du framework).
# Fixe en lisant l'attaquant directement via `message.would_atk_message.attacker`.


def GetAbilities() -> Sequence['Ability']:

    def reduire_degats(effect: 'Effect', message: 'Message.WhenUnitWouldTakeDamage') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(this)

        if message.will_take_damage > 1:
            message.PreventDamage(1, effect)

    def riposte(effect: 'Effect', message: 'Message.AfterDamageBePrevented') -> None:
        this = effect.this.CastTo(Upgrade)
        if message.would_atk_message is None:
            return
        attaquant = message.would_atk_message.attacker
        if attaquant is None:
            return
        this.DealDamage([attaquant], 1, effect)

    return [
        AbilityFactory.WhenUnitWouldTakeDamage(
            AbilityType.Interrupt,
            "You",
            reduire_degats,
            is_from_attack=True,
            while_defending=False,
        ),
        AbilityFactory.AfterDamageBePrevented(
            AbilityType.Interrupt,
            riposte,
            who_not_take_damage="You",
            is_from_attack=True,
        ),
    ]
