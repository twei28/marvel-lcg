from . import *

def GetAbilities() -> Sequence['Ability']:
    def amis_pour_toujours(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        Unused(message)
        joueur = JoueurDeCetteCarte(effect)
        if joueur is None:
            return
        face = Search.PlayerCard(
            effect,
            joueur,
            include_player_deck=True,
            include_discard_pile=True,
            finder=CardFinder(name=NOM_CRREEE),
        )
        if face:
            joueur.GainCard(face, effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.Action,
            amis_pour_toujours,
        ).SetName("Forever Friends")
        .SetCostFunc(CostFunc.Discard("YourHandCards", range=(1, 1)))
        .LimitOncePerPhase(),
    ]
