from cards.pack import *

# ===========================================================================
# Set modulaire KREE-SKRULL WAR (Skrull Menace, Kajislav) — sk136-sk140.
# Livre avec le scenario Super-Skrull (livret p. 10), jouable avec n'importe quel
# mechant. Set « Kree-Skrull War » : Bel-Dann et Raksor s'appellent l'un l'autre ;
# Earth Involvement (complot annexe PERMANENT + SETUP) commence la partie en jeu
# et ne peut pas la quitter ; chaque carte du set revelee y ajoute de la menace.
# ===========================================================================

NOM_SET = "Kree-Skrull War"
NOM_COMPLOT = "Earth Involvement"


def AppartientAuSet(face: 'CardFace') -> bool:
    """« A card that belongs to the Kree-Skrull War encounter set »."""
    return face.paper.set_name == NOM_SET


def EarthInvolvementEnJeu(effect: 'Effect') -> 'CardFace|None':
    return Worlds.FindCardOnField(effect, name=NOM_COMPLOT, card_type=SchemeSide2)


def PlacerMenaceSurEarthInvolvement(effect: 'Effect', source: 'CardFace', valeur: int) -> None:
    """« Place N threat on Earth Involvement. » Carte absente (retiree par une
    personnalisation de scenario) : rien."""
    complot = EarthInvolvementEnJeu(effect)
    if complot is not None and valeur > 0:
        source.PlaceThreatOnSchemes([complot], valeur, effect)


def MettreEnJeuEngage(effect: 'Effect', joueur: 'Player', nom: str) -> 'CardFace|None':
    """« Search the encounter deck and discard pile for <nom> and put him into
    play engaged with you. » Le sbire est MIS EN JEU (aucun When Revealed ne part :
    Bel-Dann et Raksor ne se rappellent donc pas en boucle). La recherche melange
    le deck rencontre (natif)."""
    face = Search.EncounterCard(effect, joueur, include_discard_pile=True, name=nom, card_type=Minion)
    if face is not None:
        face.PutIntoPlay(joueur, effect)
    return face
