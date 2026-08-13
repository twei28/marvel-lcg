from . import *

# Heroic Combat Vest

def GetAbilities() -> Sequence['Ability']:

    def heroic_combat_vest(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(this)

        initiator = effect.GetInitiator()
        hero = initiator.GetHero()

        text = initiator.AskChooseOneText(["THW", "ATK", "DEF"])
        if text == 'THW':
            hero.GainUntilRoundEnd(effect, thwart=1)
        if text == 'ATK':
            hero.GainUntilRoundEnd(effect, attack=1)
        if text == 'DEF':
            hero.GainUntilRoundEnd(effect, defense=1)

    return [
        AbilityFactory.CanPlayThisUpgradeCard(
            "Players"
        ),
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            heroic_combat_vest
        ).LimitOncePerRound()
        .SetCostFunc(CostFunc.TakeDamage(1, "Initiator")),
    ]
