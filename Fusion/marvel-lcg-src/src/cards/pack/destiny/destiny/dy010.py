from . import *

# Path of Violence (x3) : EVENEMENT (ATTACK. PSIONIC.), cout 2, [physical]. Classe Hero.
# Hero Action (attack): Deal 4 damage to an enemy. Deal 1 additional damage for each icon ([star] and [boost]) on the card tucked under Glimpse of the Future.
#
# CARTES DE REFERENCE
#  - `01054` Uppercut (core) : `WhenInYourPlayTurn(HeroAction, op).SetPlay().SetLabel('attack')` + `this.DealDamage(effect.targets, n, effect)`.
#
# TEXTE CONTRE CODE
#  « Deal 4 damage » : degats directs, pas une attaque de base (aucune ATQ du heros). « 1 additional damage for EACH icon » : 4 + X, X lu a la resolution. « an enemy » : vilain ou sbire.
#  Chiffres : cout 2, 4 degats + X.


def GetAbilities() -> Sequence['Ability']:

    def path_of_violence(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        joueur = effect.GetInitiator()
        this.DealDamage(effect.targets, 4 + IconesSousGlimpse(joueur), effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            path_of_violence,
        ).SetPlay().SetLabel('attack')
        .SetTarget(Enemy),
    ]
