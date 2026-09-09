from cards.pack import *

# ===========================================================================
# Set nemesis « Superior Spider-Man Nemesis » : Hobgoblin. CINQ cartes —
# Goblin Protocol (complot annexe), Hobgoblin (sbire Villainous), Lunatic Laugh
# (traitrise), Goblin Glider et Pumpkin Bombs (attachements).
#
# ⚠ LES DEUX OBLIGATIONS (`su013` Ghost of a Conscience, `su014` Crisis of
# Conscience) NE SONT PAS ICI : leur bandeau imprime dit « SPIDER-MAN », donc
# leur `set_name` est celui du HEROS et leurs modules vivent dans
# `superior_spider_man/superior_spider_man/`. Le moteur cherche le module dans
# le dossier du `set_name`, PAS du pack (database.py:195) : rangees ici, elles
# ne seraient jamais chargees, EN SILENCE (lecon `bt019`).
#
# ⚠ CE SET PUNIT LE MOT-CLE MAISON DU HEROS. `su015` Goblin Protocol fait
# COMPTER la menace posee sur les sbires traces dans le total du complot
# principal : le heros, en tracant, remplit lui-meme la barre du vilain. C'est
# la seule carte du jeu ou la menace d'un SBIRE agit, et c'est ce qui justifie
# le compteur `threat` ajoute a l'enum `COUNTER` le 08/09/2026.
# ===========================================================================

ID_HOBGOBLIN = "su016"
COMPTEUR_MENACE: 'CardFace.COUNTER' = 'threat'


def EstJoueur(objet: Any) -> bool:
    return objet is not None and hasattr(objet, "IsPlayer") and Player.IsType(objet)


def Hote(face: 'CardFace|None') -> 'CardFace|None':
    """A QUI cette carte est-elle accrochee ? `None` si elle ne l'est pas."""
    return getattr(face, "bind_face", None) if face is not None else None


def CardId(face: 'CardFace|None') -> str:
    """⚠ `face.card_id` N'EXISTE PAS : le chemin est `face.paper.card_id`."""
    paper = getattr(face, "paper", None) if face is not None else None
    return getattr(paper, "card_id", "") or ""


def MenaceSurSbire(face: 'CardFace|None') -> int:
    if face is None:
        return 0
    lire = getattr(face, "GetCounters", None)
    if lire is None:
        return 0
    return int(lire(COMPTEUR_MENACE) or 0)
