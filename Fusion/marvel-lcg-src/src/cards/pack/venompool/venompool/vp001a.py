from . import *

# * Venompool (face heros)
# MUTANT. SYMBIOTE. WEB-WARRIOR.  THW 1 / ATK 2 / DEF 2 — HS 5 / PV 9
# Fear Factor - Response (thwart): After Venompool defeats an enemy, remove
#   1 threat from a scheme. (Limit 1 [per_hero] per phase.)
#
# Carte de reference : 04001b Clint Barton pour `.LimitOncePerPhase()`, et
# pt006 Covered Fire pour `RemoveThreatFromSchemes(targets, n, effect)` avec
# `SetTarget(Scheme2, range=(1, 1))`.
#
# « Limit 1 [per_hero] per phase » sur une carte d'IDENTITE : l'icone joueur
# ne peut designer que le porteur de la carte (personne d'autre ne declenche
# la Response d'une identite qui n'est pas la sienne). La limite est donc
# bien une limite par phase pour le joueur Venompool, ce que rend
# `LimitOncePerPhase()` — et surtout PAS une limite globale a la table.

def GetAbilities() -> Sequence['Ability']:

    def fear_factor(effect: 'Effect', message: 'Message.AfterUnitDefeatedUnit') -> None:
        this = effect.this.CastTo(Hero)
        Unused(message)

        this.RemoveThreatFromSchemes(effect.targets, 1, effect)

    return [
        AbilityFactory.AfterUnitDefeatedUnit(
            AbilityType.Response,
            "You",
            Enemy,
            fear_factor,
        ).SetName("Fear Factor")
        .SetLabel('thwart')
        .SetTarget(Scheme2, range=(1, 1))
        .LimitOncePerPhase(),
    ]
