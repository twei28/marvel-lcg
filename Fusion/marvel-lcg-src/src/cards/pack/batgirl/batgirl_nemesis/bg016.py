from . import *

# * The Reaper — sbire, PV 4, SCH 1, ATQ 2, boost 1. « [star] The Reaper's attacks gain piercing. Forced Response: After the villain phase
# ends, the player engaged with The Reaper must discard a card from their hand with a printed [energy] resource. If no card was
# discarded this way, place 1 threat on the main scheme. »
# Cartes de reference : `UnitAttackGainKeyword("This", piercing=True)` (uw010), `uw014` (`AfterPhaseEnd(ForcedResponse, "Villain")`).


def GetAbilities() -> Sequence['Ability']:

    def reaper(effect: 'Effect', message: 'Message.AfterPhaseEnd') -> None:
        this = effect.this.CastTo(Minion)
        joueur = this.GetEngagedPlayer()
        if joueur is None:
            return
        cartes = CartesDeLaMain(joueur, "Y")
        if cartes:
            choisie = joueur.AskChooseFace(cartes, effect)
            if choisie is not None:
                Faces.DiscardAll([choisie], effect)
                return
        principal = Worlds.FindMainScheme(effect)
        if principal is not None:
            this.PlaceThreatOnSchemes([principal], 1, effect)

    return [
        AbilityFactory.UnitAttackGainKeyword("This", piercing=True),
        AbilityFactory.AfterPhaseEnd(AbilityType.ForcedResponse, "Villain", reaper),
    ]
