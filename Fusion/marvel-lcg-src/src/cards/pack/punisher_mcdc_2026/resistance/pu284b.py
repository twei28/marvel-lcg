from . import *

# Guerilla Warfare (Civil War, 2B, Resistance 6/8) — le complot 2 du defi p280 (carte fournie par capture, absente du moteur).
# Forced Response : After a status card is placed on the enemy leader, place 1 threat here.
# If this stage is completed, the players lose the game. (9 par joueur ; menace de depart 0 ; +1 par joueur : valeurs de `desc`.)
#
# Cartes de reference : harry_osborn/ho012 et skrull_menace/paibok/sk154 (`AfterStatusCardPlaceOn(type, qui, statuts, op)`), cw/resistance/56142b (« EnemyLeader » :
# le Leader adverse), gmw/campaign.py (`scheme.PlaceThreatInternal(n, effect)`), `AfterSchemePlaceThreat` de rainy/ra029.
# ⚠ Mots-pieges : « a status card » = TOUT statut (Stunned, Confused, Tough, ...) ; « the enemy LEADER » = le Leader (les Civil War ont des Leaders), pas un sbire ;
# « place 1 threat HERE » = sur ce complot (cette carte), pas sur le principal en general ; « Forced Response ».
# La condition de defaite (« If this stage is completed ») est le comportement de base d'un complot principal.


def GetAbilities() -> Sequence['Ability']:

    def une_menace(effect: 'Effect', message: 'Message.AfterStatusCardPlaceOn') -> None:
        effect.this.CastTo(MainScheme).PlaceThreatInternal(1, effect)

    return [
        AbilityFactory.AfterStatusCardPlaceOn(AbilityType.ForcedResponse, "EnemyLeader", None, une_menace),
    ]
