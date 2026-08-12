from . import *

# "I've Got This!" — custom « DesignHacker »
# Hero Action (attack): Deal 5 damage to the villain (7 damage instead if this
#   attack has ranged or piercing).
#
# La carte porte `SetLabel('attack')`, donc `DealDamage` passe par
# `CanAttack.SpecialAttack` (voir `is_like_attack` dans ability.py) : c'est une
# VRAIE attaque. Le moteur resout d'abord les mots-cles
# (`CheckIfAttackMessageHasKeyword`) puis, si l'attaque en a au moins un,
# envoie `WhenUnitMakeKeyWordAttack`. C'est la qu'on ajoute les 2 degats.
#
# L'interet : on ne devine rien. Ten Out of Ten! (piercing a 10 PV) et Bear
# Arms (ranged) accordent leurs mots-cles par la fabrique standard, mais
# n'IMPORTE quelle carte d'aspect exterieure au pack qui accorde ranged ou
# piercing aux attaques du heros compte de la meme facon.

def GetAbilities() -> Sequence['Ability']:

    def ive_got_this(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)

        def bonus(effect2: 'Effect', message2: 'Message.WhenUnitMakeKeyWordAttack') -> None:
            message2.DealAdditionalDamage(2, effect2)

        def ranged_ou_piercing(effect2: 'Effect', message2: 'Message.WhenUnitMakeKeyWordAttack') -> bool:
            attaque = message2.would_atk_unit_message
            return attaque.IsRanged() or attaque.IsPiercing()

        identity = GetAgentAntiVenom(effect)
        if identity is not None:
            # Posee juste avant l'attaque et retiree des sa premiere execution :
            # elle ne peut concerner que celle-ci.
            identity.effect.RegisterTemp(
                AbilityFactory.WhenUnitMakeKeyWordAttack(
                    AbilityType.Temp0,
                    "This",
                    bonus,
                    conditions=[ranged_ou_piercing],
                ),
                unregister_after_exec=True,
            )

        this.DealDamage(effect.targets, 5, effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            ive_got_this,
        ).SetPlay()
        .SetLabel('attack')
        .SetTarget(Villain),
    ]
