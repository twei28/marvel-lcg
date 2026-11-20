from . import *
from cards.pack.hellfire_hunt import campaign as hc
from cards.pack.mts.campaign import WriteCampaignLogAtGameOver

# The Hellfire Club's Revenge (1A). « Setup : Choose 3 modular sets, each with an ELITE, HELLFIRE minion ... and shuffle them into the encounter deck. Shuffle every
# ELITE, HELLFIRE minion to create the Hellfire deck and set it next to the encounter deck. Put the Nova's Psychic Puppetry side scheme into play, CONTROLLED side
# face up. » Le choix des modules est fait par l'ecran de preparation (`data/scenarios/hellfire_torn*.json`, `modular_sets`).
# Cartes de reference : hf104a (`WhenCardSetup("This", ...)`, deck de rencontre fouille a la mise en place), hf048 / `campaign.py` (deck de table), Light at the
# End 27102a (manigance annexe a deux faces mise en jeu au depart). Mise en place de campagne : `hc.MiseEnPlace(4)` (Potential Ally, Xavier's Institute,
# Recruited Mutants, PV experts) ; releve de fin de partie : `ReleveTorn` (le releve commun + les allies sortis de la zone mise de cote, voir __init__).


def GetAbilities() -> Sequence['Ability']:
    def mise_en_place(effect: 'Effect', message: 'Message.WhenCardSetup') -> None:
        Unused(message)
        ConstruireLeDeckHellfire(effect)
        faces = Worlds.GetSetAsideAreaCards(effect, CardFinder(name=NOM_PUPPETRY))
        if faces:
            faces[0].PutIntoPlay("FirstPlayer", effect)

    return [AbilityFactory.WhenCardSetup("This", mise_en_place), hc.MiseEnPlace(4),
            WriteCampaignLogAtGameOver(ReleveTorn, scenario_id=hc.SCENARIOS[3])]
