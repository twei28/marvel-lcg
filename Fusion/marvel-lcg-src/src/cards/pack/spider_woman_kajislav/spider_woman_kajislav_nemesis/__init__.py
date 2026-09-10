from cards.pack import *
from cards.pack.spider_woman_kajislav.spider_woman_kajislav import *

# `TreatAsMinion` est une FONCTION DE MODULE, pas une methode d'AbilityFactory :
# le `from game.ability.factory import *` de cards/pack/__init__.py ne la
# reexporte pas. Import explicite obligatoire, comme dans le set nemesis
# d'Agent Anti-Venom.
from game.ability.factory.treat import TreatAsMinion
