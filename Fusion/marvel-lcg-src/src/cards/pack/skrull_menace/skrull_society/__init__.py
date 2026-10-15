from cards.pack import *

# ===========================================================================
# Set modulaire SKRULL SOCIETY (Skrull Menace, Kajislav) — sk107-112.
# Livre avec le scenario Skrull Empire, mais jouable avec n'importe quel
# mechant : « heal the villain » doit donc marcher dans les deux cas.
# ===========================================================================


def SoignerLeMechantPartout(effect: 'Effect', valeur: int) -> int:
    """« Heal X damage from the villain ». Scenario Skrull Empire (un
    environnement porte le cadran de PV) : c'est lui qu'on soigne. Ailleurs :
    le mechant, normalement."""
    from cards.pack.skrull_menace.skrull_empire import EnvironnementEnJeu, SoignerLeMechant
    if EnvironnementEnJeu(effect) is not None:
        return SoignerLeMechant(effect, effect.this, valeur)
    mechant = Worlds.FindVillain(effect)
    if mechant is None or valeur <= 0:
        return 0
    avant = mechant.GetCounters('damage')
    mechant.HealHealth(valeur, effect)
    return max(0, avant - mechant.GetCounters('damage'))


def EnnemisSkrullEnJeu(effect: 'Effect') -> List['CardFace']:
    return [f for f in Worlds.GetOnFieldCards(effect)
            if Enemy.IsType(f) and f.IsInPlay() and f.HasTrait("SKRULL")]
