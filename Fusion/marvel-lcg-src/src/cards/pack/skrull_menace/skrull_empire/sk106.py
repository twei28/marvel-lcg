from . import *

# Wrath of the Empire — TRAITRISE x3 (Skrull Empire). ★.
# When Revealed: Discard the top 2 cards of the encounter deck for each PLANET
#   environment in play. Place 1 acceleration token on the main scheme, if a
#   card with the acceleration icon was discarded this way.
# ★ Boost: This card gets +1 boost icon for each PLANET environment in play.
#
# Cartes de reference : **`46028`** Burn (`message.GainBoostIcon(n, effect)`) ;
# `PlaceAccelerationToken(1, effect)` (can_acceleration_token.py).
# ⚠ « 2 cards FOR EACH planet » ; « 1 acceleration token » (UN seul, meme si
# plusieurs icones) ; icone lue sur les cartes defaussees (`acceleration_icon`).


def GetAbilities() -> Sequence['Ability']:

    def colere(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        Unused(message)
        n = 2 * len(PlanetesEnJeu(effect))
        if n <= 0:
            return
        defaussees = Worlds.DiscardEncounterCards(n, effect)
        if any(getattr(f, "acceleration_icon", 0) for f in defaussees):
            complot = Worlds.FindMainScheme(effect)
            if complot is not None:
                complot.PlaceAccelerationToken(1, effect)

    def boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        n = len(PlanetesEnJeu(effect))
        if n:
            message.GainBoostIcon(n, effect)

    return [
        AbilityFactory.WhenThisRevealed(None, colere),
        AbilityFactory.WhenCardBecomeBoost("This", boost),
    ]
