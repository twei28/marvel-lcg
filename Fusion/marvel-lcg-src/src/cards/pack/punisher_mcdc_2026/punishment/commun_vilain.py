from . import *

def ReponseDeHeros(*, meme_type: bool, carte_de_boost: bool) -> 'Ability':
    """« Hero Response : After you attack Punisher, spend 2 resources of [any type | the same type] → flip Target Lock to its
    DISTRACTED side and discard one non-permanent attachment from Punisher. [Give Punisher a facedown boost card.] »"""

    def operation(effect: 'Effect', message: 'Message.AfterUnitAttackUnit') -> None:
        this = effect.this
        joueur = effect.GetInitiator()
        RetournerTargetLockVersDistracted(effect)
        candidates = [a for a in this.GetAttachedAttachments() if not a.permanent]
        if candidates:
            choisie = candidates[0] if len(candidates) == 1 else joueur.AskChooseFace(candidates, effect)
            if choisie is not None:
                Faces.DiscardAll([choisie], effect)
        if carte_de_boost:
            DonnerUneCarteBoostFaceCachee(effect, this, 1)

    cout = Cost("2", same_type=True) if meme_type else Cost("2")
    return AbilityFactory.AfterUnitAttackUnit(
        AbilityType.HeroResponse, "You", "This", operation,
    ).SetCostFunc(CostFunc.Spend(cout))
