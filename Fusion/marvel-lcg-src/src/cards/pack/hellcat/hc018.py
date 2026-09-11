from . import *
from cards.pack.hellcat.hellcat import AMentalImprime
# * Firestar (Angelica Jones) — ALLIEE d'AGRESSIVITE custom (jakxin), cout 3,
# [mental]. X-MEN. CTR 1 (1 conseq.) / ATQ 1 (1 conseq.), 3 PV.
# Firestar enters play with 1 fire counter on her for each [mental] resource
#   used to pay for her.
# Interrupt: When Firestar attacks, remove 1 fire counter from her → deal 2
#   damage to an enemy.
#
# Modeles : 28018 Moon Girl (`AfterYouPlayThisFromHand` + `paid_resources`),
# 23016 (`CostFunc.Counter("This", 1, 'fire')`), ss012 (interruption
# `WhenUnitMakeAttack(..., "This")`). Compteur 'fire' ajoute a l'enum COUNTER
# le 11/09/2026 (card_face.py), libelle « feu » dans compteurs-fr.ts.
# ⚠ « ★ Interrupt » : l'etoile n'ajoute rien (arbitrage utilisateur du
#   11/09/2026), c'est un Interrupt ordinaire, repetable a chaque attaque tant
#   qu'il reste un compteur.

def GetAbilities() -> Sequence['Ability']:

    def compteurs_de_feu(effect: 'Effect', message: 'Message.AfterPlayerPlayedCard') -> None:
        this = effect.this.CastTo(Ally)
        n = message.paid_resources.GetColor("B")
        if n > 0:
            this.CastTo(CanPlaceCounter).PlaceCountersInternal(n, 'fire', effect)

    def firestar(effect: 'Effect', message: 'Message.WhenUnitWouldAttack') -> None:
        this = effect.this.CastTo(Ally)
        Unused(message)
        this.DealDamage(effect.targets, 2, effect)

    return [
        AbilityFactory.AfterYouPlayThisFromHand(
            AbilityType.ForcedResponse,
            compteurs_de_feu,
        ),
        AbilityFactory.WhenUnitMakeAttack(
            AbilityType.Interrupt,
            "This",
            firestar,
        ).SetCostFunc(CostFunc.Counter("This", 1, 'fire'))
        .SetTarget(Enemy),
    ]
