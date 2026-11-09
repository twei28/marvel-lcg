from . import *

# mp161 : carte du modulaire du scenario Mephisto, texte IDENTIQUE a la carte officielle du core `01191` (`cards/pack/core/.../01191.py`) : meme script, recopie ici parce que
# la carte vit dans un autre pack. Voir le texte imprime dans data/cards.json (pack `mephisto`).


def GetAbilities() -> Sequence['Ability']:

    def exhaustion(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Treachery)
        Unused(this)

        player = message.GetToPlayer()
        identity = player.GetIdentity()
        Faces.ExhaustAll([identity], effect)

    return [
        AbilityFactory.WhenThisRevealed(
            None,
            exhaustion
        )
    ]
