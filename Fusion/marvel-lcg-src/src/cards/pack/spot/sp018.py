from . import *

# Oddballs

def GetAbilities() -> Sequence['Ability']:

    def revelee(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Treachery)
        Unused(this)
        player = message.GetToPlayer()

        # « Place 1 threat on each Spot card with an odd Threat Level number.
        # If 2 or fewer threat was placed this way, discard a card in your hand
        # with an odd printed cost. »
        impaires = [x for x in Worlds.GetThreatLevelFaces(effect) if x.threat_level % 2 == 1]
        for cible in impaires:
            Faces.PlaceTokensOn([cible], 1, 'threat', effect)
        if len(impaires) <= 2:
            player.AskDiscardHandCards(
                (1, 1),
                effect,
                finder=CardFinder(is_odd_cost=True)
            )

    def boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        # « Boost: Place 2 threat on The Spot. »
        spot = Worlds.FindVillain(effect, name="The Spot")
        if spot:
            Faces.PlaceTokensOn([spot], 2, 'threat', effect)

    return [
        AbilityFactory.WhenThisRevealed(
            None,
            revelee
        ),
        AbilityFactory.WhenCardBecomeBoost(
            "This",
            boost
        ),
    ]
