from . import *

# * Mister Fish (CRIMINAL, MAGGIA)
# [star] Mister Fish's attacks gain piercing and ranged.
# When Revealed: Mister Fish engages the player whose identity has the fewest
#   remaining hit points.
#
# Modeles : 04027 Crossfire (UnitAttackGainKeyword), 45135 Armored Unibike
# (EngagePlayer). PlayerFinder ne sait pas trier par PV : on choisit a la main.

def GetAbilities() -> Sequence['Ability']:

    def revele(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Minion)
        joueurs = [j for j in effect.world.const_players if j.GetIdentity() is not None]
        if not joueurs:
            return
        cible = min(joueurs, key=lambda j: j.GetIdentity().health)
        this.EngagePlayer(cible, effect)

    return [
        AbilityFactory.UnitAttackGainKeyword(
            "This",
            piercing=True,
            ranged=True,
        ),
        AbilityFactory.WhenThisRevealed(None, revele),
    ]
