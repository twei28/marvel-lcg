from . import *

# Arachno-Telepathy

def GetAbilities() -> Sequence['Ability']:

    def lire_les_fils(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        # « Action (thwart): Exhaust Arachno-Telepathy, and discard 1 card from
        # the encounter deck → remove 1 threat from a scheme for each icon
        # (boost ou etoile) discarded this way. »
        this = effect.this.CastTo(Upgrade)
        defaussees = Worlds.DiscardEncounterCards(1, effect)
        valeur = 0
        for carte in defaussees:
            if HasBoostIcon.IsType(carte):
                valeur += carte.printed_boost + carte.boost_star
        if valeur > 0:
            this.RemoveThreatFromSchemes(effect.targets, valeur, effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.Action,
            lire_les_fils
        ).SetCostFunc(CostFunc.Exhaust("This"))
        .SetLabel('thwart')
        .SetTarget(Scheme2),
    ]
