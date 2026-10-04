from . import *

# * Crashing Wave — evenement signature, x3 (2-4/15). ATTACK. SUPERPOWER.
# Cout 1.
# Hero Action (attack): Deal 1 damage to an enemy. Flip up to 3 faceup cards
# in your Rising Tide area facedown -> deal 2 additional damage for each card
# flipped facedown this way.
#
# Modele : 01031 Repulsor Blast (meme montage `WhenInYourPlayTurn(HeroAction,
# ...).SetPlay().SetLabel('attack').SetTarget(Enemy)`, degats calcules avant
# `DealDamage`, un seul appel).

def GetAbilities() -> Sequence['Ability']:

    def crashing_wave(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        initiator = effect.GetInitiator()
        if not isinstance(initiator, Player):
            return

        degats = 1
        retournees = RetournerCartesRisingTide(
            effect, initiator, face_visible=True, minimum=0, maximum=3,
            prompt="Flip up to 3 faceup cards in your Rising Tide area facedown",
        )
        degats += 2 * len(retournees)

        this.DealDamage(effect.targets, degats, effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            crashing_wave,
        ).SetPlay().SetLabel('attack')
        .SetTarget(Enemy),
    ]
