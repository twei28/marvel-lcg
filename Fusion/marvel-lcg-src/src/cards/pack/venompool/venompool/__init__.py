from cards.pack import *

# ===========================================================================
# Pack VENOMPOOL — helpers partages du set `Venompool`.
#
# ---------------------------------------------------------------------------
# 1. « DRAIN X » — ET CETTE FOIS LE MOT-CLE EST DEFINI PAR ECRIT
#
# L'insert du pack (« Venompool Insert.png ») le definit noir sur blanc :
#
#     « When an ability instructs you to drain X from an enemy, deal X damage
#       to that enemy, then heal X damage from your identity. »
#
# C'est EXACTEMENT la lecture retenue a l'aveugle avec l'utilisateur le
# 4/8/2026 pour le pack `agent_anti_venom`, ou le mot-cle etait employe sans
# jamais etre defini (voir docs/reference/mots-cles/drain-x.md). La convention
# est donc confirmee par une source imprimee, elle n'est plus une supposition.
#
# On NE reutilise PAS `Drain()` d'agent_anti_venom : chaque pack garde son
# helper local (l'identite soignee n'est pas la meme, et un pack ne doit pas
# dependre d'un autre pack custom). Le corps est volontairement identique.
#
# ---------------------------------------------------------------------------
# 2. « TRUE FORM » — TROIS CARTES LISENT SA PRESENCE
#
# vp003 (4 degats -> 6), vp004 (l'attaque gagne piercing) et vp010 elle-meme.
# La recherche se fait dans la zone du JOUEUR qui resout l'effet, pas sur tout
# le plateau : True Form est une amelioration attachee a une identite, deux
# joueurs peuvent en avoir une chacun.
# ===========================================================================

TRUE_FORM_NAME = "True Form"
KLYNTAR_SUIT_NAME = "Klyntar Suit"


def GetVenompool(effect: 'Effect') -> Any:
    """L'identite du joueur qui resout l'effet, quelle que soit sa face.

    Volontairement resolu par le JOUEUR et jamais par le nom « Venompool » :
    dt105 (pack `determination`) est un ALLIE qui porte deja ce nom, et une
    recherche par nom pourrait le designer a la place de l'identite.
    """
    initiator = effect.GetInitiator()
    if initiator is None:
        return None
    return initiator.GetIdentity()


def Drain(source: 'CardFace', targets: Sequence['CardFace'], value: int, effect: 'Effect') -> None:
    """X degats a l'ennemi, puis X soins sur l'identite (definition de l'insert)."""
    if not targets:
        return
    source.DealDamage(targets, value, effect)
    identity = GetVenompool(effect)
    if identity is not None:
        source.HealthUnits([identity], value, effect)


def ControlsUpgrade(effect: 'Effect', name: str) -> bool:
    """Le joueur qui resout l'effet controle-t-il l'amelioration nommee ?

    Modele dt080 (`player.GetControlCards()` + `f.paper.name`) : on interroge
    la zone du JOUEUR, jamais le plateau entier. True Form et Klyntar Suit
    s'attachent a une identite, deux joueurs peuvent en avoir chacun une.
    """
    initiator = effect.GetInitiator()
    if initiator is None:
        return False
    return any(f.paper.name == name for f in initiator.GetControlCards())


def TrueFormInPlay(effect: 'Effect', message: Any=None) -> bool:
    return ControlsUpgrade(effect, TRUE_FORM_NAME)


def TrueFormAbsent(effect: 'Effect', message: Any=None) -> bool:
    return not ControlsUpgrade(effect, TRUE_FORM_NAME)
