from . import *

# hs207 Captured! (set de campagne experte)
# Tu ne peux pas changer de forme. Action : incline ton identite -> defausse Captured!

def _pioche(effect: 'Effect', message: 'Message.AfterPlayerDrewCards') -> None:
    # Livret p.11 : une carte rencontre piochee dans le deck du joueur entre
    # immediatement en jeu dans sa zone, sans etre remplacee.
    effect.this.PutIntoPlay(message.to_player, effect)


def GetAbilities() -> Sequence['Ability']:
    return [
        AbilityFactory.AfterPlayerDrewCards(AbilityType.Campaign, "AnyPlayer", "This", _pioche),
        AbilityFactory.PlayersCannotChangeForms(AbilityType.NonKeyword, "AttachedPlayer"),
        AbilityFactory.PlayerActionToDiscardThis(AbilityType.Action).SetCostFunc(CostFunc.Exhaust("YourIdentity")),
    ]
