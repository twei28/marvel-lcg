from . import *

# Reeling — AMELIORATION, cout 0, [physical]. CONDITION. TACTIC. x2.
# Attach to a minion. Max 1 per enemy.
# Attacks against attached minion gain overkill. Increase the amount of excess
#   damage this enemy is dealt by 2.
#
# BRIQUE 6 : une amelioration JOUEUR attachee a un SBIRE.
#
# CARTES DE REFERENCE
#  - `ss012` Mark of Kaine (pack scarlet_spider, auteur Arnaud) : LE MODELE
#    EXACT. « Attacks against this minion gain overkill » =
#    `WhenUnitWouldAttackUnit(None, "AttachedMinion", op)` +
#    `message.GainOverKill(effect)` (modele officiel 33032 Marked) ;
#    « increase that [excess] damage by 2 » =
#    `WhenUnitAttackDealExcessDamage(type, who, op, conditions=[cible = mon
#    hote])` + `message.IncreaseDamage(2, effect)` (modele gmw/16045 Follow
#    Through).
#  - `bk009` Portal / `sf009` Burning : l'amelioration sur un ennemi.
#
# TEXTE CONTRE CODE
#  ⚠ « Attach to a MINION » -> `CanPlayThisUpgradeCard(Minion)`, pas Enemy :
#    jamais sur le vilain (Feint, lui, dit « an enemy »).
#  ⚠ « Max 1 per enemy » -> `desc.MaxPerUnit = "1"`, aucun code.
#  ⚠ « ATTACKS against attached minion gain overkill » -> toute attaque, de
#    n'importe qui (Ares, un allie, un autre joueur) : `attacker=None`. Pas les
#    degats hors attaque (Feint), le mot-cle ne porte que sur les attaques
#    (fiche overkill.md).
#  ⚠ « Increase the amount of EXCESS damage this enemy is dealt by 2 » ->
#    `WhenCalcDealExcessDamage`, message que le moteur n'envoie QUE quand la
#    sante passe sous zero (can_health.py:402-403). A exces nul (coup pile),
#    rien ne part et le +2 ne s'applique pas : meme lecture que Mark of Kaine,
#    ecrite par le meme auteur. Le +2 va au deversement d'overkill ET au
#    compte d'Ares' Battle Helm (ar005), qui lit `excess_damage`.
#  ⚠ Ce sont deux capacites CONSTANTES (aucun mot en gras) : `NonKeyword`
#    pour les deux, jamais un Interrupt optionnel qui poserait une question.
#  ⚠ « this enemy » = le sbire attache, verifie par `Condition.CheckWhichCard(
#    "AttachedMinion", message.target, effect)`, le litteral qu'emploie 33032.


def GetAbilities() -> Sequence['Ability']:

    def deferler(effect: 'Effect', message: 'Message.WhenUnitWouldAttackUnit') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(this)
        message.GainOverKill(effect)

    def vise_mon_hote(effect: 'Effect', message: 'Message.WhenCalcDealExcessDamage') -> bool:
        return Condition.CheckWhichCard("AttachedMinion", message.target, effect)

    def gonfler_lexces(effect: 'Effect', message: 'Message.WhenCalcDealExcessDamage') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(this)
        message.IncreaseDamage(2, effect)

    return [
        AbilityFactory.CanPlayThisUpgradeCard(Minion),
        AbilityFactory.WhenUnitWouldAttackUnit(
            AbilityType.NonKeyword,
            None,
            "AttachedMinion",
            deferler,
        ),
        AbilityFactory.WhenUnitAttackDealExcessDamage(
            AbilityType.NonKeyword,
            None,
            gonfler_lexces,
            conditions=[vise_mon_hote],
        ),
    ]
