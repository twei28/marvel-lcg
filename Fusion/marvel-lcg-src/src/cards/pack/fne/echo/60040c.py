from . import *

# Photographic Reflexes (variante C) — meme texte que les deux autres,
# seule l'icone de ressource change. Tout le module est en commun :
# `AbilitesPhotographicReflexes` dans le `__init__.py` du set.
def GetAbilities() -> Sequence['Ability']:
    return list(AbilitesPhotographicReflexes())
