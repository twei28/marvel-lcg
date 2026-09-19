from . import *

# * Proxima Midnight (BLACK ORDER, ELITE, PRISONER) — Villainous : base.
# [star] Forced Interrupt: When Proxima Midnight attacks you, choose to either
#   place 1 threat on the main scheme, or Proxima Midnight gets +2 ATK for
#   this attack.

def GetAbilities() -> Sequence['Ability']:

    def attaque(effect: 'Effect', message: 'Message.WhenUnitWouldAttack') -> None:
        this = effect.this.CastTo(Minion)
        joueur = message.GetAgainstPlayer()
        if joueur is None:
            return
        joueur.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility("Place 1 threat on the main scheme", lambda targets: this.PlaceThreatOnSchemes("MainScheme", 1, effect)),
            AbilityFactory.ForChoiceAbility("Proxima Midnight gets +2 ATK for this attack", lambda targets: message.GainATKForThisAttack(2, effect)),
        )

    return [
        AbilityFactory.WhenUnitAttackYou(AbilityType.ForcedInterrupt, "This", attaque),
    ]
