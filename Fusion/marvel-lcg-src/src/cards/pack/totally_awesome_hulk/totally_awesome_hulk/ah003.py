from . import *

# * Maddy Cho — custom « DesignHacker »
# Totally Awesome Hulk gets +1 hand size.
# Hero Action: Exhaust Maddy Cho → add or remove 1 rage counter from "The Trunk".


def GetAbilities() -> Sequence['Ability']:

    def maddy_cho(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Support)
        initiator = effect.GetInitiator()

        trunk = FindTrunk(effect, initiator)
        if not trunk:
            return

        def ajouter(targets: Sequence['CardFace']) -> None:
            Faces.PlaceCountersOn(trunk, 1, 'rage', effect)

        def retirer(targets: Sequence['CardFace']) -> None:
            Faces.RemoveCountersOn(trunk, 1, 'rage', effect)

        choix: List['Ability'] = [
            AbilityFactory.ForChoiceAbility(
                "Add 1 rage counter",
                ajouter,
            ),
        ]
        if Faces.GetTotalCounters(trunk, 'rage') > 0:
            choix.append(
                AbilityFactory.ForChoiceAbility(
                    "Remove 1 rage counter",
                    retirer,
                )
            )

        Unused(this)
        initiator.ChooseAbilities(effect, *choix)

    return [
        *AbilityFactory.GiveKeywordToInPlayWhenApplyThis(
            CardFinder(name="Totally Awesome Hulk"),
            control_by="You",
            hand_size=1,
        ),
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            maddy_cho,
        ).SetCostFunc(CostFunc.Exhaust("This")),
    ]
