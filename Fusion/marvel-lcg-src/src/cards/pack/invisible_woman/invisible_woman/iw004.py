from . import *


def GetAbilities() -> Sequence['Ability']:

    def gain_thwart(effect: 'Effect', message: 'Message.AfterUnitChangeForm') -> None:
        effect.GetInitiator().GetIdentity().GainUntilTurnEnd(effect, thwart=1)

    def gain_attack(effect: 'Effect', message: 'Message.AfterUnitChangeForm') -> None:
        effect.GetInitiator().GetIdentity().GainUntilTurnEnd(effect, attack=1)

    return [
        *AbilityFactory.GiveKeywordToAttached("You", defense=1),
        AbilityFactory.AfterUnitChangeForm(
            AbilityType.HeroResponse,
            "You",
            gain_thwart,
            to_form=CardFinder2("INVISIBLE", Hero),
        ).SetName("Unstable Uniform"),
        AbilityFactory.AfterUnitChangeForm(
            AbilityType.HeroResponse,
            "You",
            gain_attack,
            to_form=CardFinder2("PSIONIC", Hero),
        ).SetName("Unstable Uniform"),
    ]
