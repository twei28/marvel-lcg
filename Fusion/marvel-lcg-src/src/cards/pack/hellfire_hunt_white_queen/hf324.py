from . import *

# Mind Manipulation. Attachement ILLUSION PSIONIC. « Treat attached ally as a minion with a blank text box (except for TRAITS). Attach minion's SCH is
# equal to its printed THW and it does not take consequential damage. When Revealed : Attach to the ally you control with the lowest cost. If you cannot,
# this card gains surge. » Carte de reference : hp017 Take Over Signal (`TreatAttachedCardAsMinion`), `AttachToFaceWhenPutIntoPlay(..., lowest cost)`.


def GetAbilities() -> Sequence['Ability']:
    def revelee(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        this = effect.this
        joueur = message.GetToPlayer()
        allies = [f for f in joueur.GetControlCards(CardFinder(card_type=Ally)) if f.IsInPlay()]
        cible = Filter.One(allies, effect, lowest_cost=True)
        if cible is None:
            ThisCardGainSurge(effect)
            return
        this.AttachTo2(cible, effect)

    return [
        AbilityFactory.TreatAttachedCardAsMinion(Ally, "Minion"),
        AbilityFactory.WhenThisRevealed(None, revelee),
    ]
