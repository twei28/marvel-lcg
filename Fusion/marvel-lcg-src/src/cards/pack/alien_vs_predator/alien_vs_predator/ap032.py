from . import *

# Swarm Breaker — MANIGANCE ANNEXE. Menace 4 (fixe). Boost 2. Acceleration, Hazard.
# Hinder 1[per_hero]. Victory 0.
# When Defeated: Deal 2[per_hero] damage to each enemy.
#
# Cartes de reference : Hinder, Victory, Acceleration, Hazard : `desc`, natifs (fiches) ; « When Defeated » d'une manigance :
#   `WhenSchemeBeDefeated(WhenDefeated, "This")` (tk Bumbling Buffoons) ; « each enemy » : `Worlds.GetOnFieldEnemies`.
#
# ⚠ Mots-pieges : « EACH enemy » : les mechants ET tous les sbires ; 2[per_hero] = 2 x joueurs.


def GetAbilities() -> Sequence['Ability']:

    def vaincue(effect: 'Effect', message: 'Message.WhenSchemeBeDefeated') -> None:
        Unused(message)
        ennemis = list(Worlds.GetOnFieldEnemies(effect))
        if ennemis:
            effect.this.DealDamage(ennemis, 2 * NombreDeJoueurs(effect), effect)

    return [
        AbilityFactory.WhenSchemeBeDefeated(AbilityType.WhenDefeated, "This", vaincue),
    ]
