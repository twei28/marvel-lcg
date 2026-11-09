from . import *

# mp162 : carte du modulaire du scenario Mephisto, texte IDENTIQUE a la carte officielle du core `01192` (`cards/pack/core/.../01192.py`) : meme script, recopie ici parce que
# la carte vit dans un autre pack. Voir le texte imprime dans data/cards.json (pack `mephisto`).


def GetAbilities() -> Sequence['Ability']:

    def masterplan(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Treachery)
        Unused(this)

        had_placed = False
        for scheme in Worlds.GetSideSchemes(effect):
            this.PlaceThreatOnSchemes([scheme], 4, effect)
            had_placed = True
        if not had_placed:
            face = Worlds.DiscardEncounterCardsUntil(
                effect,
                card_type=SchemeSide2
            )
            if face:
                face.Reveal(message.to_player, effect)

    return [
        AbilityFactory.WhenThisRevealed(
            None,
            masterplan
        )
    ]
