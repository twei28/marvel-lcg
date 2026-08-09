from . import *

# * Lady Hellbender — custom « DesignHacker »
# Hero Action: Spend [wild] resources equal to Lady Hellbender's remaining hit
#   points → treat Lady Hellbender as an ally you control with THW instead of
#   SCH.


def GetAbilities() -> Sequence['Ability']:

    def spend_wild(targets: Sequence['CardFace'], effect: 'Effect') -> bool:
        this = effect.this.CastTo(Minion)
        player = effect.GetInitiator()
        if player is None:
            return False

        value = this.health
        if value <= 0:
            return False

        return player.AskSpendResourcesInternal(Cost("G" * value), effect) is not None

    def lady_hellbender(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Minion)
        initiator = effect.GetInitiator()

        # `TreatAsAlly` reprend le SCH imprimé du sbire comme THW de l'allié,
        # ce qui est exactement le « with THW instead of SCH » de la carte.
        Faces.TreatAsAlly(this, "tah_hellbender_ally", initiator, effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            lady_hellbender,
        ).SetCostFunc(CostFunc.Custom(None, spend_wild)),
    ]
