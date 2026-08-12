from . import *

# "Sorry, Gotta Run!" — custom « ekAugust »
# Hero Action (thwart): Remove 2 threat from a scheme. This thwart ignores
# the patrol keyword and crisis icons. If this thwart defeats a scheme, ____.
# Bulle : « Remove 2 threat from the main scheme. »
# LENIENT : « ignores the patrol keyword » non câblé (le ciblage du moteur ne
# propose pas d'exemption patrol) ; « defeats a scheme » approximé par « retire
# la dernière menace ».

def GetAbilities() -> Sequence['Ability']:

    def sorry_gotta_run(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)

        def last_threat():
            ResolveBlank(effect)

        this.RemoveThreatFromSchemes(
            effect.targets, 2, effect,
            if_this_remove_last_threat=last_threat,
            ignore_crisis=True,
        )

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            sorry_gotta_run
        ).SetPlay().SetLabel('thwart')
        .SetTarget(Scheme2),
    ]
