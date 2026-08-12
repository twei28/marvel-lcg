from . import *

# Fly-By — custom « DesignHacker »
# Hero Action (thwart): Remove 2 threat from a scheme, then remove 1 threat
# from a scheme for each flame counter on the villain.
#
# LENIENT : le texte autorise deux manigances différentes ; ici tout est
# retiré de la manigance choisie.

def GetAbilities() -> Sequence['Ability']:

    def fly_by(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)

        valeur = 2
        villain = Worlds.FindVillain(effect)
        if villain:
            valeur += villain.GetCounters('flame')

        this.RemoveThreatFromSchemes(effect.targets, valeur, effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            fly_by
        ).SetPlay().SetLabel('thwart')
        .SetTarget(Scheme2),
    ]
