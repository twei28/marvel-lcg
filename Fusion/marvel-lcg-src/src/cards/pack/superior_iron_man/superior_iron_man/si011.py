from . import *

# Spectacular Blast
#
# Double cible (attaque + retrait de menace) sur la meme carte : modele
# Giant Stomp (ant/ant_man/12003.py), `.SetTarget(...).SetTarget2(...)`,
# `effect.targets` / `effect.targets2`.

def GetAbilities() -> Sequence['Ability']:

    def spectacular_blast(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        this.DealDamage(effect.targets, 3, effect)
        this.RemoveThreatFromSchemes(effect.targets2, 2, effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            spectacular_blast,
        ).SetPlay().SetLabel('attack', 'thwart')
        .SetTarget(Enemy)
        .SetTarget2(Scheme2, has_threat=True),
    ]
