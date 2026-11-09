from . import *

# * Call of the Demoness — MANIGANCE ANNEXE. Boost 2, menace de depart 3[per_hero] (natifs, `desc`).
# This card cannot leave play while facedown MYSTIC minion is in play. Each facedown MYSTIC minion engaged with a player has a base SCH of 1, a base ATK of 1, and a base hit
# points of 1. Forced Response : After the villain phase begins, the first player puts the top card of their discard pile into play facedown engaged with them as a MYSTIC minion.
#
# Cartes de reference : 04140 (`SchemeCannotLeavlPlayWhile("This", conditions=..)`), core/ultron (`PutYouDeckTopCardAsFacedownMinion` : `MettreEnSbireFaceCachee`), `AfterPhaseBegin`.
# Les valeurs de base (SCH 1, ATK 1, PV 1) sont celles de la carte technique `hellspawn_minion` (construire_cartes.py) : les sbires face cachee n'existent que par cette famille de cartes.
# ⚠ Mots-pieges : « cannot leave play WHILE a facedown MYSTIC minion is in play » : impossible a vaincre tant qu'il en reste un ; « the FIRST PLAYER » : lui seul, au debut de la phase
# du mechant ; « the top card of THEIR discard pile » : la defausse de CE joueur ; defausse vide : rien.


def GetAbilities() -> Sequence['Ability']:
    def appel(effect: 'Effect', message: 'Message.AfterPhaseBegin') -> None:
        Unused(message)
        joueur = Worlds.GetFirstPlayer(effect)
        dessus = DessusDeLaDefausse(joueur, 1)
        if dessus:
            MettreEnSbireFaceCachee(effect, joueur, dessus[0])

    return [
        AbilityFactory.SchemeCannotLeavlPlayWhile("This", conditions=[lambda effect, message: SbiresFaceCachee(effect) != []]),
        AbilityFactory.AfterPhaseBegin(AbilityType.ForcedResponse, "Villain", appel),
    ]
