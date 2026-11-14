from cards.pack import *

# ===========================================================================
# Set « Carnage Nemesis » (ca015-ca018) : Torment, Meticulous Targeting, Death Spiral, Closing the Loops x2.
# ⚠ Helpers partages ICI (lecon hk005 : un helper defini dans le `__init__.py` du PACK leve un NameError avale par le moteur).
# ===========================================================================
NOM_TORMENT = "Torment"


def ClassificationDe(face: 'CardFace') -> 'set[str]':
    """« classification » d'un personnage ami (texte de Torment : identity-specific, aspect, or basic), en ENSEMBLE : une identite est `IdentitySpecific` ;
    une carte joueur porte ses classes imprimees (`card_classes`, `desc.Class` : `Hero` y devient `IdentitySpecific`, un aspect y ajoute `Aspect`, ignore ici :
    deux aspects differents sont deux classifications differentes). Deux personnages ont la meme classification quand les ensembles se recoupent."""
    if Hero.IsType(face) or AlterEgo.IsType(face):
        return {"IdentitySpecific"}
    return {c for c in getattr(face, "card_classes", []) if c != "Aspect"}


def _allie_ou_soutien_persona(face: 'CardFace') -> bool:
    return Ally.IsType(face) or (Support.IsType(face) and face.HasTrait("PERSONA"))


def CartesSacrifiables(joueur: 'Player', cible: 'CardFace') -> List['CardFace']:
    """Les allies et soutiens PERSONA de MEME classification que `cible`, sous le controle du joueur (en jeu) ou dans sa main."""
    voulue = ClassificationDe(cible)
    if not voulue:
        return []
    en_jeu = [f for f in joueur.GetControlCards() if f.IsInPlay() and _allie_ou_soutien_persona(f)]
    en_main = [f for f in joueur.hand_cards.Get() if _allie_ou_soutien_persona(f)]
    return [f for f in en_jeu + en_main if ClassificationDe(f) & voulue]


def EchangerContreUnSacrifice(effect: 'Effect', message: 'Message.WhenUnitWouldAttack') -> None:
    """Interruption forcee commune a Torment et a Death Spiral : si une carte sacrifiable existe, l'attaque est ANNULEE et cette carte est defaussee A SA PLACE (choisie par le joueur attaque)."""
    for cible in list(message.attacked_targets):
        joueur = cible.GetControlBy()
        if joueur is None or not hasattr(joueur, "IsPlayer"):
            continue
        candidates = CartesSacrifiables(joueur, cible)
        if not candidates:
            continue
        choisie = joueur.AskChooseFace(candidates, effect, forced=True)
        if choisie is None:
            choisie = candidates[0]
        message.CancelThisAttack(effect)
        Faces.DiscardAll([choisie], effect)
        return


def CibleAmie(effect: 'Effect', message: 'Message.WhenUnitWouldAttack') -> bool:
    """« attacks a FRIENDLY character » : identite ou allie du joueur."""
    Unused(effect)
    cibles = list(message.attacked_targets)
    return bool(cibles) and all(Hero.IsType(c) or AlterEgo.IsType(c) or Ally.IsType(c) for c in cibles)
