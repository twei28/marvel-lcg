from . import *

# Position du vilain (environnement recto-verso : The Streets Below / Atop the Tenshu). VILLAIN POSITION.
# Positions identiques : chaque personnage gagne +1 ATK. Positions differentes : -1 degat par attaque, menace non retirable du complot principal.
# Les deux faces portent le MEME texte : abilites partagees (AbilitesPositionVilain).
# Cartes de reference : hood/streets_of_mayhem/24060 (+1 ATK a tous), aos/supersonic/50159 (-N degats par attaque), mojo/spiral/39012a (menace non retirable).
# ⚠ Mots-pieges : « each character » = heros ET allies ET sbires ET vilain (« Character ») ; « from each attack » (pas les degats d'une carte) ; sl004 a les MEMES NOMS de faces.


def GetAbilities() -> Sequence['Ability']:
    return AbilitesPositionVilain()
