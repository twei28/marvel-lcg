from . import *

# Psionic Slash
# When Revealed: If the Mary Walker attachment is in play, flip it and reveal
#   Establish Trust. The villain schemes.
# [star] Boost: If Typhoid Mary is activating, deal 3 damage to an ally you control.

def GetAbilities() -> Sequence['Ability']:

    def revele(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        joueur = message.GetToPlayer()
        FlipMaryWalkerVersEstablishTrust(effect, joueur)
        vilain = TrouverMary(effect)
        if vilain:
            vilain.DoSchemes(joueur, effect)

    def boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        this = effect.this.CastTo(Treachery)
        if not MaryActive(effect, "Typhoid Mary"):
            return
        joueur = message.GetToPlayer()
        joueur.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility("Deal 3 damage to an ally you control", lambda targets: this.DealDamage(targets, 3, effect)).SetTarget("YourAlly"),
        )

    return [
        AbilityFactory.WhenThisRevealed(None, revele),
        AbilityFactory.WhenCardBecomeBoost("This", boost),
    ]
