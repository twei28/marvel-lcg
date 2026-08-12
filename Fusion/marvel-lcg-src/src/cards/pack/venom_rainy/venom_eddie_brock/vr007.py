from . import *

# Venomous Bite — custom « Rainy »
# Hero Action (attack): Deal 5 damage to an enemy. Then, stun that enemy. If
#   no enemy was stunned this way, heal 2 damage from Venom.

def GetAbilities() -> Sequence['Ability']:

    def venomous_bite(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)

        cibles = list(effect.targets)
        this.DealDamage(cibles, 5, effect)

        etourdi = False
        for cible in cibles:
        # CORRECTIF (4/8/2026) : `IsInField` n'existe sur AUCUNE face du
        # moteur. La carte plantait des qu'elle arrivait ici. La bonne
        # methode est `IsInPlay`.
            if cible.IsInPlay() and not cible.IsStunned():
                Faces.GiveStatus([cible], "Stunned", effect)
                etourdi = cible.IsStunned()

        if not etourdi:
            initiator = effect.GetInitiator()
            this.HealthUnits([initiator.GetIdentity()], 2, effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            venomous_bite
        ).SetPlay(hero_form_only=True)
        .SetLabel('attack')
        .SetTarget(Enemy),
    ]
