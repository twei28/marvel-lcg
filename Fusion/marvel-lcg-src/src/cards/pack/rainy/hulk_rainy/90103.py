from . import *

# * Black Widow

def GetAbilities() -> Sequence['Ability']:

    def apres_thwart(effect: 'Effect', message: 'Message.AfterUnitThwartEnd') -> None:
        this = effect.this.CastTo(Ally)

        this.RemoveThreatFromSchemes(effect.targets, 1, effect)

    def retour_alter_ego(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Ally)
        Unused(this)

        effect.targets[0].CastTo(Identity).ChangeToForm(AlterEgo, effect)

    return [
        AbilityFactory.CanPlayThisAllyCard(),
        # « remove 1 threat from ANOTHER scheme » : on exclut celui qu'on vient
        # de contrecarrer, comme le fait 50105b.
        AbilityFactory.AfterUnitThwartEnd(
            AbilityType.Response,
            "This",
            apres_thwart
        ).SetTarget(Scheme2, exclude="Targets"),
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            retour_alter_ego
        ).SetCostFunc(CostFunc.Exhaust("This"))
        .SetTarget("YourIdentity"),
    ]
