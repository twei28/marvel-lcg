from . import *

# Fists of Fury — EVENEMENT, cout 1, [physical]. ATTACK. x2 (Iron Fist 5/15).
# Hero Action (attack): Deal 1 damage to an enemy. Deal 1 damage to an enemy. Deal 1 damage to
#   an enemy.
#
# CARTES DE REFERENCE
#  - meme structure imprimee « Deal N damage to an enemy. Deal N damage to an enemy. » :
#    `cw/56008` Tooth and Claw (1re cible par `SetTarget(Enemy)`, les suivantes choisies a la
#    resolution) et `gambit/37007` Royal Flush (trois fois `ChooseAbilities(ForChoiceAbility(...)
#    .SetTarget(Enemy))`).
#
# TEXTE CONTRE CODE
#  ⚠ Trois phrases = trois choix de cible INDEPENDANTS : le meme ennemi peut etre choisi plusieurs
#    fois (un ennemi vaincu ne peut plus l'etre, il n'est plus en jeu).
#  ⚠ 1 degat chacune, trois fois : jamais 3 degats d'un coup.


def GetAbilities() -> Sequence['Ability']:

    def fists_of_fury(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(message)
        this.DealDamage([t for t in effect.targets if t is not None], 1, effect)
        joueur = JoueurDeCetteCarte(effect)
        if joueur is None:
            return

        def frapper(cibles: Sequence['CardFace']) -> None:
            this.DealDamage([c for c in cibles if c is not None], 1, effect)

        for _ in range(2):
            joueur.ChooseAbilities(
                effect,
                AbilityFactory.ForChoiceAbility("Deal 1 damage to an enemy", frapper).SetTarget(Enemy),
            )

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            fists_of_fury,
        ).SetPlay().SetLabel('attack')
        .SetTarget(Enemy),
    ]
