from . import *

# * Mutanimal Van — SOUTIEN 1 [mental], aspect Basic (TMNT Reskins). MUTANIMAL. NYC. VEHICLE.
# Play only if your identity has the [[MUTANIMAL]] trait.
# Hero Action: Exhaust Mutanimal Van and deal 1 facedown encounter card to a player → that player draws 2 cards.
#
# MODIFIEE de 41022 IPAC : X-FORCE -> MUTANIMAL. Script copie de 41022.


def GetAbilities() -> Sequence['Ability']:

    def mutanimal_van(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Support)
        Unused(this)

        for player in effect.cost_func.Get(CostFunc.DealPlayerEncounterCard).return_players:
            player.DrawUp(2, effect)

    return [
        AbilityFactory.CanPlayThisSupportCard(
        ).SetPlay(only_if_your_identity_has_trait="MUTANIMAL"),
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            mutanimal_van
        ).SetCostFunc(CostFunc.Exhaust("This"))
        .SetCostFunc(CostFunc.DealPlayerEncounterCard(1, "AnyPlayer")),
    ]
