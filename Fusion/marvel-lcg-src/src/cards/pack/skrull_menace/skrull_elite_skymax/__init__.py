from cards.pack.skrull_menace.communs_modulaires import *

# `TreatAsMinion` est une fonction de module, pas une methode d'AbilityFactory : le `import *` de
# cards/pack/__init__.py ne la reexporte PAS (meme remarque que agent_anti_venom_nemesis/__init__.py).
from game.ability.factory.treat import TreatAsMinion

# ===========================================================================
# Ensemble d'ELITE « SKRULL ELITE - SKYMAX » (Skrull Menace, Kajislav) — sk241-sk244.
# Six cartes : le sbire * Skymax, deux Changing Appearance, le complot annexe Surprising Alliance et
# deux Shape Alteration. Dossier du set : `FileManager.CleanName("Skrull Elite - Skymax")` =
# `skrull_elite_skymax`.
# ===========================================================================

GABARIT_SBIRE = "Minion"
