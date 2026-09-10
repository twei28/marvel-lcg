from cards.pack import *
from cards.pack.spider_woman_kajislav.spider_woman_kajislav import *

################################################################################
# Set nemesis B de Spider-Woman (Kajislav) — « verze 2 », dit set MS. MARVEL.
#
# ⚠⚠ LE PACK LIVRE DEUX SETS NEMESIS ALTERNATIFS, tous deux numerotes 1/5 a
# 5/5. Le deck de depart monte le set A « Man-Bull » (`sw021`-`sw024`), parce
# que son obligation `sw020` Separation from the Child est rangee avec le set
# HEROS. Celui-ci a SA PROPRE obligation (`sw027` Fugitive, en double) et le
# moteur n'accepte qu'un set nemesis par heros : il est donc livre en SET DE
# RENCONTRE MODULAIRE (`data/encounter_sets/spider_woman_kajislav_ms_marvel`).
#
# LES QUATRE CARTES TOURNENT AUTOUR D'UNE SEULE : Superhuman Registration Act.
# Trois d'entre elles y posent de la menace, et c'est cette menace qui allume
# son icone d'ALEA. Sans elle en jeu, le set ne fait presque rien : c'est
# assume, et c'est ce qui est ecrit.
################################################################################

ACTE = "Superhuman Registration Act"


def ActeDEnregistrement(effect: 'Effect') -> 'CardFace|None':
    """La manigance `sw026` en jeu, ou None.

    ⚠ Les trois cartes qui y posent de la menace ne disent PAS quoi faire si
    elle n'est pas en jeu. Rien, donc : pas de report, pas de repli sur le
    complot principal. On renvoie None et l'appelant s'arrete.
    """
    return Worlds.FindCardOnField(effect, name=ACTE, card_type=EncounterSideScheme)


def PoserSurLActe(source: 'CardFace', valeur: int, effect: 'Effect') -> None:
    """Pose `valeur` menace sur l'Acte s'il est en jeu."""
    acte = ActeDEnregistrement(effect)
    if acte is not None:
        source.PlaceThreatOnSchemes([acte], valeur, effect)
