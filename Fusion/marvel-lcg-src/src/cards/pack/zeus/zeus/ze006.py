from . import *

# Wrath of Olympus (evenement, cout 5, ATTACK SUPERPOWER, energie)
# Requirement ([energy][energy][energy]).
# Hero Action (attack): Deal 10 damage to an enemy. This attack gains overkill.
# Special: Deal 2 damage to each enemy in play. Remove 2 threat from each
# scheme.
#
# Modeles : 35023 (`AttackProperty(overkill=True)`), `RemoveThreatFromSchemes
# ("EachScheme", ...)` (card_face.py:790). « each enemy in play » : tous les
# ennemis sur la table, vilain compris, quel que soit le joueur engage.

def GetAbilities() -> Sequence['Ability']:

    def wrath_of_olympus(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        this.DealDamage(effect.targets, 10, effect, property=AttackProperty(overkill=True))

    def special(effect: 'Effect', message: 'Message.WhenResolveSpecialAbility') -> None:
        this = effect.this.CastTo(Event)
        ennemis = Worlds.FindCardsOnField(effect, card_type=Enemy)
        if ennemis:
            this.DealDamage(ennemis, 2, effect)
        this.RemoveThreatFromSchemes("EachScheme", 2, effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            wrath_of_olympus,
        ).SetPlay().SetLabel('attack')
        .SetTarget(Enemy),

        # ⚠ `.NoOutOfPlayLimit()` : ce Special se resout depuis la MAIN (Hera)
        # ou pendant le paiement (Tempest), jamais depuis la table. Sans ce
        # drapeau, le moteur ignore l'effet d'une carte hors jeu et le message
        # `WhenResolveSpecialAbility` tombe dans le vide (vu le 11/09/2026).
        AbilityFactory.WhenResolveSpecialAbility(
            "This",
            special,
        ).NoOutOfPlayLimit(),
    ]
