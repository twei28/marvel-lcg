from . import *

# * Lightbringr
# PERSONA.
# Events attached to Lightbringr may be played as if they were in your hand.
#   Reduce the resource cost of cards played this way by 1.
# Alter-Ego Action: Exhaust Lightbringr -> attach 1 SONG event from your hand
#   facedown here (to a maximum of 3).
#
# Squelette de Resource Reserve (53021, Falcon), qui fait exactement la
# premiere moitie : `YouMayPlayCardLikeInHand(from_where="ThisPlacedCard")`
# plus une action qui glisse des cartes dessous.
#
# La reduction de cout n'a pas de fabrique dediee pour les cartes D'AUTRUI : on
# passe par le crochet generique `WhenCalculateEffectCost` et on ne l'applique
# qu'aux cartes qui se jouent DEPUIS la zone de Lightbringr, ce qui est le sens
# exact de « played this way ».
#
# FACE CACHEE ici (`False`), contrairement a la Setlist de Live Concert : le
# texte dit « facedown ».


MAX_ATTACHEES = 3


def GetAbilities() -> Sequence['Ability']:

    def sous_lightbringr(effect: 'Effect', face: 'CardFace') -> bool:
        zone = effect.this.GetPlacedCardArea()
        return zone is not None and face is not None and face.card.area == zone

    def reduction(effect: 'Effect',
                  message: 'Message.WhenCalculateEffectCost') -> None:
        message.UpdateCost(-1, effect)

    def ranger(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Support)
        this.PlaceCardHere(effect.targets, False, effect)

    return [
        *AbilityFactory.YouMayPlayCardLikeInHand(
            AbilityType.NonKeyword,
            Event,
            from_where="ThisPlacedCard",
        ),
        AbilityFactory.WhenCalculateEffectCost(
            AbilityType.NonKeyword,
            reduction,
            conditions=[
                lambda effect, message:
                    message.is_play and
                    message.check_effect is not None and
                    sous_lightbringr(effect, message.check_effect.this),
            ],
        ).NoOutOfPlayLimit(),
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.AlterEgoAction,
            ranger,
            conditions=[
                lambda effect, message:
                    effect.this.GetPlacedCardArea().GetSize() < MAX_ATTACHEES,
            ],
        ).SetCostFunc(CostFunc.Exhaust("This"))
        .SetTarget("YourHandCards", card_type=Event, trait=TRAIT_SONG),
    ]
