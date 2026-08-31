from cards.pack import *

# ===========================================================================
# Pack ANGELA — helpers partages du set `Angela`.
#
# ---------------------------------------------------------------------------
# « EACH MINION YOU DEFEATED THIS ROUND »
#
# Deux cartes en dependent : an004 Murderous Glare (1 menace de plus par sbire
# vaincu) et an007 Asgard's Assassin ([wild] au lieu de [physical] si au moins
# un sbire est tombe).
#
# Le moteur tenait DEJA un compteur de mises a mort par joueur,
# `PlayerStat.kill_counter` (game/rule/gameplay.py:43, sur
# `AfterUnitBeDefeated`), mais il est vide a chaque PHASE (`OnBeginPhase`).
# Or ces cartes comptent « this ROUND », ce qui inclut les sbires vaincus
# pendant la phase du vilain — par une riposte, ou par un allie qui defend.
#
# On a donc ajoute `PlayerStat.round_kill_counter`, jumeau du precedent mais
# vide seulement au changement de round. Aucune autre carte du jeu n'en
# depend : le comportement existant est inchange.
# ===========================================================================


def SbiresVaincusCeRound(effect: 'Effect') -> int:
    """Combien de SBIRES le joueur qui resout l'effet a-t-il vaincus ce round ?

    On filtre sur `Minion` : `round_kill_counter` enregistre toutes les unites
    vaincues, vilain et allies compris, et le texte des cartes dit « minion ».
    """
    from game.card.face.card_type import Minion

    initiator = effect.GetInitiator()
    if not isinstance(initiator, Player):
        return 0
    return sum(1 for unit in initiator.stat.round_kill_counter
               if Minion.IsType(unit))


def AuMoinsUnSbireVaincuCeRound(effect: 'Effect', message: Any=None) -> bool:
    return SbiresVaincusCeRound(effect) > 0


def ArmesControlees(effect: 'Effect') -> int:
    """Le nombre de cartes [[WEAPON]] que controle le joueur qui resout l'effet.

    Sert au [star] « Of Heven and Hel » de an001b : +1 REC par arme.
    """
    initiator = effect.GetInitiator()
    if not isinstance(initiator, Player):
        return 0
    return sum(1 for f in initiator.GetControlCards() if f.HasTrait("WEAPON"))
