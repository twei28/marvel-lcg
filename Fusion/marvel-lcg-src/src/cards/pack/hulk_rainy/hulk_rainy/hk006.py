from . import *

# Reckless Charge — evenement signature, x2 (n/15 = 8 et 9).
# ATTACK. SUPERPOWER. Cout 1, ressource [physical].
# Hero Action (attack): Deal 1 damage to Hulk -> deal 3 damage to an enemy.
#   If you paid for this card using a [physical] resource, this attack gains
#   overkill.
#
# Cartes de reference :
#  - `01053` Relentless Assault, MEME phrase imprimee pour la provenance du
#    paiement : `effect.GetPaidResources().HasColor("R")` -> overkill porte
#    par `AttackProperty` ;
#  - `dt015` Preparation #2 pour `CostFunc.DealDamage(1, "YourHero")`.
#
# ⚠ Mots-pieges (PROCESSUS-CARTE etape 5) :
#  - « Deal 1 damage to Hulk -> » : la fleche en fait un COUT, paye AVANT.
#    Si le degat ne peut pas etre inflige, la carte ne se joue pas.
#  - ⚠ Ce degat de cout declenche Anger (hk001a), qui n'a AUCUN filtre
#    `is_from_attack` : la cible prend donc au moins 4 degats, pas 3, des que
#    le joueur envoie le degat rendu sur elle. C'est voulu par le pack.
#  - « using A [physical] » : AU MOINS une ressource physique, d'ou
#    `HasColor("R")` et surtout PAS `OnlyHasColor` (hk003, qui imprime
#    « only »). Un wild converti compte, comme sur 01053.
#  - « this ATTACK gains overkill » : c'est une attaque, donc Riposte,
#    Tenace et les preventions s'appliquent. Overkill seulement, jamais
#    piercing ni ranged.
#  - Coup 1 seulement : le cout ne peut donc pas etre paye par hk007 Natural
#    Genius en forme heros (cas de test dedie).


def GetAbilities() -> Sequence['Ability']:

    def reckless_charge(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(this, message)

        initiator = effect.GetInitiator()
        if initiator is None:
            return

        overkill = effect.GetPaidResources().HasColor("R")
        hero = initiator.GetHero()
        hero.DealDamage(effect.targets, 3, effect,
                        property=AttackProperty(overkill=overkill))

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            reckless_charge,
        ).SetPlay().SetLabel('attack')
        .SetCostFunc(CostFunc.DealDamage(1, "YourHero"))
        .SetTarget(Enemy),
    ]
