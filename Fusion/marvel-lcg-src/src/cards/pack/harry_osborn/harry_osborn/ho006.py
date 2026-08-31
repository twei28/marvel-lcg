from . import *

# * Norman Osborn — soutien signature. PERSONA. TECH. Cout 1.
# Hero Interrupt: When you play an ATTACK event, exhaust Norman Osborn ->
#   that event deals 1 additional damage.
#
# Cartes de reference : 32047 Aggressive Energy et 54002 * Cybernetic Arm,
# qui portent MOT POUR MOT « that event deals 1 additional damage » : un
# `RegisterTemp(WhenUnitWouldAttack(Temp0, "You", DealAdditionalDamage(1)),
# until_resolve_effect=<effet de l'evenement>)`. Leur declencheur a eux est
# le PAIEMENT ; ici c'est le JEU de la carte, donc
# `WhenPlayerPlayCard(HeroInterrupt, "You", CardFinder2("ATTACK", Event))`
# (montage de 37006 et 05011 pour ce message-la), et le cout d'epuisement
# passe par `SetCostFunc(CostFunc.Exhaust("This"))`.

def GetAbilities() -> Sequence['Ability']:

    def norman(effect: 'Effect', message: 'Message.WhenPlayerPlayCard') -> None:
        this = effect.this.CastTo(Support)

        this.effect.RegisterTemp(
            AbilityFactory.WhenUnitWouldAttack(
                AbilityType.Temp0,
                "You",
                lambda effect, atk_message:
                    atk_message.DealAdditionalDamage(1, effect),
                by_effect=message.played_effect,
            ),
            unregister_after_exec=False,
            until_resolve_effect=message.played_effect
        )

    return [
        AbilityFactory.WhenPlayerPlayCard(
            AbilityType.HeroInterrupt,
            "You",
            CardFinder2("ATTACK", Event),
            norman,
        ).SetCostFunc(CostFunc.Exhaust("This")),
    ]
