from . import *

# Sensing Trouble

def GetAbilities() -> Sequence['Ability']:

    def flair(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        # « Hero Action (thwart): Ready your identity → remove 3 threat from a
        # scheme. »
        this = effect.this.CastTo(Event)
        joueur = effect.GetInitiator()
        Faces.ReadyAll([joueur.GetIdentity()], effect)
        this.RemoveThreatFromSchemes(effect.targets, 3, effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            flair
        ).SetPlay().SetLabel('thwart')
        .SetTarget(Scheme2),
    ]
