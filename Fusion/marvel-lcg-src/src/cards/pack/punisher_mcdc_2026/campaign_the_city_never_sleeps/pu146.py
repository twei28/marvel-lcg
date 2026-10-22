from . import *

# * Punisher (Frank Castle) — ALLIE de campagne (gagne au combat 3, mis en jeu au combat 4, p275). Agressivite, cout 3, THW 1, ATK 2, PV 3. SOLDIER. VIGILANTE.
# ★ Punisher's attacks gain piercing and ranged.
# Response : After Punisher attacks and defeats a minion, deal 2 damage to an enemy.
#
# Cartes de reference : determination/dt026 (* The Punisher : `UnitAttackGainKeyword("This", piercing=True, ranged=True)`, MEME texte sur un autre
# allie), core/01051 Tigra (`AfterUnitAttackAndDefeatUnit(Response, "This", Minion, ...)`), sm/27024 (`this.DealDamage(effect.targets, 2, effect)` +
# `.SetTarget(Enemy)`).
# ⚠ Mots-pieges : « attacks AND defeats a minion » (pas « defeats ») : `AfterUnitAttackAndDefeatUnit` ; « a MINION » (pas un ennemi : le vilain ne
# declenche pas) ; « deal 2 damage to AN ENEMY » : n'importe quel ennemi, le sbire vaincu n'est plus en jeu ; ce sont des degats d'effet, pas une
# attaque (pas de piercing/ranged, pas de defense) ; ★ de la ligne 1 = « Punisher's attacks » : SES attaques seulement.

def GetAbilities() -> Sequence['Ability']:

    def deux_degats(effect: 'Effect', message: 'Message.AfterUnitDefeatedUnit') -> None:
        Unused(message)
        effect.this.CastTo(Ally).DealDamage(effect.targets, 2, effect)

    return [
        AbilityFactory.UnitAttackGainKeyword("This", piercing=True, ranged=True),
        AbilityFactory.AfterUnitAttackAndDefeatUnit(AbilityType.Response, "This", Minion, deux_degats).SetTarget(Enemy),
    ]
