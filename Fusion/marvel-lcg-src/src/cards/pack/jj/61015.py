from . import *
def GetAbilities() -> Sequence['Ability']:
    def captain_marvel(effect: 'Effect', message: 'Message.AfterCardEnterPlay') -> None:
        this = effect.this.CastTo(Ally)
        player = effect.GetInitiator()
        discarded = player.DiscardDeckTopCards(4, effect)
        energy_count = len([f for f in discarded if HasResourceIcon.IsType(f) and f.printed_resource.y])
        if energy_count >= 1:
            player.ChooseAbilities(effect, AbilityFactory.ForChoiceAbility(
                'Remove 2 threat from a scheme',
                lambda targets: this.RemoveThreatFromSchemes(targets, 2, effect)
            ).SetTarget(Scheme2, range=(1, 1)))
        if energy_count >= 2:
            player.ChooseAbilities(effect, AbilityFactory.ForChoiceAbility(
                'Confuse an enemy',
                lambda targets: [Faces.GiveStatus(targets, "Confused", effect)]
            ).SetTarget(Enemy, range=(1, 1)))
    return [AbilityFactory.AfterCardEnterPlay(AbilityType.Response, "This", captain_marvel)]
