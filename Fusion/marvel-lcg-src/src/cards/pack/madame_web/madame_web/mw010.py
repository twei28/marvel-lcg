from . import *

# Gathering of Five — custom « Kajislav »
# Action: Discard the top card of your deck. If that card's printed resource has:
#   [physical] - Deal 3 damage to your identity.
#   [energy]   - Madame Web gets +2 ATK until the end of the phase.
#   [mental]   - Remove 2 threat from a scheme.
#   [wild]     - Heal all damage from your identity.
#
# Les quatre branches se cumulent (une carte peut porter plusieurs icones), sur
# le modele de Magic Blast (09004).

def GetAbilities() -> Sequence['Ability']:

    def rassemblement(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)

        initiator = effect.GetInitiator()
        identity = initiator.GetIdentity()

        face = initiator.DiscardDeckTopCard(effect)
        res = FacesCounter.GetPrintedResources([face])

        if res.r:
            this.DealDamage([identity], 3, effect)
        if res.y:
            hero = initiator.GetHero()
            if hero:
                hero.GainUntilPhaseEnd(effect, attack=2)
        if res.b:
            def retirer_menace(targets: Sequence['CardFace']):
                this.RemoveThreatFromSchemes(targets, 2, effect)

            initiator.ChooseAbilities(
                effect,
                AbilityFactory.ForChoiceAbility(
                    "Remove 2 threat from a scheme",
                    retirer_menace,
                ).SetTarget(Scheme2)
            )
        if res.g:
            this.HealthUnits([identity], "All", effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.Action,
            rassemblement
        ).SetPlay(),
    ]
