from . import *

# * Scarlet Witch (Wanda Maximoff) — alliee signature. AVENGER. MYSTIC.
# Cout 3 / PV 2 / THW 2* / ATK 1*
# You may play the event attached to Scarlet Witch as if it were in your
#   hand, reducing its cost by 1.
# Response: After Scarlet Witch enters play, choose a SPELL event in your
#   discard pile and attach it to her facedown.
#
# Carte de reference : dz014 * Lightbringr (RECETTES), quasi jumelle —
# `YouMayPlayCardLikeInHand(from_where="ThisPlacedCard")` + reduction via
# `WhenCalculateEffectCost` limitee aux cartes jouees DEPUIS sa zone +
# `PlaceCardHere(..., False, ...)` (face cachee). Difference : Lightbringr
# charge sa reserve par une action repetable depuis la MAIN, Wanda se charge
# UNE fois a l'arrivee depuis la DEFAUSSE (01083 Mockingbird pour le
# declencheur `AfterCardEnterPlay`).

def GetAbilities() -> Sequence['Ability']:

    def sous_wanda(effect: 'Effect', face: 'CardFace') -> bool:
        zone = effect.this.GetPlacedCardArea()
        return zone is not None and face is not None and face.card.area == zone

    def reduction(effect: 'Effect',
                  message: 'Message.WhenCalculateEffectCost') -> None:
        message.UpdateCost(-1, effect)

    def charger(effect: 'Effect', message: 'Message2') -> None:
        this = effect.this.CastTo(Ally)

        cibles = [t for t in effect.targets if t is not None]
        if cibles:
            this.PlaceCardHere(cibles, False, effect)

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
                    sous_wanda(effect, message.check_effect.this),
            ],
        ).NoOutOfPlayLimit(),
        AbilityFactory.AfterCardEnterPlay(
            AbilityType.Response,
            "This",
            charger
        ).SetTarget(CardFinder2("SPELL", Event), range=(1, 1),
                    from_where=["YourDiscardPile"]),
    ]
