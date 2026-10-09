from . import *

# hs058b Reptile Brain Taking Over
# X = cartes REPTILE en jeu (le Lizard compris). Les valeurs imprimees valent 0
# en data : la menace de depart est posee a la revelation, l'escalade est
# calculee a chaque phase.

def GetAbilities() -> Sequence['Ability']:

    def menace_de_depart(effect: 'Effect', message: 'Message.WhenCardRevealed') -> None:
        x = NombreReptiles(effect)
        if x > 0:
            effect.this.PlaceThreatOnSchemes([effect.this], x, effect)

    return [
        AbilityFactory.WhenThisRevealed(None, menace_de_depart),
        AbilityFactory.WhenCalcThisSchemeEscalation(lambda effect: NombreReptiles(effect)),
    ]
