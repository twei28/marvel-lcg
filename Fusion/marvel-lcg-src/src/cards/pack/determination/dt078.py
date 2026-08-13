from . import *

# Cumbersome Enhancements

def GetAbilities() -> Sequence['Ability']:

    def check_petite_main(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> bool:
        hero = effect.GetInitiator().GetHero()
        return hero.printed_hand_size <= 4

    def debut_phase_mechant(effect: 'Effect', message: 'Message.WhenPhaseBegin') -> None:
        this = effect.this.CastTo(Upgrade)

        player = this.GetControlByPlayer()
        if player is None:
            return
        if player.AskChooseOneText(["Discard", "Acceleration"]) == "Discard":
            Faces.DiscardAll([this], effect)
        else:
            Faces.PlaceTokensOn([this], 1, 'acceleration_token', effect)

    return [
        AbilityFactory.CanPlayThisUpgradeCard(
            conditions=[check_petite_main]
        ),
        *AbilityFactory.GiveKeywordToAttached(
            Hero,
            hand_size=2,
        ),
        AbilityFactory.WhenPhaseBegin(
            AbilityType.ForcedInterrupt,
            "Villain",
            debut_phase_mechant
        ),
    ]
