from . import *

# Webbed

def GetAbilities() -> Sequence['Ability']:

    def au_lieu_dactiver(effect: 'Effect', message: 'Message.WhenEnemyWouldActivate') -> None:
        # « Forced Interrupt: When an enemy would activate, discard Webbed
        # instead. » Un tour d'avance, pas plus : la toile ne tient qu'une fois.
        this = effect.this.CastTo(Upgrade)
        message.SetBeInstead(effect)
        Faces.DiscardAll([this], effect)

    return [
        AbilityFactory.AttachToFaceWhenPutIntoPlay(
            Enemy
        ),
        # « Attached enemy loses steady and stalwart. »
        *AbilityFactory.GiveKeywordToAttached(
            steady=-1,
            stalwart=-1,
        ),
        AbilityFactory.WhenEnemyWouldActivate(
            AbilityType.ForcedInterrupt,
            "AttachedEnemy",
            au_lieu_dactiver
        ),
    ]
