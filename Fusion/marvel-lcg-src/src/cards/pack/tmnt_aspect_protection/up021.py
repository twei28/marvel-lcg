from . import *

# * Jotaro — ALLIE 3 [physical], aspect Protection (TMNT Reskins, Inkwire). RABBIT. RONIN.
# THW 1 (1), ATK 2 (1), PV 2. Toughness.
# Interrupt: When an enemy would deal any amount of damage, spend a [physical] resource -> reduce that
#   amount of damage by 1. (Limit once per round.)
#
# MODIFIEE de `26014` Protector (« When Protector would take any amount of damage, spend a [mental]
# resource -> reduce that amount by 1. (Limit once per round.) »). Script propre.
# ⚠ Cout imprime 3 sur le scan (la table de classement disait 2 : le scan fait foi).
#
# MOT-CLE : Toughness (fiche toughness.md) — lu dans `desc`, AUCUN code.
#
# CARTES DE REFERENCE
#  - `26014` Protector : `WhenUnitWouldTakeDamage(Interrupt, ...)` + `ReduceDamage(1)` +
#    `.SetCost(Cost(...))` + `.LimitOncePerRound()`.
#  - `32011` Nightcrawler : `who_deal_damage=Enemy` (la SOURCE des degats est un ennemi).
#
# TEXTE CONTRE CODE
#  ⚠ « When AN ENEMY would deal any amount of damage » : la condition porte sur la SOURCE (un ennemi), pas
#    sur la cible : n'importe quel personnage qui recevrait ces degats (Jotaro, l'identite, un autre
#    allie...). Lecture litterale : `Unit2` pour la cible, `who_deal_damage=Enemy`.
#  ⚠ « spend a [physical] resource » : `Cost("R")` (icone poing noir du texte).
#  ⚠ « reduce that amount by 1 » : `ReduceDamage(1)` (pas une prevention totale).
#  ⚠ « Limit once per round » : `LimitOncePerRound()` (temoin d'epuisement dans les cas).


def GetAbilities() -> Sequence['Ability']:

    def jotaro(effect: 'Effect', message: 'Message.WhenUnitWouldTakeDamage') -> None:
        this = effect.this.CastTo(Ally)
        Unused(this)
        message.ReduceDamage(1, effect)

    return [
        AbilityFactory.WhenUnitWouldTakeDamage(
            AbilityType.Interrupt,
            Unit2,
            jotaro,
            who_deal_damage=Enemy,
        ).SetCost(Cost("R"))
        .LimitOncePerRound(),
    ]
