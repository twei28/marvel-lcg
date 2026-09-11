from . import *

# Thunder Strike (evenement, cout 2, ATTACK SUPERPOWER) — x4
# Requirement ([energy]).
# Hero Action (attack): Deal 5 damage to an enemy. This attack gains piercing.
# Special: Stun an enemy.
#
# ⚠ C'est la SEULE carte du pack qui imprime l'ECLAIR (`"RES": "L"`), et son
# Requirement est une ENERGIE officielle : les deux ressources du Tempest
# viennent donc de deux endroits differents. `Requirement` est une base
# automatique lue dans `desc` (fiche mots-cles/requirement.md), rien a coder.
#
# Modeles : 05015 Tackle (Hero Action attaque sur evenement), 35023 pour
# `AttackProperty(piercing=True)`, ab007 pour le Special nomme.

def GetAbilities() -> Sequence['Ability']:

    def thunder_strike(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        this.DealDamage(effect.targets, 5, effect, property=AttackProperty(piercing=True))

    def special(effect: 'Effect', message: 'Message.WhenResolveSpecialAbility') -> None:
        this = effect.this.CastTo(Event)
        Unused(this)
        joueur = message.GetToPlayer() or effect.GetInitiator()
        cible = ChoisirUnEnnemi(joueur, effect)
        if cible:
            Faces.GiveStatus([cible], "Stunned", effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            thunder_strike,
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
