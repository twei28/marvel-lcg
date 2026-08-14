from . import *

# * Vulture (III)

def GetAbilities() -> Sequence['Ability']:

    def revelation(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        # « When Revealed: Deal each player an encounter card. »
        Players.ForEachPlayer(
            effect, lambda joueur: joueur.DealEncounterCards(1, effect))

    return [
        NePeutEtreAttaqueQueParLesAeriens(),
        AbilityFactory.WhenThisRevealed(
            None,
            revelation
        ),
    ]
