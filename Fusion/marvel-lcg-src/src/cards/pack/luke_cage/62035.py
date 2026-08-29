from . import *
def GetAbilities() -> Sequence['Ability']:
    def observe(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Event)
        Unused(this)
        villain = Worlds.FindVillain(effect)
        if villain:
            villain.Scheme(effect)
        hero = effect.GetInitiator().GetHero()
        Faces.GiveStatus([hero], "Tough", effect)
    return [AbilityFactory.WhenInYourPlayTurn(AbilityType.HeroAction, observe).SetPlay()]
