from . import *

# Space Hand Grenade — amelioration Discovery (2/5). WEAPON. Cout 1.
# Attach to minion.
# Forced Interrupt: When this minion would attack, cancel that attack and deal
#   4 damage to that minion.
#
# Cartes de reference :
#  - 01185 Biomechanical Upgrades : amelioration qui s'ATTACHE A UN SBIRE et
#    porte un `ForcedInterrupt` vise sur `"AttachedMinion"`. Comparable pour
#    toute la charpente (attachement + declencheur sur le porteur) ; seul
#    l'evenement intercepte differe (elle guette la defaite, nous l'attaque).
#  - l'annulation d'attaque : 20003 Grasping Tendrils,
#    `message.CancelThisAttack(effect)`.
#
# ⚠ « that minion » = CELUI qui portait la grenade, pas un sbire au choix
# (mot-piege `that <nom>` de PROCESSUS-CARTE etape 5). C'est
# `message.attacker`, l'unite qui allait attaquer, et c'est aussi le porteur.
#
# ⚠ Le joueur CHOISIT le sbire a l'entree en jeu (`CanPlayThisUpgradeCard`
# avec un `CardFinder(card_type=Minion)`), contrairement a 01185 qui impose le
# sbire aux plus gros PV : le texte de la grenade ne pose aucune contrainte.
#
# ⚠ 4 degats a un sbire APRES annulation de son attaque : la carte tue net la
# plupart des sbires. C'est bien ce qui est imprime, et c'est coherent avec le
# fait qu'elle vienne du pool Discovery, hors deck.

def GetAbilities() -> Sequence['Ability']:

    def space_hand_grenade(effect: 'Effect', message: 'Message.WhenUnitWouldAttack') -> None:
        this = effect.this.CastTo(Upgrade)

        message.CancelThisAttack(effect)

        sbire = message.attacker
        if sbire is not None:
            this.DealDamage([sbire], 4, effect)

    return [
        AbilityFactory.CanPlayThisUpgradeCard(
            CardFinder(card_type=Minion),
        ),
        AbilityFactory.WhenUnitMakeAttack(
            AbilityType.ForcedInterrupt,
            "AttachedMinion",
            space_hand_grenade,
        ),
    ]
