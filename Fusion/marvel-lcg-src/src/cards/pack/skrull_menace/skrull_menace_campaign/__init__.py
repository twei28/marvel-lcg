from cards.pack.skrull_menace.communs_modulaires import *

# ===========================================================================
# CARTES DE CAMPAGNE de Skrull Menace (Kajislav) — sk263-sk289b, set « Skrull Menace Campaign »
# (dossier = FileManager.CleanName du set_name).
#
# Sept allies, sept complots annexes de JOUEUR, six soutiens, six ameliorations, le rappel
# « Cooperation Progress Reminder » (type Insert, rien a scripter) et deux gabarits techniques :
#   - `skrull_war_minion` : la forme SBIRE de sk268 Chilly McHotpants (TreatAsMinion) ;
#   - `skrull_fickle_ally` : la forme ALLIEE d'un sbire repris par sk272 Fickle Alliance (TreatAsAlly).
# Ces cartes sont de classe « Campaign » : elles n'entrent dans un deck que par la Cooperation Area
# (mode campagne, autre bloc). Ici, les CARTES et leurs capacites, jouables en partie normale.
# ===========================================================================

# `TreatAsMinion` est une fonction de module (treat.py), pas une methode d'AbilityFactory : le
# `import *` de cards/pack/__init__.py ne la reexporte pas (meme remarque que skrull_elite_skymax).
from game.ability.factory.treat import TreatAsMinion

# « You may spend X resources ... If you cannot » (sk288 Sy-Torak Gem) : meme helper que 60127 Tug of War.
from cards.pack.fne import PeutCouvrirLeCout  # noqa: F401

# « a TREACHERY card » : meme notion que Lyja / Paibok (decision utilisateur du 15/10/2026 : TOUTE
# carte de type Treachery OU portant le trait TREACHERY).
from cards.pack.skrull_menace.lyja import EstTraitrise, FinderTraitrise  # noqa: F401

GABARIT_SBIRE_WAR_SKRULL = "Chilly McHotpants Minion"
GABARIT_ALLIE_FICKLE = "Fickle Ally"


def LesAlliesSkrull(joueur: 'Player') -> List['CardFace']:
    """« a SKRULL ally » que le joueur controle."""
    return [a for a in joueur.GetControlAllies() if a.HasTrait("SKRULL")]


def MettreSousLeControle(effect: 'Effect', face: 'CardFace', joueur: 'Player') -> None:
    """Pose `face` (un sbire cherche dans le deck rencontre) sous le controle de `joueur`."""
    face.PutIntoPlay(joueur, effect, under_control=True)
