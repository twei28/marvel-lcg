from . import *

# Punch, Reverse Punch — EVENEMENT 1★ [physical], aspect Basic (Iron Fist 23). ATTACK.
# [star] Discount 1 (Martial Artist).
# Hero Action (attack): Deal 1 damage to an enemy. Deal 1 damage to an enemy.
#
# MOTS-CLES : discount.md (fiche lue).
#
# CARTES DE REFERENCE
#  - `64004` Fists of Fury (meme pack) : « Deal 1 damage to an enemy. » repete = premiere cible par `SetTarget(Enemy)`,
#    les suivantes choisies a la resolution (`ChooseAbilities(ForChoiceAbility(...).SetTarget(Enemy))`).
#  - `ua030` Nerve Strike : `DiscountAbility(1, ['MARTIAL ARTIST'])` sur un evenement d'attaque.
#
# TEXTE CONTRE CODE
#  ⚠ Deux phrases = deux choix de cible INDEPENDANTS (meme ennemi possible), 1 degat chacun (jamais 2 d'un coup).
#  ⚠ « Hero Action (attack) » : sous-type dedie, etiquette d'attaque.


def GetAbilities() -> Sequence['Ability']:

    def punch_reverse_punch(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(message)
        this.DealDamage([t for t in effect.targets if t is not None], 1, effect)
        joueur = JoueurDeCetteCarte(effect)
        if joueur is None:
            return

        def frapper(cibles: Sequence['CardFace']) -> None:
            this.DealDamage([c for c in cibles if c is not None], 1, effect)

        joueur.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility("Deal 1 damage to an enemy", frapper).SetTarget(Enemy),
        )

    return [
        DiscountAbility(1, ['MARTIAL ARTIST']),
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            punch_reverse_punch,
        ).SetPlay().SetLabel('attack')
        .SetTarget(Enemy),
    ]
