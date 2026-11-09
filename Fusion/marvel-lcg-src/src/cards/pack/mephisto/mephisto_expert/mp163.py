from . import *

# mp163 : carte du modulaire du scenario Mephisto, texte IDENTIQUE a la carte officielle du core `01193` (`cards/pack/core/.../01193.py`) : meme script, recopie ici parce que
# la carte vit dans un autre pack. Voir le texte imprime dans data/cards.json (pack `mephisto`).


def GetAbilities() -> Sequence['Ability']:

    def under_fire(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Treachery)
        Unused(this)

        player = message.GetToPlayer()
        Worlds.RevealEncounterDeckTopCard(player, effect)

    return [
        AbilityFactory.WhenThisRevealed(
            None,
            under_fire
        )
    ]
