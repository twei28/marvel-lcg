from . import *
def GetAbilities() -> Sequence['Ability']:
    def norn_stone(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        this = effect.this.CastTo(Upgrade)
        initiator = effect.GetInitiator()
        Faces.ReadyAll([initiator.GetIdentity()], effect)
        this.card.Flip(effect)
    return [*AbilityFactory.GiveKeywordToAttached(Hero, thwart=1, attack=1, defense=1),
            AbilityFactory.WhenInYourPlayTurn(AbilityType.HeroAction, norn_stone)]
