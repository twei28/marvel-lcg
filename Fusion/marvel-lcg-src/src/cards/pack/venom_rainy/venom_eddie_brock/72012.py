from . import *

# We Hunger — custom « Rainy » (obligation d'Eddie Brock)
# Give to the Eddie Brock player. Flip to hero form. Choose:
# - Take 3 damage -> discard this obligation.
# - Place 3 threat on the main scheme -> heal 1 damage from Venom and discard
#   this obligation.

def GetAbilities() -> Sequence['Ability']:

    def we_hunger(effect: 'Effect', message: 'Message.WhenObligationGiveToPlayer') -> None:
        this = effect.this.CastTo(Obligation)
        player = message.GetGaveToPlayer()
        identity = player.GetIdentity()

        if not player.IsHero():
            identity.ChangeToForm(Hero, effect)

        def degats(targets: Sequence['CardFace']) -> None:
            this.DealDamage([player.GetIdentity()], 3, effect)
            Faces.DiscardAll([this], effect)

        def menace(targets: Sequence['CardFace']) -> None:
            scheme = Worlds.FindMainScheme(this)
            if scheme:
                this.PlaceThreatOnSchemes([scheme], 3, effect)
            this.HealthUnits([player.GetIdentity()], 1, effect)
            Faces.DiscardAll([this], effect)

        player.ChooseAbilities(
            effect,
            AbilityFactory.ForChoiceAbility(
                "Take 3 damage",
                degats,
            ),
            AbilityFactory.ForChoiceAbility(
                "Place 3 threat on the main scheme → heal 1 damage from Venom",
                menace,
            ),
        )

    return [
        AbilityFactory.WhenThisObligationGiveToYou(
            we_hunger
        )
    ]
