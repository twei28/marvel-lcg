from . import *

# "Out and Proud"
# SONG.
# Hero Action: Defeat a non-ELITE minion.
# Showtime!: Heal 1 damage from each ally in play.
#
# Le « defeat » suit Lady Deadpool (44016), meme clause au mot pres :
# `SetTarget(Minion, non_trait="ELITE")` puis `Faces.DefeatUnits`.


def GetAbilities() -> Sequence['Ability']:

    def fiere(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Faces.DefeatUnits(effect.targets, this, effect)

    def showtime(effect: 'Effect', message: 'Message2') -> None:
        this = effect.this.CastTo(Event)
        # « EACH ally in play », allies de tout le monde, pas seulement les tiens.
        allies = Worlds.FindCardsOnField(effect, card_type=Ally)
        if allies:
            this.HealthUnits(list(allies), 1, effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            fiere,
        ).SetPlay().SetLabel()
        .SetTarget(Minion, non_trait="ELITE"),
        Showtime(showtime),
    ]
