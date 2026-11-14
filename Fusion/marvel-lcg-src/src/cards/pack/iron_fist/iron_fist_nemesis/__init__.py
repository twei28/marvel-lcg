from cards.pack import *
from cards.pack.iron_fist.iron_fist import CHI, Chi

# ===========================================================================
# Obligation et set nemesis d'Iron Fist (Hero Pack officiel MC64EN) : 64026 Lack of Chi (obligation, set « Iron Fist »
# 1/1 sur la carte, range ici avec le set nemesis), 64027 Davos, 64028 Crane Daughter (x3), 64029 Steel Serpent.
# Ajoute le 14/11/2026 depuis les scans mc4db (.planning/elektra-iron-fist-scans-mc4db/).
# Gabarits PROCESSUS-CARTE : docs/packs/iron_fist_cartes.md. Cas : tools/cas/iron_fist_nemesis.py (« [iron_fist_nem] »).
#
# MECANIQUE CENTRALE : les Crane Daughter GLISSEES sous Davos (fiche docs/reference/mots-cles/tuck.md). Une carte glissee
# n'est PAS en jeu ; `Worlds.FindCardOnField` la voit pourtant (zone sur le terrain) : toujours filtrer sur `IsInPlay()`.
# ⚠ Seul 64027 Davos porte `desc.Nemesis` (seule carte imprimee « (Iron Fist's nemesis minion.) »). Noms SANS l'etoile.
# ===========================================================================

NOM_DAVOS = "Davos"
NOM_CRANE = "Crane Daughter"


def EstCrane(face: 'CardFace|None') -> bool:
    return face is not None and face.paper.name.lstrip("* ") == NOM_CRANE


def DavosEnJeu(effect: 'Effect') -> 'Minion|None':
    """Davos EN JEU (jamais une copie glissee ou hors jeu)."""
    for face in Worlds.FindCardsOnField(effect, name=NOM_DAVOS, card_type=Minion):
        if face is not None and face.IsInPlay():
            return face.CastTo(Minion)
    return None


def CranesSous(davos: 'CardFace|None') -> List['CardFace']:
    """Les Crane Daughter glissees sous Davos."""
    if davos is None:
        return []
    return [f for f in davos.GetPlacedCardArea().Get() if EstCrane(f)]


def CranesEnJeu(effect: 'Effect') -> List['CardFace']:
    """Les Crane Daughter EN JEU (sbires engages), pas celles glissees sous Davos."""
    return [f for f in Worlds.FindCardsOnField(effect, name=NOM_CRANE, card_type=Minion) if f is not None and f.IsInPlay()]


def Glisser(davos: 'CardFace', faces: Sequence['CardFace'], effect: 'Effect') -> None:
    """Glisse sous Davos, visible de tous (ce sont des cartes connues ; modele bs002 Beast's Lab)."""
    for face in faces:
        davos.TuckCardUnderHere(face, effect, peek=True)


def MelangerQuandVaincu() -> 'Ability':
    """« When Defeated: Shuffle Crane Daughter into the encounter deck. » (modele : 50098 Machete)."""
    def melanger(effect: 'Effect', message: 'Message.WhenUnitBeDefeated') -> None:
        Faces.ShuffleAllTo([effect.this], "EncounterDeck", effect)
    return AbilityFactory.WhenUnitBeDefeated(AbilityType.WhenDefeated, "This", melanger)
