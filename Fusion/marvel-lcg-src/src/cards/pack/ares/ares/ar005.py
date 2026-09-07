from . import *

# * Ares' Battle Helm — AMELIORATION, cout 2, [mental]. ARMOR. OLYMPUS. UNIQUE.
# Hero Response: After Ares attacks and defeats an enemy, exhaust Ares' Battle
#   Helm and choose a scheme -> remove 1 threat from that scheme for each point
#   of excess damage dealt to that enemy by that attack.
#
# CARTES DE REFERENCE
#  - `an004` Murderous Glare (pack angela) : `AfterUnitDefeatedUnit(type, "You",
#    Enemy, op, is_from_attack=True).SetTarget(Scheme2, range=(1, 1))` +
#    `RemoveThreatFromSchemes(effect.targets, n, effect)`. « attacks AND
#    defeats » = `is_from_attack=True`, « an ENEMY » = le vilain compte.
#  - `defeated.py:51` : le drapeau `has_excess_damage=True` de la meme
#    fabrique, et `message.excess_damage` (sender_damage.py:947) pour le
#    chiffre.
#
# TEXTE CONTRE CODE
#  ⚠ « After ARES attacks and defeats » -> `"You"` + `is_from_attack=True` : une
#    defaite par un allie, ou par des degats directs (Feint, la brulure d'un
#    autre pack) ne declenche rien.
#  ⚠ « exhaust Ares' Battle Helm AND choose a scheme → » -> les deux sont le
#    COUT : `CostFunc.Exhaust("This")` et le selecteur `Scheme2, range=(1,1)`.
#    Un casque incline ne se propose plus.
#  ⚠ « for each point of EXCESS damage » -> `message.excess_damage`. Avec
#    `has_excess_damage=True`, la Reponse n'est meme pas proposee quand
#    l'exces vaut 0 : rien a retirer, rien a payer. Reeling (ar008) gonfle cet
#    exces de 2, c'est la synergie du pack.
#  ⚠ « from THAT scheme » -> la cible choisie, une seule, en une fois.


def GetAbilities() -> Sequence['Ability']:

    def coup_de_casque(effect: 'Effect', message: 'Message.AfterUnitDefeatedUnit') -> None:
        this = effect.this.CastTo(Upgrade)
        exces = int(getattr(message, "excess_damage", 0) or 0)
        if exces <= 0:
            return
        this.RemoveThreatFromSchemes(effect.targets, exces, effect)

    return [
        AbilityFactory.CanPlayThisUpgradeCard(),
        AbilityFactory.AfterUnitDefeatedUnit(
            AbilityType.HeroResponse,
            "You",
            Enemy,
            coup_de_casque,
            is_from_attack=True,
            has_excess_damage=True,
        ).SetCostFunc(CostFunc.Exhaust("This"))
        .SetTarget(Scheme2, range=(1, 1)),
    ]
