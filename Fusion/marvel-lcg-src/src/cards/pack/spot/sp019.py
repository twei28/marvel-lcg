from . import *

# Target Spotted

def GetAbilities() -> Sequence['Ability']:

    def revelee(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Treachery)
        Unused(this)
        player = message.GetToPlayer()

        # « Search the top 8 cards of the encounter deck for The Hypernova and
        # reveal it. If it was not revealed this way, seek a Spot card with the
        # Threat Level keyword and reveal it. »
        trouvee = Search.EncounterCardsTop(
            effect,
            player,
            8,
            name="The Hypernova"
        )
        if trouvee:
            for face in trouvee:
                face.Reveal(player, effect)
            return
        Find.FindAndReveal(
            effect,
            player,
            finder=CardFinder(card_ids=CARTES_A_NIVEAU)
        )

    return [
        AbilityFactory.WhenThisRevealed(
            None,
            revelee
        ),
    ]
