from . import *
from .jigsaw_commun import TrouverJigsaw as Jigsaw

# Cut to Pieces — TRAITRISE x2. Boost 0★.
# When Revealed : Jigsaw activates against you. If this activation is an attack, he gets +1 ATK.
# ★ Boost : Place 1 threat on the main scheme and heal 1 damage from Jigsaw.
#
# Cartes de reference : `galactic_storm/hala_ultimatum/gs155.py` (`villain.DoActivate(joueur,
# effect)`, modele OFFICIEL 11051), `mut_gen/brawler/32177.py` (`would_message.GainAttackForThisAttack`),
# `sm/sinister_six/27100a.py` (`PlaceThreatOnSchemes`), `night_thrasher/nt008.py` (`HealthUnits`).
#
# ⚠ « Jigsaw activates against YOU » : le joueur qui revele ; « If this activation IS AN ATTACK » : +1 ATK
# seulement si l'activation est une attaque (un heros), pas une manigance (alter ego) ; « heal 1 damage FROM Jigsaw ».

def GetAbilities() -> Sequence['Ability']:

    def revele(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        joueur = message.GetToPlayer()
        jigsaw = Jigsaw(effect)
        if jigsaw is None or joueur is None:
            return

        def plus_un(activation: 'Message.WhenEnemyActivateAgainstYou') -> None:
            voulu = activation.would_message
            if isinstance(voulu, Message.WhenUnitWouldAttack):
                jigsaw.GainForThisActive(effect, voulu, attack=1)

        jigsaw.DoActivate(joueur, effect, plus_un)

    def boost(effect: 'Effect', message: 'Message.WhenCardBecomeBoost') -> None:
        this = effect.this
        schemes = Worlds.GetMainSchemes(effect)
        if schemes:
            this.PlaceThreatOnSchemes(schemes[:1], 1, effect)
        jigsaw = Jigsaw(effect)
        if jigsaw is not None:
            jigsaw.HealHealth(1, effect)

    return [
        AbilityFactory.WhenThisRevealed(None, revele),
        AbilityFactory.WhenCardBecomeBoost("This", boost),
    ]
