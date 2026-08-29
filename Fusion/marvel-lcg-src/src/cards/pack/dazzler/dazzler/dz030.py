from . import *

# Power Ballad
# SONG.
# Reduce the cost to play Power Ballad by 2 if your identity is Dazzler, Jem,
#   Lila Cheney, Luna Snow or Virgo.
# Hero Action: Choose:
#   - Remove 2 threat from a scheme.
#   - Deal 2 damage to an enemy.
#
# `ReduceCostToPlayThis` est la fabrique dediee (helper Discount du pack fne).
# Les cinq noms sont ceux imprimes : quatre d'entre eux ne sont pas dans le jeu,
# la condition reste vraie pour Dazzler et dormante pour les autres, ce qui est
# exactement ce que fait la carte physique.
#
# Le « Choose » est rendu par UNE seule capacite de jeu avec un choix interne,
# et non par deux : le moteur n'admet deux capacites `Play` sur un evenement
# que pour une liste blanche nommee (factory.py), qu'on evite ainsi.


CHANTEUSES = ("Dazzler", "Jem", "Lila Cheney", "Luna Snow", "Virgo")


def GetAbilities() -> Sequence['Ability']:

    def bonne_identite(effect: 'Effect',
                       message: 'Message.WhenCalculateEffectCost') -> bool:
        joueur = effect.GetInitiator()
        if joueur is None:
            return False
        identite = joueur.GetIdentity()
        return identite is not None and any(identite.IsName(n)
                                            for n in CHANTEUSES)

    def ballade(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        joueur = effect.GetInitiator()
        if joueur is None:
            return

        def menace(targets: Sequence['CardFace']) -> None:
            this.RemoveThreatFromSchemes(targets, 2, effect)

        def degats(targets: Sequence['CardFace']) -> None:
            this.DealDamage(targets, 2, effect)

        joueur.MayChooseOneAbility(
            effect,
            AbilityFactory.ForChoiceAbility("Remove 2 threat", menace)
            .SetTarget(Scheme2),
            AbilityFactory.ForChoiceAbility("Deal 2 damage", degats)
            .SetTarget(Enemy),
        )

    return [
        AbilityFactory.ReduceCostToPlayThis(2, conditions=[bonne_identite]),
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            ballade,
        ).SetPlay().SetLabel(),
    ]
