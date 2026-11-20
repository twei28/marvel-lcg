from . import *

# Fortress Lockdown (2A) — MANIGANCE PRINCIPALE, stade 2.
# In expert mode, the villain gets +3[per_hero] hit points.
# When Revealed : Change the villain's position. Each player searches the encounter deck and discard pile for a minion and reveals it. (Shuffle.)
#
# Cartes de reference : sl001a/sl001b (ce pack), sw/... pour la recherche : voir `RechercherUnSbire` (shadowland/__init__.py).
# ⚠ Mots-pieges : « change the villain's position » inconditionnel ; « EACH player searches » : chaque joueur, l'un apres l'autre, dans l'ordre des joueurs ;
#  « the encounter deck AND discard pile » : les deux piles ; « reveals it » : le sbire est REVELE (ses When Revealed partent) ; « (Shuffle.) » : on melange apres chaque recherche.


def GetAbilities() -> Sequence['Ability']:

    def revele(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        Unused(message)
        ChangerPositionVilain(effect)
        Players.ForEachPlayer(effect, lambda joueur: RechercherUnSbire(effect, joueur))

    return [
        *AbilitesPvExpert(),
        AbilityFactory.WhenThisRevealed(None, revele),
    ]
