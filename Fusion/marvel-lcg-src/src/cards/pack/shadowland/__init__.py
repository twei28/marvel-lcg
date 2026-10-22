from cards.pack import *
import re

# ===========================================================================
# Helpers partages du pack SHADOWLAND (pack scenario officiel MC65, prefixe `sl`,
# voir docs/packs/shadowland/). Ici : les POSITIONS (Shadows in the Night).
#
# Deux cartes Environnement recto-verso, mises en jeu ensemble a la mise en place :
#   sl003 = position du VILAIN  (face a « The Streets Below », face b « Atop the Tenshu »)
#   sl004 = position du HEROS   (memes noms de faces)
# ⚠ Les deux cartes portent les MEMES NOMS de faces : on les distingue TOUJOURS par
# card_id, jamais par le nom. La position se lit sur la face visible (a / b).
# « Change the villain's position » = retourner sl003. « if it has not changed this
# phase » : un changement n'est permis qu'une fois par phase (`world.phase_id`, qui
# monte a chaque phase des joueurs / du mechant).
# ===========================================================================

POSITION_VILAIN = ["sl003a", "sl003b"]
POSITION_HEROS = ["sl004a", "sl004b"]
STREETS, TENSHU = "streets", "tenshu"


def _position(effect: 'Effect', ids: List[str]) -> 'str|None':
    face = Worlds.FindCardOnField(effect, card_ids=ids)
    if face is None:
        return None
    return STREETS if str(face.paper.card_id) == ids[0] else TENSHU


def PositionDuVilain(effect: 'Effect') -> 'str|None':
    """STREETS / TENSHU, ou None si la carte de position n'est pas en jeu."""
    return _position(effect, POSITION_VILAIN)


def PositionDuHeros(effect: 'Effect') -> 'str|None':
    return _position(effect, POSITION_HEROS)


def PositionsIdentiques(effect: 'Effect') -> bool:
    """« If both positions are the same ». Faux si l'une des deux cartes manque."""
    v, h = PositionDuVilain(effect), PositionDuHeros(effect)
    return v is not None and v == h


def ChangerPositionVilain(effect: 'Effect', *, si_pas_change_cette_phase: bool=False) -> bool:
    """« Change the villain's position [if it has not changed this phase] ».
    Rend True si la carte a ete retournee. Avec `si_pas_change_cette_phase`, un
    deuxieme changement dans la meme phase est refuse (mais les changements
    INCONDITIONNELS, sans ce drapeau, comptent aussi comme « changes cette phase »)."""
    face = Worlds.FindCardOnField(effect, card_ids=POSITION_VILAIN)
    if face is None:
        return False
    monde = effect.world
    if si_pas_change_cette_phase and getattr(monde, "_sl_phase_position", None) == monde.phase_id:
        return False
    face.card.Flip(effect)
    monde._sl_phase_position = monde.phase_id
    return True


################################################################################
# CARTES LIEES (mot-cle « Linked (A, B, or C) » de Dark Protege, sl018 a sl027). La carte est liee aux TROIS vilains nommes : quand le vilain tire au hasard
# est l'un d'eux, la carte est melangee dans le deck de rencontre ; sinon elle reste de cote. `desc.Linked` du moteur n'accepte qu'UN nom : on lit donc
# la liste dans le TEXTE imprime (« Linked (Elektra, Lady Bullseye, or White Tiger). »), le seul endroit ou elle est complete.
################################################################################
_LIEE = re.compile(r'Linked \(([^)]*)\)')


def VilainsLies(face: 'CardFace') -> List[str]:
    """Les noms de vilains auxquels la carte est liee, [] si elle ne porte pas « Linked (...) »."""
    m = _LIEE.search(face.paper.text or '')
    if m is None:
        return []
    # « A, B, or C » : la virgule est suivie de « or » devant le DERNIER nom (piege : sans ca, « or White Tiger » ne correspond a aucun vilain)
    return [re.sub(r'^or\s+', '', n.strip()) for n in re.split(r',\s*|\s+or\s+', m.group(1)) if n.strip()]


def NomDuVilain(face: 'CardFace') -> str:
    """« * Gorgon » -> « Gorgon » (les uniques portent une etoile devant leur nom)."""
    return face.paper.name.lstrip('* ').strip()
