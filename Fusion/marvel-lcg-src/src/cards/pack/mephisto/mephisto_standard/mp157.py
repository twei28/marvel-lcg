from . import *

# mp157 : carte du modulaire du scenario Mephisto, texte IDENTIQUE a la carte officielle du core `01189` (`cards/pack/core/.../01189.py`) : meme script, recopie ici parce que
# la carte vit dans un autre pack. Voir le texte imprime dans data/cards.json (pack `mephisto`).


def GetAbilities() -> Sequence['Ability']:

    def gang_up_hero(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Treachery)
        Unused(this)

        player = message.GetToPlayer()
        Worlds.Enemies.VillainAndEngagedMinionsAttackYou(effect, player)

    return [
        AbilityFactory.WhenThisRevealed(
            "Alter-Ego",
            ThisCardGainSurge
        ),
        AbilityFactory.WhenThisRevealed(
            "Hero",
            gang_up_hero
        ),
    ]
