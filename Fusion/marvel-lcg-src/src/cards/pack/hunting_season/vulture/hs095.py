from . import *

# hs095 Aerial Kidnapping
# Surge (donnees). Forced Interrupt : au debut de la phase du vilain, 3 menace sur le complot principal et defaussez ceci.
# When Defeated : Vulture perd AERIAL jusqu'a la fin du tour du joueur actif.

def GetAbilities() -> Sequence['Ability']:

    def enlever(effect: 'Effect', message: 'Message.WhenPhaseBegin') -> None:
        effect.this.PlaceThreatOnSchemes("MainScheme", 3, effect)
        Faces.DiscardAll([effect.this], effect)

    def vaincue(effect: 'Effect', message: 'Message.WhenSchemeBeDefeated') -> None:
        v = Vulture(effect)
        if v is not None:
            PerdreAerialJusquauTour(v, effect)

    return [
        AbilityFactory.WhenVillainPhaseBegin(AbilityType.ForcedInterrupt, enlever),
        AbilityFactory.WhenSchemeBeDefeated(AbilityType.WhenDefeated, "This", vaincue),
    ]
