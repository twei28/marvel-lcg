from . import *

# Zooming Around — custom « Nugget »
# Hero Action: Choose a player. Deal 1 damage to each enemy engaged with that
#   player. Remove 1 threat from each scheme. If you paid for this card using
#   a [wild] resource, you may change your form.


def GetAbilities() -> Sequence['Ability']:

    def zoomer(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        initiator = effect.GetInitiator()

        for cible in effect.targets:
            joueur = cible.GetControlByPlayer()
            if joueur is None:
                continue
            # « chaque ennemi engage avec ce joueur » = le vilain plus les
            # sbires engages, montage de la carte officielle Energy Daggers
            # (01046) : le moteur n'expose pas d'engagement pour le vilain.
            vilain = Worlds.FindVillain(effect)
            ennemis = ([vilain] if vilain else []) + joueur.GetEngagedMinions()
            ennemis = [x for x in ennemis if not x.IsDefeated()]
            if ennemis:
                this.DealDamage(ennemis, 1, effect)

        schemes = Worlds.FindCardsOnField(effect, card_type=Scheme2)
        if schemes:
            this.RemoveThreatFromSchemes(schemes, 1, effect)

        if PayeAvecMental(effect):
            YouMayChangeForm(initiator, effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            zoomer,
        ).SetPlay()
        .SetTarget("Players"),
    ]
