from . import *

# hs049 Tail Enhancements

def GetAbilities() -> Sequence['Ability']:
    def revelee(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        joueur = message.GetToPlayer()
        carte = Worlds.DiscardEncounterCardsUntil(effect, trait="TAIL", card_type=Attachment)
        if carte is not None:
            carte.Reveal(joueur, effect)

    def icones(effect: 'Effect', message: 'Message.WhenBoostIconsWouldBeCount') -> None:
        scorpion, queue = ScorpionEtQueue(effect)
        if scorpion is None:
            return
        nombre = sum(1 for a in scorpion.GetAttachedAttachments() + queue.GetAttachedAttachments() if a.HasTrait("TAIL"))
        if nombre:
            message.UpdateBoostIcon(nombre, effect)

    return [
        AbilityFactory.WhenThisRevealed(None, revelee),
        AbilityFactory.WhenBoostIconsWouldBeCount(
            AbilityType.NonKeyword, icones,
            conditions=[lambda effect, message: message.trigger is effect.this],
        ),
    ]
