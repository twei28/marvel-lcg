from . import *
def GetAbilities() -> Sequence['Ability']:
    def son_of_zeus(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(this)
        initiator = effect.GetInitiator()
        identity = initiator.GetIdentity()
        Faces.ReadyAll([identity], effect)
        gifts = CountGifts(effect, initiator)
        if (gifts >= 1):
            upgrades = [f for f in Worlds.FindCardsOnField(effect, card_type=Upgrade) if (f.GetControlByPlayer() == initiator) and f.IsClass('IdentitySpecific') and (not f.card.state.is_ready)]
            if upgrades:
                def action(targets: Sequence['CardFace']):
                    Faces.ReadyAll(list(targets), effect)
                initiator.ChooseAbilities(effect, AbilityFactory.ForChoiceAbility('Ready an identity-specific upgrade', action).SetTarget(upgrades, range=(1, 1), not_move=True))
        if (gifts >= 2):
            Faces.GiveStatus([identity], 'Tough', effect)
        if (gifts >= 3):
            initiator.DrawUp(1, effect)
    return [AbilityFactory.WhenInYourPlayTurn(AbilityType.HeroAction, son_of_zeus).SetPlay().SetLabel()]
