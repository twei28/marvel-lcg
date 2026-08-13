from . import *

# Twice the Determination

def GetAbilities() -> Sequence['Ability']:

    def twice_the_determination(effect: 'Effect', message: 'Message.AfterCardsBeSpendAsResource') -> None:
        this = effect.this.CastTo(Resource)

        initiator = effect.GetInitiator()
        Faces.ReturnToHand([this], initiator, effect)

    return [
        AbilityFactory.AfterYouSpendThisCard(
            AbilityType.HeroResponse,
            twice_the_determination
        ).LimitOncePerRound(),
    ]
