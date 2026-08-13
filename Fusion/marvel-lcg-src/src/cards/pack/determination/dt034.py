from . import *

# Improvised 'Porting

def GetAbilities() -> Sequence['Ability']:

    def improvised_porting(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(this)

        initiator = effect.GetInitiator()
        identity = initiator.GetIdentity()
        identity.ChangeToOtherForm(effect)
        Faces.ReadyAll([initiator.GetIdentity()], effect)

    def donner_le_boost(targets: Sequence['CardFace'], effect: 'Effect') -> bool:
        villain = Worlds.FindVillain(effect)
        if villain is None:
            return False
        villain.CastTo(CanBoost).GiveFacedownBoostCardsInternal(1, effect, None)
        return True

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.HeroAction,
            improvised_porting
        ).SetPlay()
        .SetCostFunc(CostFunc.Custom(None, donner_le_boost)),
    ]
