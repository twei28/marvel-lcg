from . import *

# Kate's Aviators — ITEM
# Uses (2 style counters).
# Hero Action: Exhaust Kate's Aviators and remove 1 style counter from it ->
#   draw 1 card.
#
# Modele : Surveillance Team (core/01064.py), deux `.SetCostFunc(...)`
# chaines (Exhaust + Counter) sur la meme ability.
#
# CORRECTIF (test de comportement) : le desc imprime porte deja "Uses":
# "2,style", que `HasUses` (mixin de `Upgrade`, actif sur TOUTE carte du
# type) applique automatiquement a l'entree en jeu -- Surveillance Team, le
# modele cite, ne declare d'ailleurs AUCUN `ThisEnterPlayWithCounters`
# lui-meme, pour cette raison. La carte ici en ajoutait un DEUXIEME en plus,
# doublant le compte (4 au lieu de 2 a l'entree, 3 au lieu de 1 apres la
# premiere depense) : confirme par sonde (compteurs={'style': 3} apres une
# seule activation, alors que 2 - 1 = 1 est attendu).


def GetAbilities() -> Sequence['Ability']:

    def kates_aviators(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(this)

        initiator = effect.GetInitiator()
        if initiator:
            initiator.DrawUp(1, effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            kates_aviators,
        ).SetCostFunc(CostFunc.Exhaust("This"))
        .SetCostFunc(CostFunc.Counter("This", 1, 'style')),
    ]
