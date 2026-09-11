from cards.pack import *
from cards.pack.hellcat.hellcat import *
# ===========================================================================
# Set nemesis de Hellcat (jakxin) : DEUX sbires nemesis, Blackheart et Daimon
# Hellstrom, qui ne peuvent pas partager une zone de jeu.
#
# Insert de l'auteur : « In multiplayer games, Patsy would engage with one of
# the two minions, and the next player in line would get the other. In single
# player, you would engage your choice of nemesis minion, then the other would
# gain surge since it could not enter play. » Le texte des cartes le rend tel
# quel : « engages with the next player in turn order. If he cannot, this
# card gains surge » — en solo le joueur suivant est soi-meme, donc « cannot ».
# ===========================================================================
BLACKHEART = "Blackheart"
DAIMON = "Daimon Hellstrom"

def AutreDemon(effect: 'Effect', nom_de_l_autre: str) -> 'Minion|None':
    for face in Worlds.GetOnFieldCards(effect):
        if Minion.IsType(face) and face.IsName(nom_de_l_autre):
            return face
    return None

def RevelationDUnDemon(effect: 'Effect', message: 'Message.WhenCardRevealed', nom_de_l_autre: str) -> None:
    """When Revealed commun : si l'autre demon est engage avec moi, ce sbire
    va au joueur suivant ; s'il n'y en a pas (solo), il gagne surge et ne
    reste pas en jeu."""
    this = effect.this.CastTo(Minion)
    joueur = message.GetToPlayer()
    autre = AutreDemon(effect, nom_de_l_autre)
    if autre is None or autre.GetEngagedPlayer() is not joueur:
        return
    suivant = Worlds.GetNextPlayer(joueur, effect) if Worlds.GetPlayerNum(effect) > 1 else None
    if suivant is not None and suivant is not joueur:
        this.EngagePlayer(suivant, effect)
        return
    ThisCardGainSurge(effect, message)
    Faces.DiscardAll([this], effect)
