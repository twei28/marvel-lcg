from . import *

# mp152 : carte du modulaire du scenario Mephisto, texte IDENTIQUE a la carte officielle du core `01186` (`cards/pack/core/.../01186.py`) : meme script, recopie ici parce que
# la carte vit dans un autre pack. Voir le texte imprime dans data/cards.json (pack `mephisto`).


def GetAbilities() -> Sequence['Ability']:

    def advance(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Treachery)
        Unused(this)

        player = message.GetToPlayer()
        villain = Worlds.FindVillain(effect)
        if villain:
            villain.DoSchemes(player, effect)

    return [
        AbilityFactory.WhenThisRevealed(
            None,
            advance
        )
    ]
