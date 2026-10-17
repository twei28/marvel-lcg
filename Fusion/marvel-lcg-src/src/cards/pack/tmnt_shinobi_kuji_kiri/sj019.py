from . import *

# Static Shock (sj019), Kuji-Kiri, evenement ATTACK SPELL (Inkwire, TMNT Shinobi).
# [star] Rampage 1. (As an additional cost for this card, take 1 damage and discard 1 card from the top of your
# deck.)
# Hero Action (attack): Deal 3 damage to an enemy. Deal 1 damage to each enemy engaged with you.
#
# Mots-cles (fiches lues AVANT le code) : Rampage (`rampage.md` : `CostFunc.Rampage(X)`, cout additionnel, le [star]
# devant Rampage et le cout « 1* » sont l'icone etoile des regles, aucun code).
# Cartes de reference : `tmnt_aspect_aggression/ua015` Demolish (Rampage sur une Hero Action d'evenement) ;
# `rainy/thor_jane_foster/ra005` Lightning Strike (« Deal N damage to an enemy and 1 damage to each enemy engaged
# with you » : `Worlds.FindCardsOnField(card_type=Enemy, engaged_with=initiator)`, vilain compris quand il est engage).
#
# TEXTE CONTRE CODE
#  ⚠ « Rampage 1 » : 1 degat a l'identite ET 1 carte du dessus du deck defaussee, EN COUT (payes ensemble ; des
#    degats empeches = cout impaye, carte non jouee).
#  ⚠ « Deal 3 damage to AN enemy » (degats directs, l'ATQ du heros est ignoree) PUIS « 1 damage to EACH enemy
#    ENGAGED WITH YOU » : l'ennemi cible compte aussi s'il est engage avec vous (3 + 1) ; un ennemi vaincu par
#    les 3 degats n'en prend pas de plus.
#  ⚠ Label 'attack' (parenthese imprimee).


def GetAbilities() -> Sequence['Ability']:

    def static_shock(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(message)

        joueur = effect.GetInitiator()
        if joueur is None:
            return
        this.DealDamage(effect.targets, 3, effect)

        engages = Worlds.FindCardsOnField(
            effect,
            card_type=Enemy,
            engaged_with=joueur,
        )
        engages = [x for x in engages if not x.IsDefeated()]
        if engages:
            this.DealDamage(engages, 1, effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            static_shock,
        ).SetPlay().SetLabel('attack')
        .SetCostFunc(CostFunc.Rampage(1))
        .SetTarget(Enemy),
    ]
