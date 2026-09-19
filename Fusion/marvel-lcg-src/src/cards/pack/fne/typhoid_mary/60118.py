from . import *

# Hail of Blades
# When Revealed: If the Mary Walker attachment is in play, flip it and reveal
#   Establish Trust. The villain attacks you (even if you are in alter-ego form).
# [star] Boost: If Bloody Mary is activating, take 2 damage.

def GetAbilities() -> Sequence['Ability']:

    def revele(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        joueur = message.GetToPlayer()
        FlipMaryWalkerVersEstablishTrust(effect, joueur)
        vilain = TrouverMary(effect)
        if vilain:
            vilain.DoAttackYou(joueur, effect)

    def boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        this = effect.this.CastTo(Treachery)
        if MaryActive(effect, "Bloody Mary"):
            this.DealDamage([message.GetToPlayer().GetIdentity()], 2, effect)

    return [
        AbilityFactory.WhenThisRevealed(None, revele),
        AbilityFactory.WhenCardBecomeBoost("This", boost),
    ]
