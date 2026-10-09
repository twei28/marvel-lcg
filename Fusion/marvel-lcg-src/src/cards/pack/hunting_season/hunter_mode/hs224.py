from . import *

# hs224 Cold Blooded (environnement du mode Hunter, scenario 3)
# La menace cible du complot principal est reduite de 1 par heros.
# Forced Response : apres l'activation de Curtis Connors contre ton heros,
# distribue-toi 1 carte rencontre face cachee.

def GetAbilities() -> Sequence['Ability']:

    def par_heros(effect: 'Effect', face: 'CardFace') -> int:
        return Worlds.GetPlayerNumIcon(effect)

    def contre_un_heros(effect: 'Effect', message: 'Message.AfterEnemyActivationEnd') -> bool:
        joueur = message.activate_message.to_player
        return joueur is not None and Hero.IsType(joueur.GetIdentity())

    def distribuer(effect: 'Effect', message: 'Message.AfterEnemyActivationEnd') -> None:
        message.activate_message.to_player.DealEncounterCards(1, effect)

    return [
        *AbilityFactory.GiveKeywordToInPlayWhenApplyThis(MainScheme, target_threat=-1, get_new_value=par_heros),
        AbilityFactory.AfterEnemyActivationEnd(AbilityType.ForcedResponse, CardFinder(name="Curtis Connors"),
                                               distribuer, conditions=[contre_un_heros]),
    ]
