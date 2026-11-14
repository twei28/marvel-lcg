from . import *
# Critical Blow (Aggression, evenement 3 [energy]). ATTACK. THWART. Requirement ([energy][mental][physical]).
# Hero Action (attack/thwart): Deal 4 damage to an enemy. Remove threat from a scheme equal to the damage dealt this way. This attack
# gains piercing.
#
# Cartes de reference : gam/18020 Hit and Run (« deal N damage to an enemy, remove N threat from a scheme » : `SetTarget(Enemy)` +
# `SetTarget2(Scheme2)`, label 'attack','thwart') ; night_thrasher/nt006 (`this.DealDamage(.., property=AttackProperty(piercing=True))`) ;
# fiche requirement.md (`desc.Requirement "YBR"`, base automatique : aucun script).
# « threat equal to the DAMAGE DEALT this way » : le total rendu par `DealDamage` (un ennemi qui encaisse 0 -> 0 menace retiree).
# « This attack gains piercing » : le perforant defausse la Tenacite de la cible avant les degats (RR « Piercing »).
def GetAbilities() -> Sequence['Ability']:
    def critical_blow(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(message)
        infliges = this.DealDamage(effect.targets, 4, effect, property=AttackProperty(piercing=True))
        if infliges:
            this.RemoveThreatFromSchemes(effect.targets2, infliges, effect)
    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            critical_blow,
        ).SetPlay().SetLabel('attack', 'thwart')
        .SetTarget(Enemy)
        .SetTarget2(Scheme2),
    ]
