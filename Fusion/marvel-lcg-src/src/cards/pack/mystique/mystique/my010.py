from . import *

# Quick and Dirty (Execution) (x3) : EVENEMENT (ATTACK. SHAPESHIFTER.), cout 2, [physical].
# Hero Action (attack): Deal 4 damage to an enemy. If the Enemy shapeshift form upgrade is faceup, this attack deals 2 additional damage and gains overkill.
#
# CARTES DE REFERENCE
#  - `bs010` Beastly Charge / `01053` Relentless Assault : `hero.DealDamage(cibles, n, effect, property=AttackProperty(overkill=..))` + `.SetPlay().SetLabel('attack').SetTarget(Enemy)` (fiche `overkill.md`).
#
# TEXTE CONTRE CODE
#  « Deal 4 damage » : 4 (une ATTAQUE du heros, donc Defense/Tenace/Perce s'appliquent). « If the ENEMY form is FACEUP » : la forme my004 face `a` ; sinon 4 degats sans overkill. « 2 ADDITIONAL damage AND gains
#    overkill » : 6 degats ET overkill, ensemble ou pas du tout.
#  Chiffres : cout 2, 4 degats, +2.


def GetAbilities() -> Sequence['Ability']:

    def quick_and_dirty(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        Unused(message)
        joueur = effect.GetInitiator()
        visible = FormeVisible(joueur, ID_ENEMY)
        joueur.GetHero().DealDamage(effect.targets, 4 + (2 if visible else 0), effect, property=AttackProperty(overkill=visible))

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            quick_and_dirty,
        ).SetPlay().SetLabel('attack')
        .SetTarget(Enemy),
    ]
