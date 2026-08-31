from . import *

# Whack-a-Rabbit — evenement. ATTACK. Cout 0. x3
# You may trigger the "Hero Action" below one additional time for each minion
#   engaged with you. (Each enemy may only be targeted once.)
# Hero Action (attack): Take 1 damage -> deal 2 damage to an enemy.
#
# Cartes de reference : 13006 Wasp Sting pour le ciblage multiple
# (`SetTarget(Enemy, range=(min, max))`), 44010 / 45043 pour « Take N damage »
# en cout.
#
# CHOIX TECHNIQUE (§9 du guide, pas un arbitrage de regles) : le texte parle
# de repeter une capacite N+1 fois ; le moteur ne sait pas repeter une
# capacite, mais `range` accepte une BORNE CALCULEE
# (`SelectorRange.RANGE_TYPE` autorise `Callable[['Effect'], int]`, voir
# game/selector/selector_range.py:16). On modelise donc les N+1 declenchements
# par UNE capacite qui designe 1 a N+1 ennemis, et l'on paie le cout une fois
# PAR ennemi designe. Resultat identique en jeu, sans repetition d'interface.
#
# ⚠ « Each enemy may only be targeted once » : on n'ajoute SURTOUT PAS
# `repeat_rules="Health"` (contrairement a vp003 Talk About Armed Assault, ou
# la repartition libre l'exige). Sans cette cle, le moteur interdit de
# reprendre deux fois la meme cible — exactement ce que la parenthese demande.
#
# ⚠ « You MAY trigger » : la borne basse reste 1 (la capacite de base n'est
# pas optionnelle une fois la carte jouee), la borne haute est facultative.

def GetAbilities() -> Sequence['Ability']:

    def cibles_max(effect: 'Effect') -> int:
        """1 declenchement de base + 1 par sbire engage avec le joueur."""
        initiator = effect.GetInitiator()
        if initiator is None:
            return 1
        return 1 + len(initiator.engaged_minions.Get())

    def whack_a_rabbit(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(message)

        identity = GetVenompool(effect)

        # Un declenchement = un cout PUIS son effet, dans cet ordre, sbire par
        # sbire : c'est bien N fois « Take 1 damage -> deal 2 damage », et non
        # « take 1 damage » une seule fois pour toute la carte.
        for cible in effect.targets:
            if identity is not None:
                identity.TakeDamage(this, 1, effect)
            this.DealDamage([cible], 2, effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            whack_a_rabbit,
        ).SetPlay().SetLabel('attack')
        .SetTarget(Enemy, range=(1, cibles_max)),
    ]
