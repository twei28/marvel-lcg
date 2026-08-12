from . import *

# * Baxter Building — custom « DesignHacker »
# Alter-Ego Action: Exhaust Baxter Building -> heal 2 damage from an identity.
# Hero Action: Exhaust Baxter Building -> search the top 4 cards of your deck
# for a Mister Fantastic card, then add it to your hand (top 8 instead if your
# hero has 10 or more hit points remaining).

def GetAbilities() -> Sequence['Ability']:

    def soigner(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Support)
        this.HealthUnits(effect.targets, 2, effect)

    def chercher(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Support)
        Unused(this)

        initiator = effect.GetInitiator()
        hero = initiator.GetHero()
        profondeur = 8 if hero.GetRemainingHealth() >= 10 else 4

        face = Search.PlayerDeckTop(
            effect,
            initiator,
            profondeur,
            set_name="Mister Fantastic",
        )
        if face:
            initiator.GainCard(face, effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.AlterEgoAction,
            soigner
        ).SetCostFunc(CostFunc.Exhaust("This"))
        .SetTarget(Identity, canbe_heal=True),

        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            chercher
        ).SetCostFunc(CostFunc.Exhaust("This")),
    ]
