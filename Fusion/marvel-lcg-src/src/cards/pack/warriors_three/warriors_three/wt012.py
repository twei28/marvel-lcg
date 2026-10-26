from . import *


def GetAbilities() -> Sequence['Ability']:
    def bladework(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        Unused(message)
        this = effect.this.CastTo(Event)
        joueur = effect.GetInitiator()
        this.DealDamage(effect.targets, 4, effect)
        if paye_avec(effect, "Fandral"):
            ennemis = [f for f in Worlds.FindCardsOnField(effect, card_type=Enemy) if f.IsInPlay()]
            if ennemis:
                cible = joueur.AskChooseFace(ennemis, effect, prompt="Deal 2 damage to an enemy", forced=True)
                if cible is not None:
                    this.DealDamage([cible], 2, effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(AbilityType.HeroAction, bladework).SetPlay().SetLabel('attack')
        .SetTarget(Enemy),
    ]
