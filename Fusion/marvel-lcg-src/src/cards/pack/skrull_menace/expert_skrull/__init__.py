from cards.pack.skrull_menace.communs_modulaires import *

# ===========================================================================
# Alternative « EXPERT SKRULL » (Skrull Menace, Kajislav) — sk260-sk262 (3 cartes).
# Remplace le set `expert` (3 cartes : Exhaustion, Masterplan, Under Fire) quand le livret le permet
# (« Alternative sets »). Dossier : `FileManager.CleanName("Expert Skrull")` = `expert_skrull`.
# ===========================================================================


def SbireNemesisEnJeu(joueur: 'Player', effect: 'Effect') -> 'CardFace|None':
    """Le sbire NEMESIS du joueur, s'il est en jeu (modele fne/kingpin `SbireNemesisEnJeu`)."""
    return Worlds.FindCardOnField(effect, finder=CardFinder(card_type=Minion, is_nemesis=joueur))
