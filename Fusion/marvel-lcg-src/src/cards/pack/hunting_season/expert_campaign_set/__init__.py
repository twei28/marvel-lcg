from cards.pack import *


def PeutPayerEnergie(joueur: 'Player') -> bool:
    """La branche « depense une ressource [energy] » n'est offerte que payable
    (meme regle que `PeutPayer` du set Trap : sinon le joueur la choisit, le
    paiement echoue et la carte ne fait rien)."""
    from cards.pack.hunting_season.trap import PeutPayer
    return PeutPayer(joueur, "Y")
