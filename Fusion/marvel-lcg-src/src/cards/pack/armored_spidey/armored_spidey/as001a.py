from . import *

# * Armored Spidey — face HEROS. PV 10, ATQ 2, CTR 2, DEF 2, main 5.
# WEB-WARRIOR.
# Armor Protection — Interrupt: When you would take any amount of damage from
#   an attack, remove a metal counter from Spider Armor -> prevent up to 2 of
#   that damage.
#
# Cartes de reference :
#  - **`im007`** Energy Shield (pack iron_man_model_42) et `01098` Armored
#    Rhino Suit : `WhenUnitWouldTakeDamage(..., "You", op)` puis
#    `message.PreventDamage(2, effect)`. Meme phrase imprimee au compteur
#    pres, ecrite trois semaines plus tot.
#  - `CostFunc.Counter(cible, 1, 'metal')` (cost_func.py:792) pour le cout en
#    compteur : c'est la classe de cout native, elle refuse le paiement quand
#    la cible n'a pas assez de compteurs (`has_enough_counter`).
#
# ⚠ Mots-pieges (PROCESSUS-CARTE etape 5) :
#  - « damage **from an attack** » : PAS toute source. Une traitrise, un degat
#    indirect, un degat que le heros s'inflige lui-meme ne declenchent RIEN.
#    D'ou `is_from_attack=True`, et c'est la difference exacte avec im007, qui
#    imprime « any amount of damage » tout court.
#  - « **you** would take » : l'identite, donc cette face-ci seulement, la
#    capacite etant imprimee sur la face heros.
#  - « remove a metal counter from Spider Armor **->** » : la fleche en fait
#    un COUT. Sans compteur, aucune prevention, et l'option n'est meme pas
#    offerte. LE RETRAIT VA DANS LE COUT, JAMAIS DANS LE CORPS (voir
#    `ArmureCible` dans le `__init__` du set).
#  - « prevent **up to** 2 » : 2 au plus. `PreventDamage(2, ...)` plafonne
#    deja, une instance de 1 degat ne gaspille rien au-dela.
#  - ⚠ CONSEQUENCE DE JEU : le 3e compteur depense retourne l'armure sur
#    as002b DESTROYED (Forced Response de as002a), et le heros perd alors
#    1 ATQ et 1 DEF. Prevenir 2 degats a un prix differe.


def GetAbilities() -> Sequence['Ability']:

    def armor_protection(effect: 'Effect', message: 'Message.WhenUnitWouldTakeDamage') -> None:
        this = effect.this.CastTo(Hero)
        Unused(this)

        # Le compteur a deja ete retire par le COUT : ici, on previent.
        message.PreventDamage(2, effect)

    return [
        AbilityFactory.WhenUnitWouldTakeDamage(
            AbilityType.Interrupt,
            "You",
            armor_protection,
            is_from_attack=True,
        ).SetName("Armor Protection")
        .SetCostFunc(CostFunc.Counter(ArmureCible, 1, 'metal')),
    ]
