from . import *
from cards.pack.fne import DiscountAbility

# Nerve Strike — EVENEMENT 3* [energy], aspect Aggression (TMNT Aspects, Inkwire). ATTACK. SKILL.
# [star] Discount 1 (MARTIAL ARTIST).
# Hero Action (attack): Deal 2 damage to an enemy. Stun or confuse that enemy.
#
# MOT-CLE (fiche CREEE avant le code) : docs/reference/mots-cles/discount.md — `DiscountAbility(1,
#   ['MARTIAL ARTIST'])` du pack fne (60023 Know Your Enemy). L'etoile du cout « 3* » n'est qu'un rappel.
# CARTES DE REFERENCE
#  - `60023` Know Your Enemy : meme mot-cle, meme trait.
#  - `35018` Precision Strike : « Deal 2 damage to an enemy » sur une Hero Action (attack).
#  - `ua002` : « Stun or confuse » = choix entre deux `ForChoiceAbility`.
# TEXTE CONTRE CODE
#  ⚠ « THAT enemy » : le meme ennemi que celui qui a pris les 2 degats (s'il est encore en jeu).
#  ⚠ « Stun OR confuse » : une seule des deux, au choix.


def GetAbilities() -> Sequence['Ability']:

    def nerve_strike(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(message)
        if not effect.targets:
            return
        cible = effect.targets[0]
        this.DealDamage([cible], 2, effect)
        if not cible.IsInPlay():
            return
        effect.GetInitiator().ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility(
                "Stun that enemy",
                lambda _c: Faces.GiveStatus([cible], "Stunned", effect),
            ),
            AbilityFactory.ForChoiceAbility(
                "Confuse that enemy",
                lambda _c: Faces.GiveStatus([cible], "Confused", effect),
            ),
        )

    return [
        DiscountAbility(1, ['MARTIAL ARTIST']),
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            nerve_strike,
        ).SetPlay().SetLabel('attack')
        .SetTarget(Enemy),
    ]
