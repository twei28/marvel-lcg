from . import *

# Galvanize

def GetAbilities() -> Sequence['Ability']:

    # La carte dit « maximum hit points ». Le crochet officiel le plus proche,
    # `only_if_your_identity_has_at_least_printed_hp` (31024, Unshakable), ne lit
    # que l'imprime : il raterait les points gagnes en jeu. La condition est donc
    # ecrite a la main, sur `max_health`, qui est ce que dit la carte.
    def check_max_hp(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> bool:
        identity = effect.GetInitiator().GetIdentity()
        return identity.max_health >= 12

    def galvanize(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(this)

        initiator = effect.GetInitiator()
        if initiator.AskChooseOneText(["Ready", "Draw"]) == "Ready":
            Faces.ReadyAll([initiator.GetHero()], effect)
        else:
            initiator.DrawUp(1, effect)

    return [
        AbilityFactory.CanPlayThisUpgradeCard(
            conditions=[check_max_hp]
        ),
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            galvanize
        ).SetCostFunc(CostFunc.Exhaust("This"))
        .SetCostFunc(CostFunc.TakeDamage(3, "Initiator")),
    ]
