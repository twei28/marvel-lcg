from cards.pack import *
# ===========================================================================
# HELLCAT (jakxin, set 172, prefixe `hc`) — helpers partages du pack.
#
# TOUT le pack tourne autour d'UNE chose : les cartes ACCROCHEES A L'IDENTITE.
# Hellcat accroche a elle-meme les evenements a ressource [mental] qu'elle
# joue (hc001a), Hedy Wolfe en remonte de la defausse (hc011), et six cartes
# les comptent ou les consomment : Empowered (hc001a), Illusion (hc008),
# Mental Episode (hc013), Battle for a Soul (hc014).
#
# COMMENT ON ACCROCHE UN EVENEMENT. Un `Event` n'a pas l'attribut `CanAttach`
# des ameliorations : `AttachTo2` lui est ferme. Le moteur a en revanche une
# zone « cartes glissees sous une carte » (`PlaceCardHere` /
# `GetPlacedCardArea`, modele 01166 Highway Robbery et ze014 The Mother of
# Night), que le plateau DESSINE (etape 8 bis, portePar). On glisse donc les
# cartes FACE VISIBLE sous l'identite : c'est l'accroche du pack.
#
# ⚠ « cards attached to your identity » = les cartes glissees par cette
# mecanique, PAS les ameliorations (Cat Suit, Claws, Mental Training) que le
# moteur attache aussi a l'identite par defaut. Regle officielle : une
# amelioration sans « Attach to » n'est pas un attachement. Arbitrage du
# portage, note dans le releve.
#
# Arbitrages utilisateur du 11/09/2026 (releve dans .planning/todos) :
#  - la Response de Hellcat n'accroche que les EVENEMENTS (notice de l'auteur) ;
#  - Outer Demons donne un VRAI boost a Hellcat (voie ouverte par dd001a) ;
#  - « limit once per turn » d'Iron Man = une fois par round.
# ===========================================================================
HELLCAT = "Hellcat"
PATSY = "Patsy Walker"
MENTAL_POTENTIAL = "Mental Potential"
EMPOWERED = "Empowered"
MAX_ATTACHEES = 3

def IdentiteDe(effect: 'Effect') -> 'Identity|None':
    joueur = effect.GetInitiator()
    return joueur.GetIdentity() if joueur else None

def CartesAttacheesA(identite: 'CardFace') -> List['CardFace']:
    """Les cartes glissees face visible sous l'identite (l'accroche du pack)."""
    return list(identite.GetPlacedCardArea().Get(True))

def AccrocherA(identite: 'CardFace', faces: Sequence['CardFace'], effect: 'Effect') -> bool:
    return identite.PlaceCardHere(list(faces), True, effect)

def PayeSeulementEnMental(effect: 'Effect') -> bool:
    """« If you paid for this using only [mental] resources » : modele dd004."""
    return effect.GetPaidResources().OnlyHasColor("B")

def AMentalImprime(face: 'CardFace') -> bool:
    return FacesCounter.GetPrintedResources([face]).GetColor("B", convert_green_res=False) > 0

def CartesDeLaDefausse(joueur: 'Player') -> List['CardFace']:
    return list(joueur.discard_pile.Get(True))
