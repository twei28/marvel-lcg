from . import *

# Gamma Strike — custom « Rainy »
# Hero Action (attack): Deal 7 damage to an enemy. If you paid for this card
#   using only [physical] resources, this attack deals 3 additional damage and
#   gains overkill. If you paid for this card using only [mental] resources and
#   played it from your hand, put it into your reserve.
#
# Les deux clauses sont EXCLUSIVES l'une de l'autre par construction : on ne
# peut pas avoir paye « uniquement en [physical] » et « uniquement en [mental] »
# a la fois. La carte offre donc un vrai choix a la depense — frapper plus fort,
# ou garder la carte pour la rejouer.

def GetAbilities() -> Sequence['Ability']:

    def gamma_strike(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)

        joueur = effect.GetInitiator()
        paye = effect.GetPaidResources()

        cibles = effect.targets
        if cibles:
            que_du_physique = paye.OnlyHasColor("R")
            degats = 10 if que_du_physique else 7
            # Modele de Relentless Assault 01053 : l'overkill se transmet par
            # AttackProperty, et les degats partent du HEROS pour que ce soit
            # bien une attaque de sa part.
            heros = joueur.GetHero()
            source = heros if heros is not None else this
            source.DealDamage(
                cibles, degats, effect,
                property=AttackProperty(overkill=que_du_physique),
            )

        if paye.OnlyHasColor("B") and effect.context.play_from_area == joueur.hand_cards:
            RecyclerVersLaReserve(this, joueur, effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            gamma_strike,
        ).SetPlay(hero_form_only=True)
        .SetLabel('attack')
        .SetTarget(Enemy),
    ]
