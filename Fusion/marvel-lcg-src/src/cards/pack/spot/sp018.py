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
            # Ni `AskDiscardHandCards` ni `CardFinder(is_odd_cost=...)` n'existent (AttributeError a chaque defausse, releve le
            # 26/10/2026) : on filtre la main sur le cout IMPRIME impair, puis le joueur CHOISIT (defausse obligatoire s'il y en a).
            impaires_en_main = [x for x in player.hand_cards.Get() if FacesCounter.GetPrintedCost([x]) % 2 == 1]
            if impaires_en_main:
                player.AskDiscardFaces(impaires_en_main, (1, 1), effect)

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
