from . import *

# Unrestrained (1/2) — ATTACK
# Hero Action (attack): Deal 7 damage to an enemy. If the villain takes
#   overkill damage from this attack, stun and confuse the villain.
#
# Modele : wsp/13013.py (Into the Fray), `DealDamage(..., 7, effect,
# if_this_attack_deal_excess_damage=action)` -- le callback est appele avec
# le montant d'exces si la cible est vaincue avec trop-plein, quelle que
# soit son identite. La cible est deja connue via `effect.targets[0]`
# (choisie AVANT l'appel a DealDamage par `.SetTarget(Enemy)`) : on ne
# stun/confuse que si CETTE cible est le vilain (`Villain.IsType`), modele
# core/spider_man/32008.py (Steel Fist) pour `Faces.GiveStatus`.


def GetAbilities() -> Sequence['Ability']:

    def unrestrained(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(this)

        def on_excess(value: int) -> None:
            Unused(value)
            target = effect.targets[0]
            if Villain.IsType(target):
                Faces.GiveStatus([target], "Stunned", effect)
                Faces.GiveStatus([target], "Confused", effect)

        this.DealDamage(
            effect.targets, 7, effect,
            if_this_attack_deal_excess_damage=on_excess,
        )

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            unrestrained,
        ).SetPlay().SetLabel('attack')
        .SetTarget(Enemy)
        .SetName("Unrestrained"),
    ]
