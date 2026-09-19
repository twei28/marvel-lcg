from . import *
from cards.pack.fne.campaign import CapacitesDeCampagneKingpin

# The King's Gambit (1A)
# Setup: Each player reveals their set-aside nemesis minion. Each player whose
#   nemesis minion shares a title with a character in play instead removes
#   their nemesis minion from the game, then finds an UNDERLING minion that is
#   not in play and reveals it.
# Modele : 60121a (WhenCardSetup("This")). « shares a title » = meme nom
# qu'un personnage (Unit2) en jeu, par ex. le sbire Kingpin, nemesis d'Echo.

def GetAbilities() -> Sequence['Ability']:

    def mise_en_place(effect: 'Effect', message: 'Message.WhenCardSetup') -> None:

        def par_joueur(joueur: 'Player') -> None:
            for sbire in SbiresNemesisMisDeCote(joueur):
                noms = {c.name for c in Worlds.GetOnFieldCharacters(effect)}
                if sbire.name in noms:
                    Faces.RemoveAllFromGame([sbire], effect)
                    TrouverEtRevelerUnderling(effect, joueur)
                else:
                    sbire.Reveal(joueur, effect)

        Players.ForEachPlayer(effect, par_joueur)

    return [
        AbilityFactory.WhenCardSetup("This", mise_en_place),
        # Mode campagne (livret p. 9 et encarts CAMPAIGN INSTRUCTIONS) : inerte
        # hors campagne (`Worlds.IsCampaign`), voir cards/pack/fne/campaign.py.
        *CapacitesDeCampagneKingpin(),
    ]
