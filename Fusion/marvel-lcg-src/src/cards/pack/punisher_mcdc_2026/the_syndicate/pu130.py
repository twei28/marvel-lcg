from . import *

# * Trapstr — SBIRE UNIQUE. CRIMINAL. SYNDICATE. SCH 1, ATQ 2★, 3 PV, Boost 1, Quickstrike 1.
# Quickstrike.
# ★ Forced Interrupt : When Trapstr attacks you, stun a character you control.
# When Defeated : voir __init__.py.
#
# Cartes de reference : jigsaw/pu059.py (`WhenUnitWouldAttack(ForcedInterrupt, "This", ...)`), skrull_menace/paibok
# (`AuChoixDuJoueur`, repris dans `commun.py`). Quickstrike : natif.
# ⚠ « When Trapstr attacks YOU » : l'attaque contre un JOUEUR (pas un allie) ; « stun a character you control » :
# au choix du joueur, identite ou allie qui peut etre etourdi ; l'attaque a lieu ensuite normalement.

def GetAbilities() -> Sequence['Ability']:

    def etourdir(effect: 'Effect', message: 'Message.WhenUnitWouldAttack') -> None:
        joueur = effect.this.CastTo(Minion).GetEngagedPlayer()
        if joueur is None:
            return
        AuChoixDuJoueur(effect, joueur, lambda cibles: Faces.GiveStatus(cibles, "Stunned", effect), canbe_stunned=True)

    return [
        AbilityFactory.WhenUnitWouldAttack(AbilityType.ForcedInterrupt, "This", etourdir),
        DefaiteSyndicate(),
    ]
