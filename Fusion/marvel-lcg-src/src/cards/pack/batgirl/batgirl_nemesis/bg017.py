from . import *

# * Mr. Zsasz — sbire, PV 3, SCH 1, ATQ 3, boost 1. « [star] Mr. Zsasz's attacks gain overkill. Forced Interrupt: When the villain phase
# begins, the player engaged with Mr. Zsasz must discard a card from their hand with a [physical] printed resource. If no card was
# discarded this way, that player takes 2 indirect damage. »
# Cartes de reference : `UnitAttackGainKeyword("This", overkill=True)`, bg016 (meme gabarit, fenetre WhenPhaseBegin).


def GetAbilities() -> Sequence['Ability']:

    def zsasz(effect: 'Effect', message: 'Message.WhenPhaseBegin') -> None:
        this = effect.this.CastTo(Minion)
        joueur = this.GetEngagedPlayer()
        if joueur is None:
            return
        cartes = CartesDeLaMain(joueur, "R")
        if cartes:
            choisie = joueur.AskChooseFace(cartes, effect)
            if choisie is not None:
                Faces.DiscardAll([choisie], effect)
                return
        joueur.GetIdentity().TakeIndirectDamage(this, 2, effect)

    return [
        AbilityFactory.UnitAttackGainKeyword("This", overkill=True),
        AbilityFactory.WhenPhaseBegin(AbilityType.ForcedInterrupt, "Villain", zsasz),
    ]
