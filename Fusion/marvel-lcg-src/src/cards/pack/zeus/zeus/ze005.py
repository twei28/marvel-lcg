from . import *

# Olympian Might (evenement, cout 3, ATTACK SUPERPOWER, physique) — x2
# Requirement ([energy][energy]).
# Hero Action (attack): Deal 7 damage to an enemy. If this attack defeats that
# enemy, ready Zeus.
# Special: Gain tough status card.
#
# Modele : 35018 Precision Strike (« if this attack defeats », lu sur
# `effect.targets[0].IsDefeated()` juste apres DealDamage). « ready Zeus » :
# c'est le HEROS, donc `GetHero()`, pas l'identite quelle que soit sa forme
# (RECETTES §3 : lire le mot, un nom propre ne designe qu'une face). « Gain
# tough status card » : sur l'identite, comme tout statut du joueur.

def GetAbilities() -> Sequence['Ability']:

    def olympian_might(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        initiator = effect.GetInitiator()
        this.DealDamage(effect.targets, 7, effect)
        if effect.targets[0].IsDefeated():
            Faces.ReadyAll([initiator.GetHero()], effect)

    def special(effect: 'Effect', message: 'Message.WhenResolveSpecialAbility') -> None:
        this = effect.this.CastTo(Event)
        Unused(this)
        joueur = message.GetToPlayer() or effect.GetInitiator()
        Faces.GiveStatus([joueur.GetIdentity()], "Tough", effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            olympian_might,
        ).SetPlay().SetLabel('attack')
        .SetTarget(Enemy),

        # ⚠ `.NoOutOfPlayLimit()` : ce Special se resout depuis la MAIN (Hera)
        # ou pendant le paiement (Tempest), jamais depuis la table. Sans ce
        # drapeau, le moteur ignore l'effet d'une carte hors jeu et le message
        # `WhenResolveSpecialAbility` tombe dans le vide (vu le 11/09/2026).
        AbilityFactory.WhenResolveSpecialAbility(
            "This",
            special,
        ).NoOutOfPlayLimit(),
    ]
