from cards.pack import *

# ===========================================================================
# Set nemesis « Spider-Man 2099 Nemesis » : Electro. CINQ cartes en QUATRE
# noms — Containment Breach (complot annexe, Amplify 1), Electro (sbire),
# Power Surge x2 (traitrise), Charged (attachement sur l'identite).
#
# ⚠ L'OBLIGATION `sm013` Future in Crisis N'EST PAS ICI : son bandeau imprime
# dit « SPIDER-MAN », son `set_name` est donc celui du heros et son module vit
# dans `spider_man_2099/spider_man_2099/`. Le moteur cherche le module dans le
# dossier du `set_name`, PAS du pack (database.py:195) : une obligation rangee
# ici serait chargee... jamais, et EN SILENCE (lecon `bt019`, 1/9/2026).
#
# ⚠⚠ TOUT LE SET TOURNE AUTOUR DE DEUX GESTES, ET C'EST VOULU :
#  1. DEFAUSSER DEPUIS LE DESSUS DU DECK JOUEUR — comme la capacite
#     « Acceleration » du heros. Le set retourne donc l'arme du heros contre
#     lui. ⚠ CONSEQUENCE A NE PAS RATER : `sm002` Ghost Rider reagit « after
#     Ghost Rider is discarded by your ACCELERATION ability » et ne doit PAS
#     se declencher sur ces cartes-ci. C'est le marqueur du pack qui fait le
#     tri, pas le message.
#  2. COMPTER LES ICONES [energy] IMPRIMEES sur ce qui vient d'etre defausse.
#     Trois cartes le font (`sm014`, `sm015`, `sm016`), d'ou l'helper commun
#     ci-dessous. On compte les ICONES, jamais les CARTES : une carte a deux
#     icones energie en vaut deux.
#
# ⚠ HOMONYMES : « * Electro » et « Power Surge » n'ont aucun homonyme au
# depot, mais aucune carte du set ne cherche par NOM de toute facon.
# ===========================================================================

COULEUR_ENERGIE = "Y"


def EstJoueur(objet: Any) -> bool:
    """`Player.IsType` SANS le risque d'AttributeError (lecon sf002 / sf013)."""
    return objet is not None and hasattr(objet, "IsPlayer") and Player.IsType(objet)


def Hote(face: 'CardFace|None') -> 'CardFace|None':
    """A QUI cette carte est-elle accrochee ? `None` si elle ne l'est pas.

    Accesseur SUR, a employer partout a la place de `GetBindFace()` (modele
    blade, ares, blink, yondu, sunfire). C'est par lui que `sm017` Charged
    retrouve « son » joueur : un attachement de RENCONTRE n'a pas de
    controleur joueur, seulement un hote.
    """
    return getattr(face, "bind_face", None) if face is not None else None


def IconesEnergie(faces: Sequence['CardFace']) -> int:
    """Le nombre d'icones [energy] IMPRIMEES sur ces cartes.

    ⚠ `convert_green_res=False` : sans lui, une ressource wild ([wild], G)
    serait comptee comme une energie, et les trois cartes du set frapperaient
    trop fort. Le texte imprime dit « [energy] resources », pas « resources
    that can pay for energy ».
    """
    reelles = [f for f in faces if f is not None]
    if not reelles:
        return 0
    return FacesCounter.GetPrintedResources(reelles).GetColor(
        COULEUR_ENERGIE, convert_green_res=False)
