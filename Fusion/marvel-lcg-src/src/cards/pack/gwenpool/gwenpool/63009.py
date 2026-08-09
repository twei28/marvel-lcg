from . import *

# * Unbelievable Gwenpool — custom « ekAugust »
# Alter-Ego Action: Exhaust Unbelievable Gwenpool -> search your deck for a
# Gwenpool card and attach it faceup here (to a maximum of 1). (Shuffle.)
# You may use the speech bubbles of the attached card.
# Hero Action: Draw 2 cards and ____. Discard Unbelievable Gwenpool.
# Bulle : « Ready Gwenpool. »

def GetAbilities() -> Sequence['Ability']:

    def attacher(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Upgrade)

        # La carte cherchee est posee ici, pas attachee : une carte Gwenpool est le
        # plus souvent un Event, qui n'a pas le mixin CanAttach. C'est donc
        # GetPlacedCardArea (PlaceCardHere) et non GetInventoryDeck (AttachTo2).
        if this.GetPlacedCardArea().FindCards():
            return  # maximum de 1 carte attachée

        initiator = effect.GetInitiator()
        face = Search.PlayerCard(
            effect,
            initiator,
            include_player_deck=True,
            set_name="Gwenpool",
        )
        if face:
            this.PlaceCardHere(face, True, effect)

    def draw_2_and_blank(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Upgrade)

        initiator = effect.GetInitiator()
        initiator.DrawUp(2, effect)
        ResolveBlank(effect)
        Faces.DiscardAll([this], effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.AlterEgoAction,
            attacher
        ).SetCostFunc(CostFunc.Exhaust("This")),

        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            draw_2_and_blank
        ),
    ]
