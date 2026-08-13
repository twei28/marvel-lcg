from . import *

# False Security

def GetAbilities() -> Sequence['Ability']:

    def poser_le_tough(effect: 'Effect', message: 'Message.AfterCardEnterPlay') -> None:
        this = effect.this.CastTo(Upgrade)

        sbire = this.GetBindFace()
        if sbire:
            Faces.GiveStatus([sbire], "Tough", effect)

    def false_security(effect: 'Effect', message: 'Message.AfterStatusDiscardFrom') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(this)

        Faces.ReadyAll(effect.targets, effect)

    return [
        AbilityFactory.CanPlayThisUpgradeCard(
            CardFinder(card_type=Minion)
        ),
        AbilityFactory.AfterCardEnterPlay(
            AbilityType.ForcedResponse,
            "This",
            poser_le_tough
        ),
        AbilityFactory.AfterStatusDiscardFrom(
            AbilityType.ForcedResponse,
            "AttachedMinion",
            "Tough",
            false_security
        ).SetCostFunc(CostFunc.Discard("This"))
        .SetTarget(Friend, canbe_ready=True),
    ]
