from cards.pack import *
# Helpers partages du set « Raza Nemesis » (Phenexian et Mysteltainn, prefixe `rl`).
# ⚠ Un helper vit ICI, jamais dans le `__init__.py` du pack (NameError avale, lecon hk005).
SEUIL_DEGATS = 5
NOM_ZZZXX = "Zzzxx"


def TrouverZzzxx(effect: 'Effect') -> 'CardFace|None':
    """Zzzxx en jeu, sinon None."""
    return Worlds.FindCardOnField(effect, name=NOM_ZZZXX, card_type=Minion)


def MettreZzzxxEnJeu(effect: 'Effect', joueur: 'Player|None') -> None:
    """« Find Zzzxx and put him into play engaged with you » (deck rencontre, defausse ; deja en jeu : il t'engage)."""
    if joueur is None:
        return
    en_jeu = TrouverZzzxx(effect)
    if en_jeu is not None:
        en_jeu.CastTo(Minion).EngagePlayer(joueur, effect)
        return
    face = Search.EncounterCard(effect, joueur, include_discard_pile=True, name=NOM_ZZZXX, card_type=Minion)
    if face is not None:
        face.PutIntoPlay(joueur, effect)
