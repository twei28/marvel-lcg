from cards.pack import *

# ===========================================================================
# Pack DOCTOR DOOM — contenu custom de « Grawlix Ipsum ». Set 139, prefixe `dd`.
#
# Victor von Doom joue le HEROS. Deux sets : `Doctor Doom` (dd001a-dd013,
# dont DEUX obligations) et `Doctor Doom Nemesis` (dd014-dd016, les Quatre
# Fantastiques).
#
# ---------------------------------------------------------------------------
# LE PACK EN UNE PHRASE : TOUT PASSE PAR LE MENTAL
#
#   dd001a Power Syphon   -> payer un SPELL en [mental] pose un compteur power
#   dd001a Overwhelming.. -> 3 compteurs -> villainous jusqu'a la fin du round
#   dd004/dd005/dd006     -> bonus « si paye UNIQUEMENT en [mental] »
#   dd011 Doom's Mask     -> produit du [mental], DOUBLE pour un SPELL
#   dd007 Unparalleled..  -> une ressource a TROIS [mental]
#
# Et le sbire nemesis dd015 Mister Fantastic ETEINT le moteur : tant qu'il est
# engage, chaque [mental] genere devient [physical].
#
# ---------------------------------------------------------------------------
# ⚠ « VILLAINOUS » SUR UN HEROS — EXTENSION MOTEUR DU 01/09/2026
#
# `HasVillainous` etait reserve aux sbires (minion.py:10). Il a ete ajoute a la
# chaine de `Hero` (identity.py) pour dd001a, avec deux consequences a
# connaitre :
#  - un heros devient `CanBoost`, et `can_attack.py:220` appelle
#    `GiveFacedownBoostCardsInternal` a CHAQUE attaque de base : le garde
#    `num <= 0` ajoute dans `can_boost.py` est indispensable, sans lui tout
#    heros non villainous plantait sur `CastTo(Minion|Villain)` ;
#  - `TemporaryGain` et `GainUntilRoundEnd` (face_action.py) ont recu le
#    parametre `villainous`, que `Gain` acceptait deja (face_gain.py:53) —
#    meme oubli et meme correctif que `retaliate` le 4/8/2026.
# Ce n'est PAS un contournement : un heros OFFICIEL a venir (Elektra) portera
# le meme effet.
#
# ---------------------------------------------------------------------------
# ⚠ COLLISION DE NOMS : « Mister Fantastic » (dd015) est un SBIRE nemesis, a ne
# pas confondre avec le HEROS officiel mf001a ni avec l'allie iw002 (pack
# Invisible Woman). Les trois peuvent coexister.
# ===========================================================================


def CompteursPower(effect: 'Effect') -> int:
    """Compteurs `power` sur l'identite du joueur initiateur (max 3)."""
    initiator = effect.GetInitiator()
    if initiator is None:
        return 0
    identity = initiator.GetIdentity()
    if identity is None:
        return 0
    return identity.CastTo(CanPlaceCounter).GetCounters('power')
