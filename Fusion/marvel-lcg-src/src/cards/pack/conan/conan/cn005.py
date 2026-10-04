from . import *

# Destroyer's Defiance (x2) — evenement, cout 1* [energy]. DEFENSE.
# [star] Discount 1 (KING).
# Hero Interrupt (defense): When you would take any amount of damage, prevent
#   all of that damage. Place 1 Crom counter on The Cimmerian (2 counters
#   instead if you are King Conan).
#
# CARTES DE REFERENCE
#  - rs005 Devil's Defiance : `WhenUnitWouldTakeDamage(HeroInterrupt, "You",
#    op).SetPlay().SetLabel('defense')`, `message.PreventDamage("All")`.
#
# TEXTE CONTRE CODE
#  « any amount of damage » : PAS seulement une attaque (pas d'`is_from_attack`),
#    une traitrise qui inflige des degats est aussi couverte.
#  « (defense) » : pendant une attaque ennemie, jouer cette carte fait de
#    l'identite le defenseur (Rules Reference v1.8, entree Defend, Defense) ;
#    hors attaque, ce n'est pas une defense.


def GetAbilities() -> Sequence['Ability']:

    def defiance(effect: 'Effect', message: 'Message.WhenUnitWouldTakeDamage') -> None:
        message.PreventDamage("All", effect)
        joueur = JoueurDe(effect)
        PoserCrom(joueur, 2 if EstKingConan(joueur) else 1, effect)

    return [
        DiscountAbility(1, ["KING"]),
        AbilityFactory.WhenUnitWouldTakeDamage(
            AbilityType.HeroInterrupt,
            "You",
            defiance,
        ).SetPlay().SetLabel('defense'),
    ]
