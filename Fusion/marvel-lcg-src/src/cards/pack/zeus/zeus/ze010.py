from . import *

# * Hephaestus (soutien, cout 1, OLYMPUS PERSONA, mental)
# Alter-Ego Action: Exhaust Hephaestus → shuffle 1 copy of Thunder Strike from
# your discard pile into your deck. Draw 1 card.
#
# Modele : 09008 Sanctum Sanctorum, mot pour mot (cible dans la defausse,
# `ShuffleAllTo` vers le deck, puis pioche). `.SetHasNoTargetEffect()` comme
# le modele : sans Thunder Strike dans la defausse, l'action reste jouable et
# ne fait que piocher, « on fait ce qu'on peut » (regle generale des effets).

def GetAbilities() -> Sequence['Ability']:

    def hephaestus(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Support)
        Unused(this)
        initiator = effect.GetInitiator()
        if effect.targets:
            Faces.ShuffleAllTo(effect.targets, initiator.player_deck, effect)
        initiator.DrawUp(1, effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.AlterEgoAction,
            hephaestus,
        ).SetCostFunc(CostFunc.Exhaust("This"))
        .SetTarget(name=THUNDER_STRIKE, card_type=Event, from_where=["YourDiscardPile"])
        .SetHasNoTargetEffect(),
    ]
