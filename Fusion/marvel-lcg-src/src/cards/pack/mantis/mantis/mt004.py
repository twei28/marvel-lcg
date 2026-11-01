from . import *

# Pressure Point Strike (x2) : EVENEMENT (ATTACK), cout 2, [physical]. Hero Class.
# Hero Action (attack): Deal 4 damage to an enemy. If that enemy is confused, you may either deal 1 additional damage to that enemy, or discard a confused status card
# from that enemy to draw 1 card.
#
# CARTES DE REFERENCE
#  - `05003` Big Hands : evenement d'attaque `this.DealDamage(effect.targets, 4, effect)` + `SetLabel('attack')` + `SetTarget(Enemy)`.
#  - `53003` Bird of Prey : « you may » = `MayChooseOneAbility(effect, ForChoiceAbility(..))` apres les degats.
#  - `wd005` / `ho001a` : `face.DiscardConfused(effect, rule=1)` rend le nombre de statuts REELLEMENT defausses.
#
# TEXTE CONTRE CODE
#  « If that enemy IS confused » : lu APRES les 4 degats, sur le meme ennemi (s'il est vaincu, rien). « you MAY either A, or B » : choix facultatif entre deux branches exclusives.
#  « discard a confused status card from that enemy TO draw 1 card » : FAQ imprimee (« to ») : la carte n'est piochee que si le statut a REELLEMENT ete defausse.
#  Chiffres : cout 2, 4 degats, +1 degat, 1 carte.


def GetAbilities() -> Sequence['Ability']:

    def pressure_point_strike(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(message)
        joueur = effect.GetInitiator()
        cible = effect.targets[0] if effect.targets else None
        this.DealDamage(effect.targets, 4, effect)
        if cible is None or not cible.card.IsOnField() or not cible.IsConfused():
            return

        def retirer_et_piocher(_cibles: Sequence['CardFace']) -> None:
            if cible.DiscardConfused(effect, rule=1) > 0:
                joueur.DrawUp(1, effect)

        joueur.MayChooseOneAbility(
            effect,
            AbilityFactory.ForChoiceAbility(
                "Deal 1 additional damage to that enemy",
                lambda _cibles:
                    this.DealDamage([cible], 1, effect),
            ),
            AbilityFactory.ForChoiceAbility(
                "Discard a confused status card from that enemy to draw 1 card",
                retirer_et_piocher,
            ),
        )

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            pressure_point_strike,
        ).SetPlay().SetLabel('attack')
        .SetTarget(Enemy),
    ]
