from . import *
def GetAbilities() -> Sequence['Ability']:
    def choreography(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Upgrade)
        Unused(this)
        initiator = effect.GetInitiator()
        faces = [face for face in initiator.discard_pile.Get() if IsAspectOrBasicEvent(face)]
        if not faces:
            if not initiator.IsInHeroForm():
                initiator.DrawUp(1, effect)
            return
        def action(targets: Sequence['CardFace']):
            Faces.ShuffleAllTo(list(targets), initiator.player_deck, effect)
            if not initiator.IsInHeroForm():
                initiator.DrawUp(1, effect)
        initiator.ChooseAbilities(effect, AbilityFactory.ForChoiceAbility('Shuffle 1 aspect or basic event into your deck', action).SetTarget(faces, range=(1, 1)))
    def check_has_event(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> bool:
        initiator = effect.GetInitiator()
        if not initiator:
            return False
        if not initiator.IsInHeroForm():
            return True
        for face in initiator.discard_pile.Get():
            if IsAspectOrBasicEvent(face):
                return True
        return False
    return [AbilityFactory.CanPlayThisUpgradeCard(),
            AbilityFactory.WhenInYourPlayTurn(AbilityType.Action, choreography, conditions=[check_has_event]).SetCostFunc(CostFunc.Exhaust('This'))]
