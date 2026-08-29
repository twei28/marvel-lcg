from . import *

# * Tony Stark A.I.
#
# Guard/Patrol lus nativement depuis desc (fiches guard.md/patrol.md).
# "Armored 2" : mot-cle MAISON non defini (absent de tout le jeu et du
# materiel fourni), decision utilisateur (29/08/2026, voir
# docs/reference/mots-cles/armored.md) : previent 2 degats a CHAQUE instance,
# pas seulement au combat -- Forced Interrupt sur `WhenUnitWouldTakeDamage`,
# modele Armored Rhino Suit (core/rhino/01098.py). Degats au joueur : voir
# si015.py (meme simplification assumee "the Tony Stark player" -> "you").

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
        ),
    ]
