from cards.pack import *
# Helpers partages du set « Smasher » (Phenexian, prefixe `sz`).
#
# ⚠ Les modules du set font `from . import *` : un helper defini dans le `__init__.py` du PACK leve un NameError avale par
# le moteur (lecon hk005). Tout ce que les cartes appellent vit donc ICI.
TRAIT_EXOSPEX = "EXOSPEX"
TRAIT_AERIAL = "AERIAL"


def JoueurDe(effect: 'Effect') -> 'Player|None':
    """Le joueur a qui appartient la carte qui agit (ou son initiateur)."""
    porteur = getattr(effect, "this", None)
    if porteur is not None:
        controleur = porteur.GetControlByOrOwner()
        if Player.IsType(controleur):
            return controleur
    initiateur = getattr(effect, "initiator", None)
    if initiateur is not None and Player.IsType(initiateur):
        return initiateur
    return None


def ExospexEnJeu(joueur: 'Player|None') -> List['CardFace']:
    """« an EXOSPEX upgrade you control » : chaque amelioration EXOSPEX en jeu sous le controle du joueur."""
    if joueur is None:
        return []
    return [f for f in joueur.GetControlCardsByType(upgrade=True) if f.IsInPlay() and f.HasTrait(TRAIT_EXOSPEX)]


def IdentiteAerienneUI(effect: 'Effect', ui: List['CardFace']) -> int:
    """« has toughness if your identity has the AERIAL trait » (modele 49035 Bling!) : 1 si l'identite du joueur est AERIAL."""
    joueur = JoueurDe(effect)
    if joueur is None:
        return 0
    identite = joueur.GetIdentity()
    if identite is not None and identite.HasTrait(TRAIT_AERIAL):
        ui.append(identite)
        return 1
    return 0


# ------------------------------------------------------------------------------------------------------------------
# Les cinq « Hero Response » des ameliorations EXOSPEX. Chaque amelioration les joue par SA capacite (« After you play X »,
# cible choisie par le moteur) ; Accessing les REJOUE depuis le jeu (« Resolve the "Hero Response" ability on an EXOSPEX upgrade
# you control »), ce que le moteur ne sait pas faire pour une Response : on appelle donc les memes fonctions.
# ------------------------------------------------------------------------------------------------------------------
def ReponsePentaVision(effect: 'Effect', cibles: Sequence['CardFace']) -> None:
    """« deal 3 damage to an enemy » : Hero Response ETIQUETEE (attack) = une attaque de l'identite (RR « Labeled Ability »).
    `AttackDamage` (attack_in_event) et non `DealDamage` : resolue par Accessing (`effect.this` = Accessing, dont l'etiquette n'est pas
    `attack`), la Response ne passait pas pour une attaque (le Sonne, Retaliate, « after you attack » l'ignoraient). Corrige le 26/10/2026."""
    effect.this.AttackDamage(cibles, 3, effect)


def ReponseHyperStrength(effect: 'Effect', cibles: Sequence['CardFace']) -> None:
    """« stun an enemy »."""
    Faces.GiveStatus(cibles, "Stunned", effect)


def ReponseHyperSpeed(effect: 'Effect', joueur: 'Player|None') -> None:
    """« ready Smasher »."""
    if joueur is not None and joueur.GetIdentity() is not None:
        Faces.ReadyAll([joueur.GetIdentity()], effect)


def ReponseSuperResistance(effect: 'Effect', joueur: 'Player|None') -> None:
    """« give Smasher a tough status card »."""
    if joueur is not None and joueur.GetIdentity() is not None:
        Faces.GiveStatus([joueur.GetIdentity()], "Tough", effect)


def ReponseExoFlight(effect: 'Effect', cibles: Sequence['CardFace']) -> None:
    """« remove 3 threat from a scheme »."""
    effect.this.RemoveThreatFromSchemes(cibles, 3, effect)


def ChoisirUne(joueur: 'Player', candidats: Sequence['CardFace'], effect: 'Effect', prompt: str) -> 'CardFace|None':
    if not candidats:
        return None
    if len(candidats) == 1:
        return candidats[0]
    return joueur.AskChooseFace(list(candidats), effect, prompt=prompt, forced=True)


def ResoudreLaReponseDe(face: 'CardFace', joueur: 'Player', effect: 'Effect') -> None:
    """Accessing : resout la « Hero Response » de l'amelioration EXOSPEX `face`, en choisissant elle-meme la cible."""
    identifiant = getattr(face.paper, "card_id", None)
    if identifiant == "sz005":
        cible = ChoisirUne(joueur, Worlds.GetOnFieldEnemies(effect), effect, "Penta-Vision : deal 3 damage to an enemy")
        if cible is not None:
            ReponsePentaVision(effect, [cible])
    elif identifiant == "sz006":
        cible = ChoisirUne(joueur, Worlds.GetOnFieldEnemies(effect), effect, "Hyper-Strength : stun an enemy")
        if cible is not None:
            ReponseHyperStrength(effect, [cible])
    elif identifiant == "sz007":
        ReponseHyperSpeed(effect, joueur)
    elif identifiant == "sz008":
        ReponseSuperResistance(effect, joueur)
    elif identifiant == "sz009":
        cible = ChoisirUne(joueur, Worlds.GetOnFieldSchemes(effect), effect, "Exo-Flight : remove 3 threat from a scheme")
        if cible is not None:
            ReponseExoFlight(effect, [cible])
