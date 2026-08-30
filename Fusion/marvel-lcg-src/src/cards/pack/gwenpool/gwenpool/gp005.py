from . import *

# "Sorry, Gotta Run!" — custom « ekAugust »
# Hero Action (thwart): Remove 2 threat from a scheme. This thwart ignores
# the patrol keyword and crisis icons. If this thwart defeats a scheme, ____.
# Bulle : « Remove 2 threat from the main scheme. »
# CORRECTIF (30/08/2026) : « ignores the patrol keyword » n'était pas câblé, au
# motif que « le ciblage du moteur ne propose pas d'exemption patrol ». C'est
# faux : `Ability.SetIgnoreKeyword` existe, et `scheme_main.py`
# `RemoveThreatInternal` interroge `by_effect.IsIgnoreKeyword('Patrol')` juste
# après la crise. Patrol protège le COMPLOT PRINCIPAL : sans l'exemption, un
# seul sbire patrol engagé rendait la carte inopérante là où elle promet le
# contraire. Les deux exemptions passent maintenant par le même mécanisme, comme
# 42006 Natural Flight (officielle) et 61023 Grapnel Launcher, qui portent la
# MÊME phrase imprimée.
# LENIENT : « defeats a scheme » reste approximé par « retire la dernière menace ».

def GetAbilities() -> Sequence['Ability']:

    def sorry_gotta_run(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)

        def last_threat():
            ResolveBlank(effect)

        this.RemoveThreatFromSchemes(
            effect.targets, 2, effect,
            if_this_remove_last_threat=last_threat,
        )

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            sorry_gotta_run
        ).SetPlay().SetLabel('thwart')
        .SetTarget(Scheme2)
        .SetIgnoreKeyword('Crisis', 'Patrol'),
    ]
