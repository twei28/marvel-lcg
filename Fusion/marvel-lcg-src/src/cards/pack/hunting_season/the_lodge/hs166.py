from . import *

# hs166 * Black Cat (Experience Cost 4)
# [star] Forced Response : apres son contre, defausse la carte du dessus de ton deck ;
# si elle a une ressource [mental] imprimee, ajoute-la a ta main.

def GetAbilities() -> Sequence['Ability']:

    def fouiller(effect: 'Effect', message: 'Message.AfterUnitThwartEnd') -> None:
        joueur = effect.GetInitiator()
        if joueur.player_deck.GetSize() == 0 and joueur.discard_pile.GetSize() == 0:
            return
        face = joueur.DiscardDeckTopCard(effect)
        if face is not None and FacesCounter.GetPrintedResourcesCount([face], "B", joueur.player_deck) > 0:
            joueur.GainCard([face], effect)

    return [
        AbilityFactory.AfterUnitThwartEnd(AbilityType.ForcedResponse, "This", fouiller),
    ]
