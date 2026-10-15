from . import *

# Iaijutsu — AMELIORATION signature, x1. STANCE. Cout 0, [mental].
# Hero Interrupt: When an enemy initiates an attack, exhaust a [[KATANA]]
#   upgrade you control -> you may play an [[ATTACK]] event with a
#   "Hero Action" ability from your hand (paying its cost). If this attack
#   defeats an enemy, draw 1 card.
#
# Cartes de reference :
#  - `42013` Warpath: James Proudstar : `PlayCardsLikeInTurn(effect.targets,
#    effect)` avec `SetTarget(check_fn=can_be_play, from_where=["YourHandCards"])`
#    — jouer un evenement a Hero Action DEPUIS LA MAIN en payant son cout ;
#  - `vr009` Lethal Protector / `32014` Powerful Punch : declencheur
#    `WhenUnitWouldAttack(HeroInterrupt, Enemy, op)` = « when an enemy
#    initiates an attack » ;
#  - `27018` / `27043` : `CostFunc.Exhaust(trait=..., from_where=["YouControlCards"])`
#    pour « exhaust a [[KATANA]] upgrade you control » ;
#  - `angela` : `PlayerStat.kill_counter` (game/rule/gameplay.py:43) pour
#    mesurer une defaite.
#
# Insert du pack : « The Iaijutsu upgrade ability requires you to exhaust a
# KATANA, it does NOT exhaust itself ». D'ou le cout sur un KATANA, et PAS
# `CostFunc.Exhaust("This")`.
#
# Mots-pieges :
#  - « when an ENEMY initiates an attack » : tout ennemi (vilain ET sbires),
#    contre n'importe quel joueur, sans filtre de cible ;
#  - « you MAY play » : le jeu de l'evenement reste optionnel (Interrupt
#    propose, et `forced` n'est PAS force : le paiement peut etre refuse) ;
#  - « an [[ATTACK]] event WITH a "Hero Action" ability » : trait ATTACK ET
#    une capacite HeroAction (comme `can_be_play` de 42013) ;
#  - « (paying its cost) » : PAS `ignore_resources_cost` ;
#  - TODO-QUESTION Q4 : « If this attack defeats an enemy, draw 1 card ».
#    Rendu APPROXIMATIF : on compare `joueur.stat.kill_counter` avant/apres le
#    jeu de l'evenement. Toute defaite causee par le joueur pendant la
#    resolution compte. Pas de fabrique « cette attaque defait » disponible
#    pour un evenement joue par cette voie.


def GetAbilities() -> Sequence['Ability']:

    def peut_etre_jouee(effect: 'Effect', face: 'CardFace') -> bool:
        joueur = effect.GetInitiator()
        if joueur is None:
            return False
        if not Event.IsType(face):
            return False
        if not face.HasTrait("ATTACK"):
            return False
        if not face.effect.Find(type=AbilityType.HeroAction):
            return False
        if not face.CanPlayBy(joueur):
            return False
        return True

    def iaijutsu(effect: 'Effect', message: 'Message.WhenUnitWouldAttack') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(this, message)

        joueur = effect.GetInitiator()
        if joueur is None:
            return
        avant = len(joueur.stat.kill_counter)
        joueur.PlayCardsLikeInTurn(effect.targets, effect)
        if len(joueur.stat.kill_counter) > avant:
            joueur.DrawUp(1, effect)

    return [
        AbilityFactory.CanPlayThisUpgradeCard(),
        AbilityFactory.WhenUnitWouldAttack(
            AbilityType.HeroInterrupt,
            Enemy,
            iaijutsu,
        ).SetCostFunc(CostFunc.Exhaust(card_type=Upgrade, trait="KATANA",
                                       from_where=["YouControlCards"]))
        .SetTarget(check_fn=peut_etre_jouee, from_where=["YourHandCards"]),
    ]
