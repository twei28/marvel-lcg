from . import *

# hs226 Master Trapper (environnement du mode Hunter, scenario 5)
# Forced Response : apres l'etape 1 de la phase du vilain, distribue a chaque joueur
# 1 carte TRAP face cachee.
# Forced Interrupt : quand la defausse TRAP est remelangee dans le deck TRAP,
# distribue au premier joueur 1 carte rencontre face cachee (porte par
# `RemelangeDefaussePiege`, seul point ou ce remelange a lieu).

def GetAbilities() -> Sequence['Ability']:

    def pieger(effect: 'Effect', message: 'Message.AfterResolveVillainPhaseStep') -> None:
        from cards.pack.hunting_season.trap import DonnerPiege
        for joueur in Worlds.GetPlayers(effect):
            DonnerPiege(effect, joueur)

    return [
        AbilityFactory.AfterResolveVillainPhaseStep(AbilityType.ForcedResponse, 1, pieger),
    ]
