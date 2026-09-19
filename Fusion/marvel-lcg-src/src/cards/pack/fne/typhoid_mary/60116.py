from . import *

# Psi Nova
# When Revealed: Deal 1 damage to each character you control. You are stunned.
# [star] Boost: If Typhoid Mary is activating, you are stunned.

def GetAbilities() -> Sequence['Ability']:

    def revele(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Treachery)
        joueur = message.GetToPlayer()
        this.DealDamage(list(joueur.GetControlCharacters()), 1, effect)
        Faces.GiveStatus([joueur.GetIdentity()], "Stunned", effect)

    def boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        if MaryActive(effect, "Typhoid Mary"):
            Faces.GiveStatus([message.GetToPlayer().GetIdentity()], "Stunned", effect)

    return [
        AbilityFactory.WhenThisRevealed(None, revele),
        AbilityFactory.WhenCardBecomeBoost("This", boost),
    ]
