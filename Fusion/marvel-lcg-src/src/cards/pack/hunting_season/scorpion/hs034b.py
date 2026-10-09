from . import *

# hs034b Vengeful Pursuit

def GetAbilities() -> Sequence['Ability']:

    def remplacer(effect: 'Effect', message: 'Message.WhenMainSchemeStageWouldBeCompleted') -> None:
        this = effect.this.CastTo(MainScheme)
        message.SetBeInstead(effect)
        PlacerUneBlessureSurJameson(effect)
        porteurs = [this, *this.GetAttachedUpgrades(), *this.GetAttachedAttachments()]
        for p in porteurs:
            if p.GetTokens('threat'):
                Faces.RemoveTokensOn([p], "All", 'threat', effect)

    return [
        AbilityFactory.WhenMainSchemeStageWouldBeCompleted(AbilityType.ForcedInterrupt, "This", remplacer),
    ]
