from . import *

# mp156 : carte du modulaire du scenario Mephisto, texte IDENTIQUE a la carte officielle du core `01188` (`cards/pack/core/.../01188.py`) : meme script, recopie ici parce que
# la carte vit dans un autre pack. Voir le texte imprime dans data/cards.json (pack `mephisto`).


def GetAbilities() -> Sequence['Ability']:

    def caught_off_guard(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Treachery)
        Unused(this)

        player = message.GetToPlayer()
        face = player.DiscardControlCards(effect, upgrade=True, support=True)
        if face == None:
            ThisCardGainSurge(effect)


    return [
        AbilityFactory.WhenThisRevealed(
            None,
            caught_off_guard
        )
    ]
