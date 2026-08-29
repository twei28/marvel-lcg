from . import *
def GetAbilities() -> Sequence['Ability']:
    def harlems_hero(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(this)
        lc = Worlds.FindCardOnField(effect, name='Luke Cage')
        if not lc:
            return
        Faces.GiveStatus([lc], "Tough", effect)
        n = lc.tough
        player = effect.GetInitiator()
        for _ in range(n):
            candidates = [f for f in player.GetControlCardsByType(ally=True, identity=True) if not f.IsReady()]
            if not candidates:
                break
            def ready_chosen(targets: Sequence['CardFace']):
                Faces.ReadyAll(list(targets), effect)
            player.ChooseAbilities(effect, AbilityFactory.ForChoiceAbility('Ready a character', ready_chosen).SetTarget(candidates, range=(1, 1)))
    return [AbilityFactory.WhenInYourPlayTurn(AbilityType.HeroAction, harlems_hero).SetPlay()]
