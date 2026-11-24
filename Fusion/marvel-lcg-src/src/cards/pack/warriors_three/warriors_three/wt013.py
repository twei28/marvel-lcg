from . import *


def GetAbilities() -> Sequence['Ability']:
    def hold(effect: 'Effect', message: 'Message.WhenSchemeWouldPlaceThreat') -> None:
        joueur = effect.GetInitiator()
        message.PreventThreat("All", effect)
        if paye_avec(effect, "Hogun"):
            ennemis = [f for f in Worlds.FindCardsOnField(effect, card_type=Enemy) if f.IsInPlay()]
            if ennemis:
                cible = joueur.AskChooseFace(ennemis, effect, prompt="Stun an enemy", forced=True)
                if cible is not None:
                    Faces.GiveStatus([cible], "Stunned", effect)

    return [
        AbilityFactory.WhenThreatWouldBePlacedOn(AbilityType.HeroInterrupt, None, hold).SetPlay().SetLabel(),
    ]
