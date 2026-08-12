from . import *

# "Future Me Scares Me" — custom « ekAugust » (traîtrise némésis de Gwenpool)
# Incite 0 (1 en multijoueur) / Incite 1 (2 en expert).
# LENIENT : le moteur ne porte qu'une valeur d'Incite -> desc "1".
# When Revealed: If Evil Gwenpool is in play, add 2 threat to Rules of the
# Universe and shuffle this card into the encounter deck.

def GetAbilities() -> Sequence['Ability']:

    def future_me_scares_me(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Treachery)

        evil = Worlds.FindCardOnField(effect, name="Evil Gwenpool", card_type=Minion)
        if not evil:
            return

        rules = Worlds.FindCardOnField(effect, name="Rules of the Universe")
        if rules:
            this.PlaceThreatOnSchemes([rules], 2, effect)
        Faces.ShuffleAllTo([this], "EncounterDeck", effect)

    return [
        AbilityFactory.WhenThisRevealed(
            None,
            future_me_scares_me
        ),
    ]
