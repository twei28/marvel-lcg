from . import *

def GetAbilities() -> Sequence['Ability']:
    def reveler(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        joueur = message.GetToPlayer()
        if joueur is None:
            return
        ameliorations = [f for f in joueur.GetControlCards() if f.IsInPlay() and Upgrade.IsType(f)]
        if ameliorations:
            choisie = ameliorations[0] if len(ameliorations) == 1 else joueur.AskChooseFace(
                ameliorations, effect, prompt="Discard an upgrade you control", forced=True)
            if choisie is not None:
                Faces.DiscardAll([choisie], effect)
                return
        joueur.DiscardRandomHandCards(1, effect)

    return [
        # Teamwork (IMPERIAL GUARD) est LU DANS `desc` (can_teamwork.py) : aucun script.
        AbilityFactory.UnitAttackGainKeyword("This", piercing=True),
        AbilityFactory.WhenThisRevealed(None, reveler),
    ]
