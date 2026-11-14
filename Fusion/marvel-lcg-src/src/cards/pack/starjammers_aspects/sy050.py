from . import *
# Plasnet Launcher (Protection, amelioration 1 par heros [mental]). TECH. WEAPON. Restricted. Uses (3 charge counters).
# Action: Exhaust Plasnet Launcher and remove 1 charge counter from it → the villain gets -1 ATK until the end of the round.
#
# Cartes de reference : 16046 Hand Cannon (`desc.Uses "N,charge"` + `CostFunc.Counter("This", 1, 'charge')`) ; brawn/bw008 (`GainUntilRoundEnd(
# effect, attack=N)`) ; 40053 / 44046 (`desc.Cost "N*"` = N par heros) ; fiches uses.md, restricted.md.
# « the villain gets -1 ATK » : le (premier) vilain ; cumulatif si l'Action est reutilisee (la carte est incline : une fois par round).
def GetAbilities() -> Sequence['Ability']:
    def plasnet(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        vilain = Worlds.FindVillain(effect)
        if vilain is not None:
            vilain.GainUntilRoundEnd(effect, attack=-1)
    return [
        AbilityFactory.CanPlayThisUpgradeCard(),
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.Action,
            plasnet,
        ).SetCostFunc(CostFunc.Exhaust("This"))
        .SetCostFunc(CostFunc.Counter("This", 1, 'charge')),
    ]
