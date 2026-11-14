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


################################################################################
# CAMPAGNE (livret FR p. 4-6, instructions de campagne) : les Sombres Proteges RETIRES de la campagne.
# Le carnet note (`Dark Protege Removed`) les vilains deja utilises aux scenarios 1 et 2 (ecrits par `campaign.py`). S'y ajoutent, des la mise en place du scenario 1,
# les vilains qui PARTAGENT LE NOM d'une identite des joueurs (Daredevil, Elektra) : « cochez le mechant qui partage ce nom, ensuite retirez ce mechant de la campagne ».
# Hors campagne : AUCUN vilain n'est retire (le tirage est libre, comme imprime sur sl001a / sl038a).
################################################################################
CLE_VILAINS_RETIRES = 'Dark Protege Removed'
VILAINS_SOMBRES_PROTEGES = {
    'sl012': 'Archpriestess', 'sl013': 'Daredevil', 'sl014': 'Elektra', 'sl015': 'Gorgon', 'sl016': 'Lady Bullseye', 'sl017': 'White Tiger',
}
_BASE_VILAIN = re.compile(r'^(sl\d{3})')


def BaseDuVilain(card_id: str) -> str:
    """« sl014a » -> « sl014 »."""
    m = _BASE_VILAIN.match(str(card_id))
    return m.group(1) if m else str(card_id)


def VilainsDeLIdentite(effect: 'Effect') -> List[str]:
    """Bases (« sl013 ») des vilains Sombres Proteges dont le nom est celui d'un heros de la table (Daredevil, Elektra)."""
    noms = set()
    for joueur in Worlds.GetPlayers(effect):
        noms.add(str(getattr(joueur, 'hero_name', '') or '').lstrip('* ').strip().lower())
        identite = joueur.GetIdentity()
        if identite is not None:
            noms.add(str(identite.paper.name).lstrip('* ').strip().lower())
    return [base for base, nom in VILAINS_SOMBRES_PROTEGES.items() if nom.lower() in noms]


def VilainsRetiresDeLaCampagne(effect: 'Effect') -> List[str]:
    """Bases (« sl014 ») des vilains Sombres Proteges retires de la campagne ; vide hors campagne."""
    if not Worlds.IsCampaign(effect):
        return []
    retires = {BaseDuVilain(x) for x in CampaignLog.GetListInternal(CLE_VILAINS_RETIRES, effect)}
    retires.update(VilainsDeLIdentite(effect))
    return sorted(retires)


def VilainsTirables(effect: 'Effect') -> List['CardFace']:
    """Les vilains Sombres Proteges mis de cote que le tirage au hasard peut designer (ceux de la campagne encore en lice). Si TOUS sont retires, on retombe sur la
    liste complete : le livret ne dit rien de ce cas, mieux vaut un scenario jouable qu'une mise en place vide."""
    vilains = [x for x in Worlds.GetSetAsideAreaCards(effect) if Villain.IsType(x)]
    retires = set(VilainsRetiresDeLaCampagne(effect))
    restants = [x for x in vilains if BaseDuVilain(x.paper.card_id) not in retires]
    return restants or vilains
