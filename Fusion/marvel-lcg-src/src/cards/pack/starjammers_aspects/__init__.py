from cards.pack import *

# ===========================================================================
# Pack STARJAMMERS ASPECTS : les 50 cartes d'aspect et Basic des Starjammers (Phenexian et Mysteltainn), prefixe `sy`, set
# « Starjammers Aspects » (233). Pack PLAT (un module par carte : `sy001.py` ... `sy050.py`), comme les packs d'aspect TMNT.
# Numerotation : numero imprime (77-126) moins 76 ; table et transcription dans docs/packs/starjammers-aspects/.
#
# ⚠ Les modules font `from . import *` : tout helper que les cartes appellent vit ICI (un NameError dans un helper est AVALE
# par le moteur et la capacite « ne part jamais » : lecon hk005).
# ===========================================================================


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


def IdentiteDe(effect: 'Effect') -> 'CardFace|None':
    joueur = JoueurDe(effect)
    return joueur.GetIdentity() if joueur is not None else None


def Glissees(face: 'CardFace|None') -> List['CardFace']:
    """Les cartes glissees sous `face` (zone `PlaceCardArea`, hors jeu)."""
    if face is None:
        return []
    return list(face.GetPlacedCardArea().Get())


def Ennemis(effect: 'Effect') -> List['CardFace']:
    return [f for f in Worlds.FindCardsOnField(effect, card_type=Enemy) if f.IsInPlay()]


def NbIcones(face: 'CardFace') -> int:
    """« each icon ([star] and [boost]) in that card's boost area » : etoile ET icones de boost (RECETTES §3 : `CountTotalBoostIcons`
    ne compte PAS l'etoile, seule `CountTotalBoostStarAndBoost` additionne les deux)."""
    return FacesCounter.CountTotalBoostStarAndBoost([face])


def CoutImprudent(effect: 'Effect', this: 'CardFace') -> bool:
    """Le cout des quatre cartes « Reckless » : « Discard the top card of the encounter deck. Deal 1 damage to your identity for each icon
    ([star] and [boost]) in that card's boost area → <effet> ». Tout ce qui precede la fleche est le COUT : RR « Cost » (« If taking damage
    is a cost, that cost is not considered paid unless ALL of that damage was taken ») : une prevention, meme partielle, annule l'effet
    (le degat subi reste subi), comme us004 Reckless. Rend True si le cout est PAYE.
    Le nombre d'icones se lit sur la carte DEFAUSSEE (`printed_boost` + etoile : `CountTotalBoostStarAndBoost`)."""
    joueur = effect.GetInitiator()
    if joueur is None:
        return False
    faces = Worlds.DiscardEncounterCards(1, effect)
    n = sum(NbIcones(f) for f in faces)
    if n <= 0:
        return True
    identite = joueur.GetIdentity()
    resultat = identite.TakeDamage(this, n, effect)
    return resultat is not None and getattr(resultat, "took_damage", 0) >= n


def BonusAuPouvoir(puissance: str) -> dict:
    """« gets +1 to THAT basic power » : l'argument `GainUntilPhaseEnd` qui correspond au pouvoir de base utilise (`message.power`)."""
    return {"ATK": {"attack": 1}, "THW": {"thwart": 1}, "DEF": {"defense": 1}, "REC": {"recover": 1}, "SCH": {"scheme": 1}}.get(puissance, {})
