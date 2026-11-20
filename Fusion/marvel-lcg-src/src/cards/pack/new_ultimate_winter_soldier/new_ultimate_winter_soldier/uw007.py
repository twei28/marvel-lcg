from . import *

# Last Resort — evenement signature, x2. SUPERPOWER. THWART. Cout 1, [mental].
# Hero Action (thwart): Discard 1 card from your hand at random -> remove 1 threat from a scheme. Remove X additional
# threat from that scheme, where X is equal to the numeral in the printed resource cost of that card. If this removes the
# last threat from that scheme, draw 2 cards.
#
# Carte de reference : `35011` Track by Scent (Wolverine officiel) : « Remove 3 threat from a scheme. If this removes the
# last threat from that scheme, draw 2 cards » = `RemoveThreatFromSchemes(cibles, n, effect,
# if_this_remove_last_threat=...)`. Ici n = 1 + X, sur UN SEUL complot (« THAT scheme »).


def GetAbilities() -> Sequence['Ability']:

    def last_resort(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        initiator = effect.GetInitiator()

        def piocher() -> None:
            initiator.DrawUp(2, effect)

        this.RemoveThreatFromSchemes(
            effect.targets,
            1 + XDeLaCarteDefaussee(effect),
            effect,
            if_this_remove_last_threat=piocher,
        )

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            last_resort,
            conditions=[UneCarteADefausser],
        ).SetPlay().SetLabel('thwart')
        .SetCostFunc(CoutDefausseAuHasard())
        .SetTarget(Scheme2),
    ]
