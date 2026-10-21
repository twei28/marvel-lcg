from . import *

# Wrath of the Hobgoblin — TRAITRISE x2. Boost ★+1.
# When Revealed : Hobgoblin activates against you with +1 SCH and +1 ATK for each acceleration token on the main
#   scheme.
# ★ Boost : Discard 2 cards from the encounter deck.
#
# Cartes de reference : jigsaw/pu066.py (`villain.DoActivate(joueur, effect, op)` + `GainForThisActive(effect,
# would_message, ...)`), brawn/brawn_nemesis/bw020.py (`acceleration_token`), `Worlds.DiscardEncounterCards`.
#
# ⚠ « for EACH acceleration token » : N jetons = +N SCH et +N ATQ ; « on THE main scheme » : le complot principal en jeu
# (somme si plusieurs) ; le bonus ne vaut que pour CETTE activation.

def GetAbilities() -> Sequence['Ability']:

    def revele(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        joueur = message.GetToPlayer()
        hob = TrouverHobgoblin(effect)
        if hob is None or joueur is None:
            return
        n = sum(getattr(s, 'acceleration_token', 0) for s in Worlds.GetMainSchemes(effect))

        def bonus(activation: 'Message.WhenEnemyActivateAgainstYou') -> None:
            if n > 0:
                hob.GainForThisActive(effect, activation.would_message, attack=n, scheme=n)

        hob.DoActivate(joueur, effect, bonus)

    def boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        Worlds.DiscardEncounterCards(2, effect)

    return [
        AbilityFactory.WhenThisRevealed(None, revele),
        AbilityFactory.WhenCardBecomeBoost("This", boost),
    ]
