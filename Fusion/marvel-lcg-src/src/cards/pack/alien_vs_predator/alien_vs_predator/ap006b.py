from . import *

# Battleground Earth (2B) — COMPLOT PRINCIPAL, stade 2. Seuil « — » (aucun : ce stade ne s'accomplit pas), escalade +1[per_hero],
#   depart 2[per_hero].
# Forced Response: After a villain attacks, give it a facedown boost card, then move the active counter to the next villain.
# Forced Response: After threat is placed here, if there is at least 4[per_hero] threat here, deal each player a facedown encounter card.
#   Then, remove 2[per_hero] threat from this scheme.
#
# Cartes de reference :
#  - « After a villain attacks » : `AfterEnemyActivationEnd(ForcedResponse, Villain)` filtre sur une fin d'ATTAQUE (`message.atk_message`) ;
#    « give it a facedown boost card » : `GiveFacedownBoostCardsInternal(1, ..)` (la carte attend sa prochaine activation, 60075) ;
#  - mechant SONNE dont la carte remplace l'attaque : le compteur passe, PAS de carte boost (arbitrage du 25/10/2026) ;
#  - « After threat is placed here » : `AfterSchemePlaceThreat(ForcedResponse, "This")` (pd026) ; « deal each player a facedown
#    encounter card » : `DealEncounterCards(1)` ; « remove X threat » : `RemoveThreatFromSchemes`.
#
# ⚠ Mots-pieges :
#  - au stade 2 le compteur ne bouge qu'apres une ATTAQUE (une manigance contre un alter-ego le laisse en place) ;
#  - « Then, remove 2[per_hero] » fait partie du « if » (sinon la menace ne monterait jamais) ;
#  - « at least 4[per_hero] » : 4 x joueurs ou plus, compte sur la carte entiere.


def GetAbilities() -> Sequence['Ability']:

    def apres_activation(effect: 'Effect', message: 'Message.AfterEnemyActivationEnd') -> None:
        if message.atk_message is None:
            OublierLaGarde(effect)          # une manigance : rien ne bouge, une garde posee pour elle tombe avec elle
            return
        mechant = message.trigger.CastTo(Villain)
        if mechant.IsInPlay():
            mechant.GiveFacedownBoostCardsInternal(1, effect, None)
        PasserLeCompteur(effect)

    def sonne_au_lieu_d_attaquer(effect: 'Effect', message: 'Message.AfterStatusDiscardFrom') -> bool:
        Unused(effect)
        return getattr(getattr(message, "by_effect", None), "this", None) is message.status and \
            bool(NomDuMechant(message.trigger))

    def compteur_seul(effect: 'Effect', message: 'Message.AfterStatusDiscardFrom') -> None:
        Unused(message)
        PasserLeCompteur(effect)

    def menace_posee(effect: 'Effect', message: 'Message.AfterSchemePlaceThreat') -> None:
        this = effect.this.CastTo(MainScheme)
        Unused(message)
        n = NombreDeJoueurs(effect)
        if this.threat < 4 * n:
            return
        for joueur in Worlds.GetPlayers(effect):
            joueur.DealEncounterCards(1, effect)
        this.RemoveThreatFromSchemes([this], 2 * n, effect)

    return [
        AbilityFactory.AfterEnemyActivationEnd(AbilityType.ForcedResponse, Villain, apres_activation),
        AbilityFactory.AfterStatusDiscardFrom(AbilityType.ForcedResponse, Villain, "Stunned", compteur_seul,
                                              conditions=[sonne_au_lieu_d_attaquer]),
        AbilityFactory.AfterSchemePlaceThreat(AbilityType.ForcedResponse, "This", menace_posee),
    ]
