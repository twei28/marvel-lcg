from . import *

# Jaw Lock — custom « Nugget »
# Attach to an enemy. Hero form only.
# Response: After you play a TELEPORT event, deal 1 damage to attached enemy.
# Interrupt: When attached enemy would activate, discard Jaw Lock instead.


def GetAbilities() -> Sequence['Ability']:

    def apres_teleport(effect: 'Effect', message: 'Message.AfterPlayerPlayedCard') -> None:
        this = effect.this.CastTo(Upgrade)
        # CORRECTIF 4/8/2026 : ni `Worlds.FindAttachedUnit` ni
        # `Upgrade.GetAttachedTo` n'existent. Les deux appels etaient gardes par
        # un `hasattr`, donc la Response ne plantait pas : elle ne faisait
        # simplement JAMAIS rien. L'ennemi porteur se lit avec `GetBindFace`
        # (modele Star-Lord's Helmet 17010).
        cible = this.GetBindFace()
        if cible is not None:
            this.DealDamage([cible], 1, effect)

    def bloquer_activation(effect: 'Effect', message: 'Message.WhenEnemyWouldActivate') -> None:
        this = effect.this.CastTo(Upgrade)
        message.SetBeInstead(effect)
        Faces.DiscardAll([this], effect)

    def vise_l_ennemi_attache(effect: 'Effect', message: 'Message.WhenEnemyWouldActivate') -> bool:
        return Condition.CheckWhichCard("AttachedEnemy", message.trigger, effect)

    return [
        AbilityFactory.CanPlayThisUpgradeCard(
            Enemy,
        ).SetPlay(hero_form_only=True),
        AbilityFactory.AfterPlayerPlayedCard(
            AbilityType.Response,
            "You",
            CardFinder2("TELEPORT", Event),
            apres_teleport,
        ),
        Ability(
            AbilityType.Interrupt,
            Message.WhenEnemyWouldActivate,
            [vise_l_ennemi_attache],
            bloquer_activation,
        ).SetName("Jaw Lock"),
    ]
