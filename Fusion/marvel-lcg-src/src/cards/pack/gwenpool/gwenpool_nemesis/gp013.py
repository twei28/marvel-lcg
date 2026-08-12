from . import *

# Break Reality — custom « ekAugust » (traîtrise némésis de Gwenpool)
# Incite 1 (desc).
# When Revealed: Search the encounter deck for Evil Gwenpool and reveal her.
# (Shuffle.) If Unbelievable Gwenpool is in play, she gains quickstrike. If
# Evil Gwenpool was already in play, add 2[per_hero] threat to Rules of the
# Universe.

def GetAbilities() -> Sequence['Ability']:

    def break_reality(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Treachery)

        player = message.GetToPlayer()

        deja_en_jeu = Worlds.FindCardOnField(effect, name="Evil Gwenpool", card_type=Minion)

        if deja_en_jeu:
            rules = Worlds.FindCardOnField(effect, name="Rules of the Universe")
            if rules:
                this.PlaceThreatOnSchemes([rules], "2*", effect)
        else:
            Find.FindAndReveal(
                effect,
                player,
                name="Evil Gwenpool",
                card_type=Minion,
            )

        evil = Worlds.FindCardOnField(effect, name="Evil Gwenpool", card_type=Minion)
        if evil and Worlds.FindCardOnField(effect, name="Unbelievable Gwenpool", card_type=Upgrade):
            evil.GainKeyword(1, 'Quickstrike', effect)

    return [
        AbilityFactory.WhenThisRevealed(
            None,
            break_reality
        ),
    ]
