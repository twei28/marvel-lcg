from cards.pack.shadowland import *


def PositionsDifferentes(effect: 'Effect') -> bool:
    """« If the positions are different » : les DEUX cartes sont en jeu et ne montrent pas la meme position."""
    return PositionDuVilain(effect) is not None and PositionDuHeros(effect) is not None and not PositionsIdentiques(effect)


def AbilitesPositionVilain() -> Sequence['Ability']:
    """Effets continus imprimes IDENTIQUEMENT sur les deux faces de sl003 (VILLAIN POSITION)."""

    def degats_moins_un(effect: 'Effect', message: 'Message.WhenUnitWouldTakeDamage') -> bool:
        return PositionsDifferentes(effect)

    def menace_non_retirable(effect: 'Effect', message: 'Message.WhenSchemeWouldRemoveThreat') -> bool:
        return PositionsDifferentes(effect)

    return [
        *AbilityFactory.GiveKeywordToInPlayWhenApplyThis("Character", attack=1, condition=PositionsIdentiques),
        AbilityFactory.ReduceCharacterTakeDamageBy("Character", 1, from_each_attack=True, conditions=[degats_moins_un]),
        AbilityFactory.ThreatCannotBeRemovedFromWhile(MainScheme, conditions=[menace_non_retirable]),
    ]
