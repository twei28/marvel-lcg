from . import *

# Heven's Fury — evenement. ATTACK. Cout 3. x3
# Hero Action (attack): Deal 7 damage to an enemy. You may exhaust a WEAPON
#   you control. If you do, divide the damage among enemies in play instead.
#
# Cartes de reference : 13006 Wasp Sting (pack wsp) pour la repartition
# (`SetTarget(Enemy, range=(1, N), repeat_rules="Health")`, 1 degat par
# selection), et vp003 Talk About Armed Assault (pack venompool) pour le
# montage a DEUX capacites mutuellement exclusives.
#
# ⚠ `range` est fige a la construction de la capacite : impossible de decider
# au moment du jeu si l'on frappe une cible ou sept. On expose donc DEUX
# capacites de jeu, et le « You MAY exhaust » devient le choix entre les deux
# — la seconde portant l'inclinaison de l'arme en COUT, ce qui la rend
# indisponible quand on ne controle aucune arme prete. Le joueur retrouve
# exactement les options imprimees.
#
# ⚠ CONSEQUENCE OBLIGATOIRE : un evenement a deux capacites `Play` doit etre
# declare dans la liste blanche de `game/card/factory.py`, sinon
# `AssertionError: face.paper.card_id='an003'` AU SETUP — invisible pour
# test_cards, et le deck ne monte pas. Piege paye sur vp003 le 31/08/2026.

DEGATS = 7


def GetAbilities() -> Sequence['Ability']:

    def cible_unique(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(message)
        this.DealDamage(effect.targets, DEGATS, effect)

    def repartis(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(message)
        this.DealDamage(effect.targets, 1, effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            cible_unique,
        ).SetPlay().SetLabel('attack')
        .SetTarget(Enemy, range=(1, 1)),

        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            repartis,
        ).SetPlay().SetLabel('attack')
        .SetCostFunc(CostFunc.Exhaust(trait="WEAPON"))
        .SetTarget(Enemy, range=(1, DEGATS), repeat_rules="Health"),
    ]
