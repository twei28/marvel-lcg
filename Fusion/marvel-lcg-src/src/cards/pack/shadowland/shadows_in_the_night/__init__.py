from cards.pack.shadowland import *
from cards.pack.fne import PeutCouvrirLeCout


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


def ActionPositionHeros(branches: Callable[['Effect', 'Player', Callable[[], None]], Sequence['Ability']]) -> 'Ability':
    """« First Player Action : Resolve one of the effects below, then flip this card » (sl004a/b).
    `branches(effect, joueur, retourner)` rend les trois choix ; chacun appelle `retourner()` une fois SON effet resolu.
    Modeles : gmw/16143 (First Player Action d'un environnement), fne/60127 (choix payants)."""

    def action(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Environment)
        joueur = message.GetToPlayer()

        def retourner() -> None:
            this.card.Flip(effect)

        joueur.ChooseAbilities(effect, *branches(effect, joueur, retourner))

    return AbilityFactory.WhenInYourPlayTurn(AbilityType.FirstPlayerAction, action)
