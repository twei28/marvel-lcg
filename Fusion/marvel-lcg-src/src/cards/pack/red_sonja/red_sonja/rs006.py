from . import *

# Hyrkanian Fury — evenement signature, x1 (8/15). ATTACK. Cout 2, ressource
# [R].
# Hero Action (attack): Deal 4 damage to an enemy. If you used your
# "She-Devil" ability to reduce the cost of this card, stun that enemy.
#
# CARTE DE REFERENCE : `01031` Repulsor Blast (montage attaque d'evenement).
# `AUtiliseSheDevil` (`__init__.py` de ce dossier) lit le marqueur pose par
# `rs001a` (She-Devil) sur CETTE carte pendant sa propre resolution -- voir
# ce fichier pour le detail du mecanisme et sa reserve de verification.

def GetAbilities() -> Sequence['Ability']:

    def hyrkanian_fury(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(message)

        this.DealDamage(effect.targets, 4, effect)
        if AUtiliseSheDevil(this):
            Faces.GiveStatus(effect.targets, "Stunned", effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            hyrkanian_fury,
        ).SetPlay().SetLabel('attack')
        .SetTarget(Enemy),
    ]
