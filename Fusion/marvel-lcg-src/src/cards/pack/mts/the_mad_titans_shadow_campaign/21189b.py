from . import *
def GetAbilities() -> Sequence['Ability']:
    def loki_defeated(effect: 'Effect', message: 'Message.WhenUnitWouldBeDefeated') -> None:
        this = effect.this.CastTo(Attachment)
        Faces.RemoveAllFromGame([this], effect)
    return [AbilityFactory.AttachToFaceWhenPutIntoPlayInternal(CardFinder(name='Loki')),
            *AbilityFactory.GiveKeywordToAttached(CardFinder(name='Loki'), health=lambda effect: (4 * Worlds.GetPlayerNumIcon(effect))),
            AbilityFactory.WhenUnitWouldBeDefeated(AbilityType.ForcedInterrupt, CardFinder(name='Loki'), loki_defeated)]
