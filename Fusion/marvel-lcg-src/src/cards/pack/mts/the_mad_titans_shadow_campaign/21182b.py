from . import *
def GetAbilities() -> Sequence['Ability']:
    def after_engage(effect: 'Effect', message: 'Message.AfterMinionEngagePlayer') -> None:
        this = effect.this.CastTo(Minion)
        Unused(this)
        player = message.GetToPlayer()
        def action(targets):
            Faces.DiscardAll(list(targets), effect)
        player.ChooseAbilities(effect, AbilityFactory.ForChoiceAbility('Discard 1 card from your hand', action).SetTarget('YourHandCards', range=(1, 1), canbe_discard=True))
    return [AbilityFactory.AfterMinionEngagePlayer(AbilityType.ForcedResponse, 'This', None, after_engage)]
