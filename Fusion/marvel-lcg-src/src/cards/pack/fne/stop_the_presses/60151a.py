from . import *
from cards.pack.fne.campaign import CapacitesDeCampagne
import random

# Stop the Presses! 1A
# Setup: Put the Daily Bugle environment into play. Each player puts a random
#   DAILY BUGLE support from this encounter set into play under their
#   control. Remove each remaining DAILY BUGLE support from the game.
# L'environnement et les 4 soutiens sont dans la mise de cote du scenario.

def GetAbilities() -> Sequence['Ability']:

    def mise_en_place(effect: 'Effect', message: 'Message.WhenCardSetup') -> None:
        premier = Worlds.GetFirstPlayer(effect)
        de_cote = list(Worlds.GetSetAsideAreaCards(effect))
        bugle = [f for f in de_cote if f.IsName("Daily Bugle") and Environment.IsType(f)]
        if bugle:
            bugle[0].PutIntoPlay(premier, effect)
        soutiens = [f for f in de_cote if Support.IsType(f) and f.HasTrait("DAILY BUGLE")]

        def distribuer(player: 'Player') -> None:
            if not soutiens:
                return
            choisi = Rand.RandomChoice(soutiens, effect)
            soutiens.remove(choisi)
            choisi.PutIntoPlay(player, effect, under_control=True)

        Players.ForEachPlayer(effect, distribuer)
        if soutiens:
            Faces.RemoveAllFromGame(list(soutiens), effect)

    return [
        AbilityFactory.WhenCardSetup("This", mise_en_place),
        # Mode campagne (livret p. 9 et encarts CAMPAIGN INSTRUCTIONS) : inerte
        # hors campagne (`Worlds.IsCampaign`), voir cards/pack/fne/campaign.py.
        *CapacitesDeCampagne("stop_the_presses"),
    ]
