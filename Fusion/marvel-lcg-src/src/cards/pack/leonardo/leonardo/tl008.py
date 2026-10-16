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
#  - `game/card/face/card_face.py` DealDamage(if_this_attack_defeats=) : meme
#    ecoute `AfterUnitDefeatedUnit` enregistree en temporaire, ici filtree sur
#    `message.by_effect.this` (l'evenement joue) car le script de l'evenement
#    n'est pas le notre.
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
#  - « If THIS ATTACK defeats an enemy » : DECISION UTILISATEUR (15/10/2026) =
#    crochet EXACT sur l'attaque. On ecoute `AfterUnitDefeatedUnit` pendant le jeu
#    de l'evenement et on ne retient que les defaites dont `by_effect.this` est
#    L'EVENEMENT JOUE (pas un autre effet, pas une defaite causee ailleurs).


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
        jouee = effect.targets[0] if effect.targets else None
        vaincu = [False]

        def defaite(check_effect: 'Effect', check_message: 'Message.AfterUnitDefeatedUnit') -> None:
            Unused(check_effect, check_message)
            vaincu[0] = True

        from game.operate.effects import Effects
        temp = this.effect.RegisterTemp(
            Ability(
                AbilityType.Temp0,
                Message.AfterUnitDefeatedUnit,
                [lambda check_effect, check_message:
                    jouee is not None and
                    check_message.by_effect.this == jouee and
                    Enemy.IsType(check_message.target)],
                defaite,
            ),
            unregister_after_exec=False,
        )
        joueur.PlayCardsLikeInTurn(effect.targets, effect)
        Effects.UnRegister(temp)
        if vaincu[0]:
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
