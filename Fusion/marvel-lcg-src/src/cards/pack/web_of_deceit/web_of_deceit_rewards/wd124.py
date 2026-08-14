from . import *

# Wallcrawl

def GetAbilities() -> Sequence['Ability']:

    def grimper(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        # « Hero Action (thwart): Remove 3 threat from a scheme. If this removes
        # the last threat from that scheme, draw 2 cards. »
        this = effect.this.CastTo(Event)
        joueur = effect.GetInitiator()
        this.RemoveThreatFromSchemes(effect.targets, 3, effect)
        for cible in effect.targets:
            if Scheme2.IsType(cible) and cible.threat <= 0:
                joueur.DrawUp(2, effect)
                break

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            grimper
        ).SetPlay().SetLabel('thwart')
        .SetTarget(Scheme2),
    ]
