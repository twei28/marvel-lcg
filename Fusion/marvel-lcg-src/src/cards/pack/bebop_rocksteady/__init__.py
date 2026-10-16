from cards.pack import *

# ===========================================================================
# Pack BEBOP & ROCKSTEADY (scenario TMNT, Inkwire), prefixe `tk`. Module plat :
# `cards.pack.bebop_rocksteady.<card_id>` (modele : pack `spot`).
#
# Le scenario a DEUX vilains en jeu en meme temps (comme Sinister Six, mais
# les deux s'activent) ; chacun a deux faces ALERT / K.O. ; chacun porte un
# attachement permanent « Temper » (Hog Wild / Rhino Rage) a deux faces
# ROWDY / ENRAGED qui porte les compteurs « knucklehead ».
# card_id : voir tools/prefixes_fanmade.json (`tk`).
# ===========================================================================

COMPTEUR = 'knucklehead'
ALERTE = "ALERT"
KO = "K.O."
# Les deux familles d'attachement Temper : Hog Wild/Headfirst (Bebop) et
# Rhino Rage/Headstrong (Rocksteady).
FAMILLES = {"Bebop": "HOG", "Rocksteady": "RHINO"}


def NomDuVilain(villain: 'CardFace') -> str:
    """« Bebop » ou « Rocksteady » (par le nom, jamais par un homonyme sbire :
    on ne regarde que les VILAINS en jeu)."""
    for nom in FAMILLES:
        if villain.IsName(nom):
            return nom
    return ""


def VilainsEnJeu(effect: 'Effect') -> List['Villain']:
    """Bebop puis Rocksteady, ceux qui sont encore en jeu."""
    vilains = [v for v in Worlds.GetVillains(effect) if NomDuVilain(v)]
    return sorted(vilains, key=lambda v: 0 if NomDuVilain(v) == "Bebop" else 1)


def VilainNomme(effect: 'Effect', nom: str) -> 'Villain|None':
    for v in VilainsEnJeu(effect):
        if NomDuVilain(v) == nom:
            return v
    return None


def AutreVilain(effect: 'Effect', villain: 'CardFace') -> 'Villain|None':
    for v in VilainsEnJeu(effect):
        if v is not villain and v.card is not villain.card:
            return v
    return None


def EstKO(villain: 'CardFace') -> bool:
    return villain.HasTrait(KO)


def EstAlerte(villain: 'CardFace') -> bool:
    return villain.HasTrait(ALERTE)


def TemperDe(villain: 'CardFace') -> 'Attachment|None':
    """L'attachement Temper (Hog Wild / Headfirst ou Rhino Rage / Headstrong)
    accroche a ce vilain, quelle que soit sa face."""
    if villain is None:
        return None
    for att in villain.GetAttachedAttachments():
        if att.HasTrait("TEMPER"):
            return att
    return None


def TousLesTempers(effect: 'Effect') -> List['Attachment']:
    res = []
    for v in VilainsEnJeu(effect):
        t = TemperDe(v)
        if t is not None:
            res.append(t)
    return res


def Compteurs(temper: 'CardFace|None') -> int:
    return temper.GetCounters(COMPTEUR) if temper is not None else 0
