from . import *

# Reckoning Begins (2A) — MANIGANCE PRINCIPALE, stade 2.
# When Revealed: Flip the villain to its DISCOVERED side and set the Hala environment aside. Each player
#   draws 1 card.
#
# Cartes de reference :
#  - « When Revealed » d'une face A : `WhenThisRevealed(None, op)`, modele gs118a (Majestrix).
#  - « Flip the villain to its DISCOVERED side » : `villain.card.Flip(effect)` — MEME carte, attachements,
#    statuts, boosts et degats restent (mots-cles/hidden.md ; modele exact : Green Goblin/Norman Osborn,
#    `gob/risky_business/02006a.py`, et Veranke `skrull_menace/secret_invasion/sk189a.py`).
#  - « set the Hala environment aside » : `Faces.SetAside` (`game/operate/faces.py`).
#  - « each player draws 1 card » : `Players.ForEachPlayer` + `player.DrawUp(1, effect)`.
#
# ⚠ Mots-pieges : le flip ne doit partir qu'UNE FOIS (« This » stade 2A ne se revele qu'une fois dans une
# partie normale, mais un retour en arriere par une autre carte resterait sans effet si le mechant est deja
# DISCOVERED : garde `HasTrait("HIDDEN")`) ; « set aside », pas « remove from the game » ni « discard ».


def GetAbilities() -> Sequence['Ability']:

    def revele(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        Unused(message)
        villain = LeVilain(effect)
        if villain is not None and villain.HasTrait("HIDDEN"):
            villain.card.Flip(effect)
        hala = HalaEnJeu(effect)
        if hala is not None:
            Faces.SetAside([hala], effect)

        def chacun(joueur: 'Player') -> None:
            joueur.DrawUp(1, effect)
        Players.ForEachPlayer(effect, chacun)

    return [
        AbilityFactory.WhenThisRevealed(None, revele),
    ]
