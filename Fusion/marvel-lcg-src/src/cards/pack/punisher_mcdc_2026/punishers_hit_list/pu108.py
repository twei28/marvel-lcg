from . import *

# * Rachel Cole-Alves — SBIRE. MARINE. VIGILANTE. SCH 1, ATQ 2, 5 PV, Boost 2.
# Punisher cannot attack this minion.   (porte par `CARTES_QUE_PUNISHER_NE_PEUT_PAS_ATTAQUER` dans __init__.py)
# When Revealed : Resolve Punisher's "Punishment" ability. Otherwise, Rachel Cole-Alves attacks you. If you are in hero
#   form, give her a boost card for this attack.
#
# Cartes de reference : `Punishment()` (__init__.py), `Enemy.DoAttackYou(joueur, effect, property=AttackProperty(...))`
# (enemy.py), pu059 (`ChooseAbilities`).
# ⚠ « Otherwise » : si Punishment n'a pas pu etre resolu (pas de Punisher en jeu, ou aucune cible) ; « If you are in HERO
# form, give her a boost card » : en alter ego elle attaque sans carte de boost.

def GetAbilities() -> Sequence['Ability']:

    def revele(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this.CastTo(Minion)
        joueur = message.GetToPlayer()
        if Punishment(effect):
            return
        if joueur is None:
            return
        this.DoAttackYou(joueur, effect, property=AttackProperty(against_player=joueur, do_not_give_boost=not joueur.IsHero()))

    return [
        AbilityFactory.WhenThisRevealed(None, revele),
    ]
