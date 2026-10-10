from . import *

# Cruisin' for a Bruisin'
# Attach to a minion. Max 1 per minion.
# Attacks against attached minion deal 2 additional damage and gain overkill.
# Response: After you play this card, engage attached minion.
#
# CORRECTIF (10/10/2026, audit Luke Cage) : trois defauts mesures.
#  - « Attach to a MINION » : sans `CanPlayThisUpgradeCard(Minion)`, la cible par
#    defaut etait TON identite (upgrade.py). Modele : ar008 Reeling.
#  - « ATTACKS AGAINST attached minion gain overkill » : visait l'ATTAQUANT
#    attache. Modele : ar008 Reeling, `WhenUnitWouldAttackUnit(None, "AttachedMinion")`.
#  - « deal 2 additional damage » : passait par l'ATQ de l'attaque de base, et
#    meme celle-la ne partait pas. Toute attaque (de base ou d'evenement) :
#    +2 sur les degats que l'attaque va infliger au sbire attache, a l'etape
#    « would be dealt », donc avant le calcul de l'exces qui deferle.
#  - « Max 1 per minion » : `desc.MaxPerUnit`, aucun code.

def GetAbilities() -> Sequence['Ability']:

    def deferler(effect: 'Effect', message: 'Message.WhenUnitWouldAttackUnit') -> None:
        message.GainOverKill(effect)

    def plus_deux(effect: 'Effect', message: 'Message.WhenFaceWouldDealDamage') -> None:
        message.IncreaseDamage(2, effect)

    def engager(effect: 'Effect', message: 'Message.AfterPlayerPlayedCard') -> None:
        this = effect.this.CastTo(Upgrade)
        cible = this.bind_face
        player = effect.GetInitiator()
        if cible is None or player is None:
            return
        if Minion.IsType(cible):
            cible.CastTo(Minion).EngagePlayer(player, effect)

    return [
        AbilityFactory.CanPlayThisUpgradeCard(Minion),
        AbilityFactory.WhenUnitWouldAttackUnit(
            AbilityType.NonKeyword,
            None,
            "AttachedMinion",
            deferler,
        ),
        AbilityFactory.WhenFaceWouldDealDamage(
            AbilityType.NonKeyword,
            None,
            plus_deux,
            who_take_damage="AttachedMinion",
            from_attack=True,
        ),
        AbilityFactory.AfterYouPlayThisFromHand(AbilityType.Response, engager),
    ]
