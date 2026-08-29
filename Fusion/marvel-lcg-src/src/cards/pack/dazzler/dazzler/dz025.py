from . import *

# Song of Justice
# SONG. THWART.
# Max 2 per deck.
# Hero Action (thwart): Remove 1 threat from a scheme for each SONG card in
#   your discard pile (to a maximum of 4).


def GetAbilities() -> Sequence['Ability']:

    def chant_de_justice(effect: 'Effect',
                         message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        valeur = SongsDansLaDefausseBornee(effect)
        if valeur > 0:
            this.RemoveThreatFromSchemes(effect.targets, valeur, effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            chant_de_justice,
        ).SetPlay().SetLabel("thwart")
        .SetTarget(Scheme2),
    ]
