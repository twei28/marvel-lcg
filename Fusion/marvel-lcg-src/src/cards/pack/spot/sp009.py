from . import *

# Anywhere & Everywhere

def GetAbilities() -> Sequence['Ability']:

    def fin_de_phase(effect: 'Effect', message: 'Message.WhenPhaseEnd') -> None:
        this = effect.this.CastTo(EncounterSideScheme)

        # « if there is 3 threat or greater here, place 1 threat on each card
        # in play with the Threat Level keyword. »
        seuil = Worlds.ConvertPerPlayerIconToInt("3*", effect)
        if this.threat < seuil:
            return
        cibles = Worlds.GetThreatLevelFaces(effect)
        if cibles:
            Faces.PlaceTokensOn(cibles, "1*", 'threat', effect)

    return [
        AbilityFactory.WhenVillainPhaseEnd(
            AbilityType.ForcedResponse,
            fin_de_phase
        ),
    ]
