from . import *

# Rock 'Em — custom « DesignHacker »
# Hero Action (thwart): Remove 4 threat from a scheme. If this removes the
# last threat on that scheme, give The Thing a tough status card or confuse
# the villain.

def GetAbilities() -> Sequence['Ability']:

    def rock_em(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)

        def derniere_menace():
            initiator = effect.GetInitiator()
            hero = initiator.GetHero()
            villain = Worlds.FindVillain(effect)

            initiator.ChooseAbilities(
                effect,
                AbilityFactory.ForChoiceAbility(
                    "Give The Thing a tough status card",
                    lambda targets: Faces.GiveStatus([hero], "Tough", effect),
                    condition=hero is not None,
                ),
                AbilityFactory.ForChoiceAbility(
                    "Confuse the villain",
                    lambda targets: Faces.GiveStatus([villain], "Confused", effect),
                    condition=villain is not None,
                ),
            )

        this.RemoveThreatFromSchemes(
            effect.targets, 4, effect,
            if_this_remove_last_threat=derniere_menace,
        )

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            rock_em
        ).SetPlay().SetLabel('thwart')
        .SetTarget(Scheme2),
    ]
