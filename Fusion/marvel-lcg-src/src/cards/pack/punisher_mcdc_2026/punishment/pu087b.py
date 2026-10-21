from . import *
from .commun_vilain import ReponseDeHeros

# * Punisher (pu087b) : voir pu086a.py (Reponse de heros), `commun_vilain.py`. Steady, Toughness : natifs.

def GetAbilities() -> Sequence['Ability']:
    return [ReponseDeHeros(meme_type=True, carte_de_boost=True)]
