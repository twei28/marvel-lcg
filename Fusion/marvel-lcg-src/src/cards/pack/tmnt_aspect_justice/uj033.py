from . import *

# * Tomoe Ame — ALLIE 3 [energy], aspect Justice (TMNT Aspects, Inkwire). CAT. ONNA-MUSHA.
# PV 3, THW 2 (1 degat consecutif), ATK 3 (2 degats consecutifs).
# Response: After Tomoe Ame defeats a side scheme or minion, draw 1 card.
#
# CARTES DE REFERENCE
#  - `sk029` Glorious Flight / `52001a` Silk : « After <X> defeat a minion or side scheme » =
#    `AfterUnitDefeatedUnit(type, <qui>, Minion, op)` + `AfterUnitDefeatedScheme(type, <qui>, SchemeSide2, op)`.
#  - `04047` / `04049` : « draw 1 card » = `joueur.DrawUp(1, effect)`.
#
# TEXTE CONTRE CODE (PROCESSUS-CARTE etape 5)
#  ⚠ « After TOMOE AME defeats » : elle seule (pas « you ») ; par n'importe quel moyen (attaque, contre).
#  ⚠ « a SIDE scheme OR MINION » : manigance ANNEXE (pas la principale), SBIRE (pas le vilain).
#  ⚠ « draw 1 card » : le joueur qui la controle.
#  Aucune limite imprimee.


def GetAbilities() -> Sequence['Ability']:

    def piocher(effect: 'Effect', message: 'Message2') -> None:
        this = effect.this.CastTo(Ally)
        Unused(message)
        joueur = this.GetControlByPlayer() or effect.GetInitiator()
        joueur.DrawUp(1, effect)

    return [
        AbilityFactory.AfterUnitDefeatedUnit(
            AbilityType.Response,
            "This",
            Minion,
            piocher,
        ),
        AbilityFactory.AfterUnitDefeatedScheme(
            AbilityType.Response,
            "This",
            SchemeSide2,
            piocher,
        ),
    ]
