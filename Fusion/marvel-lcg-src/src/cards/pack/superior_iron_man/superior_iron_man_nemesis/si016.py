from . import *

# * Tony Stark A.I.
#
# Guard/Patrol lus nativement depuis desc (fiches guard.md/patrol.md).
# "Armored 2" : mot-cle MAISON non defini sur la carte. Glossaire MC4DB
# (aligne le 29/09/2026, voir docs/reference/mots-cles/armored.md) : « When a
# character with this keyword would take any amount of damage FROM AN ATTACK,
# prevent X of that damage » : a CHAQUE attaque, jamais hors attaque (une
# trahison qui blesserait ce sbire passe en entier). Forced Interrupt sur
# `WhenUnitWouldTakeDamage(..., is_from_attack=True)`, modele Armored Rhino
# Suit (core/rhino/01098.py). Jusque-la (arbitrage du 29/08/2026) il prevenait
# 2 degats de TOUTE instance. Degats au joueur : voir si015.py (meme
# simplification assumee "the Tony Stark player" -> "you").

def GetAbilities() -> Sequence['Ability']:

    def when_revealed(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Minion)
        player = message.GetToPlayer()
        this.DealDamage([player.GetIdentity()], 1, effect)

    def boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        this = effect.this.CastTo(Minion)
        player = message.GetToPlayer()
        this.DealDamage([player.GetIdentity()], 1, effect)

    def armored_2(effect: 'Effect', message: 'Message.WhenUnitWouldTakeDamage') -> None:
        message.PreventDamage(2, effect)

    return [
        AbilityFactory.WhenThisRevealed(
            None,
            when_revealed,
        ),
        AbilityFactory.WhenCardBecomeBoost(
            "This",
            boost,
        ),
        AbilityFactory.WhenUnitWouldTakeDamage(
            AbilityType.ForcedInterrupt,
            "This",
            armored_2,
            is_from_attack=True,
        ),
    ]
