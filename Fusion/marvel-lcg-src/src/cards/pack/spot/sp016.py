from . import *

# ...Comes Around!

def GetAbilities() -> Sequence['Ability']:

    def revelee(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Treachery)
        player = message.GetToPlayer()

        # « Discard the top 2 cards of the encounter deck. For each Spot card
        # discarded this way, choose to either place 2 threat on the main
        # scheme or reveal it. If no Spot cards were discarded this way, this
        # card gains surge. »
        defaussees = Worlds.DiscardEncounterCards(2, effect)
        cartes_du_spot = [x for x in defaussees if x.paper.set_name == "The Spot"]
        if not cartes_du_spot:
            this.GainSurge(+1, effect)
            return
        for face in cartes_du_spot:
            player.ChooseAbilities(
                effect,
                AbilityFactory.ForChoiceAbility(
                    "Place 2 threat on the main scheme",
                    lambda targets: Utility.PlaceThreatOnOneScheme(player, 2, effect)
                ),
                AbilityFactory.ForChoiceAbility(
                    "Reveal it",
                    lambda targets, face=face: face.Reveal(player, effect)
                ),
            )

    def boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        # « Boost: Discard the top 2 cards of the encounter deck. »
        Worlds.DiscardEncounterCards(2, effect)

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
