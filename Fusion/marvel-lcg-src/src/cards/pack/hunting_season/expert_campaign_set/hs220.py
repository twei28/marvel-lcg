from . import *

# hs220 Hunted! (set de campagne experte)
# Chaque sbire engage avec toi gagne quickstrike.
# Alter-Ego Action : defausse une carte de ta main -> defausse Hunted!

def _pioche(effect: 'Effect', message: 'Message.AfterPlayerDrewCards') -> None:
    # Livret p.11 : une carte rencontre piochee dans le deck du joueur entre
    # immediatement en jeu dans sa zone, sans etre remplacee.
    effect.this.PutIntoPlay(message.to_player, effect)


def _engage_avec_le_porteur(effect: 'Effect', face: 'CardFace') -> int:
    porteur = effect.this.card.area.play_area
    if porteur is None or not Minion.IsType(face):
        return 0
    return 1 if face.CastTo(Minion).engaged_player == porteur else 0


def GetAbilities() -> Sequence['Ability']:
    return [
        AbilityFactory.AfterPlayerDrewCards(AbilityType.Campaign, "AnyPlayer", "This", _pioche),
        *AbilityFactory.GiveKeywordToInPlayWhenApplyThis(Minion, quickstrike=1, get_new_value=_engage_avec_le_porteur),
        AbilityFactory.PlayerActionToDiscardThis(AbilityType.AlterEgoAction).SetCostFunc(CostFunc.Discard("YourHandCards")),
    ]
