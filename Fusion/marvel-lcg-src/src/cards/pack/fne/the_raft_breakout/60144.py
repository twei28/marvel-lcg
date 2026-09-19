from . import *

# * Absorbing Man (BRUTE, ELITE, PRISONER) — Villainous : base.
# [star] Forced Interrupt: When Absorbing Man attacks you, tuck the top card
#   of your deck under him. Absorbing Man gets +1 ATK for this attack for each
#   different resource type ([energy], [mental], [physical], and [wild]) on
#   cards tucked under him.
# FacesCounter.GetPrintedResourcesTypes = nombre de types differents
# (["YY","B","B"] -> 2), le joker compte pour un type.

def GetAbilities() -> Sequence['Ability']:

    def attaque(effect: 'Effect', message: 'Message.WhenUnitWouldAttack') -> None:
        this = effect.this.CastTo(Minion)
        joueur = message.GetAgainstPlayer()
        if joueur is None:
            return
        dessus = joueur.player_deck.GetTop()
        if dessus is not None:
            this.TuckCardUnderHere(dessus, effect)
        cachees = list(this.GetPlacedCardArea().Get())
        bonus = FacesCounter.GetPrintedResourcesTypes(cachees) if cachees else 0
        if bonus > 0:
            message.GainATKForThisAttack(bonus, effect)

    return [
        AbilityFactory.WhenUnitAttackYou(AbilityType.ForcedInterrupt, "This", attaque),
    ]
