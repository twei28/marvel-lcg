from cards.pack import *

# Helpers partages du set « Batgirl Nemesis ». (Les modules font `from . import *` : tout helper vit ICI, lecon hk005.)

def ImprimeAvec(face: 'CardFace', couleur: str) -> bool:
    """La carte porte une ressource IMPRIMEE de cette couleur (`desc.RES`)."""
    return ClassCard.IsType(face) and face.printed_resource.HasColorPrinted(couleur)


def CartesDeLaMain(joueur: 'Player', couleur: str):
    return [f for f in joueur.hand_cards.Get() if ImprimeAvec(f, couleur)]
