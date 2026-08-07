from . import *
from cards.pack.aoa.campaign_setup import CampaignSetup

# Hunting Gene Traitors

def GetAbilities() -> Sequence['Ability']:

    def hunting_gene_traitors(effect: 'Effect', message: 'Message.WhenCardSetup') -> None:
        this = effect.this.CastTo(MainScheme)
        Unused(this)

        # ~~Reveal the Gene Pool side scheme.~~

        if Worlds.IsExpert(effect):
            def action(player: 'Player'):
                player.DealEncounterCards(1, effect)

            Players.ForEachPlayer(effect, action)

    return [
        *CampaignSetup(1),
        AbilityFactory.WhenCardSetup(
            "This",
            hunting_gene_traitors
        ),
    ]

