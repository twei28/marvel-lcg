from . import *

# Pointy End (x2) — EVENEMENT (ATTACK), cout 3, [physical].
# Hero Action (attack): Exhaust Mr. Pointy → deal 8 damage to an enemy. This attack gains overkill.
#
# CARTES DE REFERENCE
#  - `01053` Relentless Assault : `hero.DealDamage(.., property=AttackProperty(overkill=..))` pour « this attack gains overkill ».
#  - `mv005` Shield Block : `CostFunc.Exhaust(card_type=Upgrade, name=.., from_where=["YouControlCards"])` pour incliner une carte NOMMEE.
#
# TEXTE CONTRE CODE
#  « Exhaust Mr. Pointy » -> cout : incliner Mr. Pointy (bf014) que VOUS controlez ; sans lui (ou deja incline) la carte n'est pas jouable.
#  « an enemy » -> `Enemy`. « 8 damage » -> 8. « This attack gains overkill » -> `overkill=True` (l'exces va a un allie du joueur
#    engage, non teste ici : seul l'effet principal est mesure).


def GetAbilities() -> Sequence['Ability']:

    def pointy_end(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(this, message)
        hero = effect.GetInitiator().GetHero()
        hero.DealDamage(effect.targets, 8, effect, property=AttackProperty(overkill=True))

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            pointy_end,
        ).SetPlay().SetLabel('attack')
        .SetTarget(Enemy)
        .SetCostFunc(CostFunc.Exhaust(card_type=Upgrade, name=NOM_MR_POINTY, from_where=["YouControlCards"])),
    ]
