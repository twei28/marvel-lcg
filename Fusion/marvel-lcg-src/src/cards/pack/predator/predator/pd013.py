from . import *

# * Plasmacaster — AMELIORATION, cout 2, [energy]. TECH. WEAPON.
# Hero Action (attack): Exhaust Plasmacaster → deal 2 damage to an enemy (3 damage instead if that enemy has an upgrade
#   attached). This attack gains ranged.
#
# Cartes de reference :
#  - `core/01053` : `hero.DealDamage(effect.targets, n, effect, property=AttackProperty(ranged=True))` ;
#    `CostFunc.Exhaust("This")` ; `.SetLabel('attack')` + `.SetTarget(Enemy)` ; fiche mots-cles/ranged.md.
#  - `GetAttachedUpgrades()` (ares, yd012) : ameliorations posees sur la cible (Infralocked en est une).
#
# ⚠ Mots-pieges :
#  - « 3 damage INSTEAD if that enemy has AN upgrade attached » : 3 au lieu de 2, quelle que soit l'amelioration (Infralocked
#    compte) ; ATTACHEE a l'ennemi, pas posee a cote.
#  - « This attack gains ranged » : ignore la riposte (`ranged=True`) ; ce n'est pas une attaque de BASE (Wrist Blades ne donne rien).
#  - « Exhaust Plasmacaster → » : l'inclinaison est le COUT (payee avant le choix de cible).


def GetAbilities() -> Sequence['Ability']:

    def tir(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(message)
        joueur = JoueurDeCetteCarte(effect)
        if joueur is None or not effect.targets:
            return
        cible = effect.targets[0]
        degats = 3 if list(cible.GetAttachedUpgrades()) else 2
        joueur.GetHero().DealDamage(effect.targets, degats, effect, property=AttackProperty(ranged=True))
        Unused(this)

    return [
        AbilityFactory.CanPlayThisUpgradeCard(),
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            tir,
        ).SetLabel('attack').SetCostFunc(CostFunc.Exhaust("This")).SetTarget(Enemy),
    ]
