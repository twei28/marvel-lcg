from cards.pack import *

# Helpers partages du set « Lady Deathstrike ».
#
# ⚠ Les modules du set font `from . import *` : un helper defini dans le `__init__.py` du PACK leve un NameError avale
# par le moteur (lecon hk005). Tout ce que les cartes appellent vit donc ICI.

ID_SAIGNEMENT = "ld005"
IDS_VILAIN = ["ld001", "ld002", "ld003"]
NOM_GRIFFES = "Reinforced Adamantium Claws"
NOM_COMMANDANT = "Reaver Commander"


def JoueurDeCetteCarte(effect: 'Effect') -> 'Player|None':
    """Le joueur a qui appartient la carte qui agit (jamais `GetInitiator()` en premier : il leve un assert quand
    l'initiateur n'est pas un joueur, et le moteur l'avale)."""
    porteur = getattr(effect, "this", None)
    if porteur is not None:
        controleur = porteur.GetControlByOrOwner()
        if Player.IsType(controleur):
            return controleur
    initiateur = getattr(effect, "initiator", None)
    if initiateur is not None and Player.IsType(initiateur):
        return initiateur
    return None


def LeSaignement(joueur: 'Player|None') -> 'CardFace|None':
    """« The copy of Bleeding Out attached to your identity » : la copie posee sur l'identite de CE joueur, ou None."""
    if joueur is None:
        return None
    identite = joueur.GetIdentity()
    if identite is None:
        return None
    for face in identite.GetInventoryDeck().Get():
        if face.paper.card_id == ID_SAIGNEMENT:
            return face
    return None


def TousLesSaignements(effect: 'Effect') -> List['CardFace']:
    """« Each copy of Bleeding Out in play » : une par joueur, dans l'ordre des joueurs."""
    out: List['CardFace'] = []
    for joueur in Worlds.GetPlayers(effect):
        face = LeSaignement(joueur)
        if face is not None:
            out.append(face)
    return out


def LadyDeathstrike(effect: 'Effect') -> 'CardFace|None':
    """Le vilain Lady Deathstrike EN JEU (par card_id : deux sbires du depot portent le meme nom)."""
    for face in Worlds.GetAllVillains(effect.world):
        if face.paper.card_id in IDS_VILAIN:
            return face
    return None


def EstDuHeros(face: 'CardFace') -> bool:
    """« Identity-specific card » : une carte de classe Hero (signature, sa nemesis n'en fait pas partie)."""
    return hasattr(face, "IsClass") and face.IsClass("IdentitySpecific")


def Saigner(effect: 'Effect', saignement: 'CardFace', joueur: 'Player') -> bool:
    """Le CORPS de la capacite « Special » de Bleeding Out (ld005) :
    place 1 compteur bleed ici, defausse du dessus du deck de `joueur` autant de cartes que de compteurs bleed ici ;
    si une carte specifique a l'identite est defaussee ainsi, prend 1 degat. Rend True si une telle carte a ete defaussee.

    FAQ de l'auteur : les degats sont infliges UNE fois, que l'on defausse une ou plusieurs cartes d'identite : 1 degat au plus."""
    Faces.PlaceCountersOn([saignement], 1, 'bleed', effect)
    n = saignement.GetCounters('bleed')
    cartes = joueur.DiscardDeckTopCards(n, effect) if n > 0 else []
    defausse_heros = any(EstDuHeros(c) for c in cartes)
    if defausse_heros:
        identite = joueur.GetIdentity()
        if identite is not None:
            saignement.DealDamage([identite], 1, effect)
    return defausse_heros


def ResoudreSaignement(effect: 'Effect', joueur: 'Player|None') -> bool:
    """« Resolve the "Special" ability on the copy of Bleeding Out attached to your identity » : passe par le vrai
    `ResolveSpecialAbility` de la carte (capacite `Special` enregistree sur ld005). Rend « une carte specifique a
    l'identite a-t-elle ete defaussee ? » (Reaver Tracker : « If you did not discard an identity-specific card this way »)."""
    saignement = LeSaignement(joueur)
    if saignement is None or joueur is None:
        return False
    saignement.ld_defausse_heros = False
    saignement.ResolveSpecialAbility(joueur, effect)
    return bool(getattr(saignement, "ld_defausse_heros", False))


def ResoudreSurTous(effect: 'Effect') -> None:
    """« Resolve the "Special" ability on each copy of Bleeding Out in play »."""
    for joueur in Worlds.GetPlayers(effect):
        ResoudreSaignement(effect, joueur)
