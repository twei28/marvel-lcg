from cards.pack.skrull_menace.communs_modulaires import *

# ===========================================================================
# Alternative « STANDARD SKRULL » (Skrull Menace, Kajislav) — sk254-sk259 (7 cartes).
# Livret (« Alternative sets ») : « when a scenario requires the Standard or Expert sets, you may
# replace them » par Standard Skrull / Expert Skrull. Le set remplace `standard` : meme nombre de
# cartes (7 : Impostor, Cursed by the Past, Experiment Subject, Forge Ahead, Mobilization, 2 Stick
# to the Plan). sk254 Impostor n'a PAS de script ici (`ability_link` vers sk098).
# Dossier : `FileManager.CleanName("Standard Skrull")` = `standard_skrull`.
# ===========================================================================


def SbireNemesisEnJeu(joueur: 'Player', effect: 'Effect') -> 'CardFace|None':
    """Le sbire NEMESIS du joueur, s'il est en jeu (modele fne/kingpin `SbireNemesisEnJeu`)."""
    return Worlds.FindCardOnField(effect, finder=CardFinder(card_type=Minion, is_nemesis=joueur))
