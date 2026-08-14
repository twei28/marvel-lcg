from . import *

# Power Outage (1B)

def GetAbilities() -> Sequence['Ability']:

    def soin(effect: 'Effect', message: 'Message.AfterResolveVillainPhaseStep') -> None:
        # « [star] Forced Response: After resolving step one of the villain
        # phase, heal 1 damage from the villain for each acceleration token and
        # icon in play. »
        #
        # L'etape 1 de la phase du vilain est celle ou le complot principal
        # prend sa menace : c'est le meme battement qui rend ses PV au vilain.
        this = effect.this.CastTo(MainScheme)
        valeur = JetonsEtIconesDAcceleration(effect)
        if valeur <= 0:
            return
        villain = Worlds.FindVillain(effect)
        if villain:
            this.HealthUnits([villain], valeur, effect)

    return [
        AbilityFactory.AfterResolveVillainPhaseStep(
            AbilityType.ForcedResponse,
            1,
            soin
        ),
    ]
