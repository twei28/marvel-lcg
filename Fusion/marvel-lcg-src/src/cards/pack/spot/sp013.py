from . import *

# Spotty Pasts

def GetAbilities() -> Sequence['Ability']:

    def fin_de_phase(effect: 'Effect', message: 'Message.WhenPhaseEnd') -> None:
        this = effect.this.CastTo(EncounterSideScheme)

        # « if there is 5 threat or greater here, the first player finds a Spot
        # minion and reveals it. »
        seuil = Worlds.ConvertPerPlayerIconToInt("5*", effect)
        if this.threat < seuil:
            return
        Find.FindAndReveal(
            effect,
            Worlds.GetFirstPlayer(effect),
            finder=CardFinder(set_name="The Spot", card_type=Minion)
        )

    return [
        AbilityFactory.WhenVillainPhaseEnd(
            AbilityType.ForcedResponse,
            fin_de_phase
        ),
    ]
