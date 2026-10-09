from . import *

# hs084 S.H.I.E.L.D. Wingsuits
# Hero Action : une ressource de n'importe quel type, votre heros et vos allies gagnent AERIAL jusqu'a la fin de la ronde.

def GetAbilities() -> Sequence['Ability']:

    def planer(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        joueur = message.to_player
        heros = joueur.GetIdentity()
        allies = [f for f in Worlds.GetOnFieldFriendlyCharacters(effect)
                  if Ally.IsType(f) and f.GetControlByPlayer() == joueur]
        for f in [heros, *allies]:
            GagnerAerialJusquaLaRonde(f, effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(AbilityType.HeroAction, planer).SetCost(Cost("1")),
    ]
