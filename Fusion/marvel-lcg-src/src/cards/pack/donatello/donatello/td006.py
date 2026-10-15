from . import *

# Singularity — EVENEMENT, cout 4, [mental]. ATTACK.
# Play only if you control the Anti-Gravity Gauntlet upgrade.
# Hero Action (attack): Deal 10 damage to an enemy. This attack gains
#   overkill, piercing, and ranged.
#
# CARTES DE REFERENCE
#  - `16036` Particle Cannon : `hero.DealDamage(effect.targets, n, effect,
#    property=AttackProperty(overkill=True, ranged=True))`.
#  - `04009` Vibranium Arrow : evenement d'ATTAQUE, `hero.DealDamage(...,
#    property=AttackProperty(piercing=True))`, `SetPlay().SetLabel('attack')
#    .SetTarget(Enemy)`.
#  - `bw024` / `wc017` : « play only if you control X » = une CONDITION sur la
#    fabrique, pas `SetPlay(only_if_you_control_face=...)` (cette clause ne
#    regarde que l'inventaire de l'identite). On passe par `IsControl`.
#
# TEXTE CONTRE CODE
#  « control the Anti-Gravity Gauntlet UPGRADE » -> `player.IsControl(
#    CardFinder(card_ids=[td009], card_type=Upgrade))`.
#  « Deal 10 damage ... This attack gains overkill, piercing, AND ranged » ->
#    les TROIS dans `AttackProperty` (c'est une attaque du heros : le
#    Gauntlet td009 « +3 aux evenements ATTACK » s'y applique).
#  « Play only if » = condition de JEU : l'evenement n'est pas offert sans
#    Gauntlet, au lieu d'etre joue puis sans effet.


def GetAbilities() -> Sequence['Ability']:

    def controle_le_gantelet(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> bool:
        Unused(message)
        joueur = effect.GetInitiator()
        if joueur is None:
            return False
        return joueur.IsControl(CardFinder(card_ids=[ID_GANTELET], card_type=Upgrade))

    def singularite(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(this, message)
        joueur = effect.GetInitiator()
        heros = joueur.GetHero()
        heros.DealDamage(
            effect.targets, 10, effect,
            property=AttackProperty(overkill=True, piercing=True, ranged=True))

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            singularite,
            conditions=[controle_le_gantelet],
        ).SetPlay().SetLabel('attack')
        .SetTarget(Enemy),
    ]
