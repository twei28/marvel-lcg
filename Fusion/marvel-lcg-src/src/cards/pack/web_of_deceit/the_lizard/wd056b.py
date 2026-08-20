from . import *

# The Cure (2B)

def GetAbilities() -> Sequence['Ability']:

    def soigner(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> None:
        # « Alter-Ego Action: If you control a GENIUS character, spend
        # [mental][mental] resources → remove 4 threat from here. »
        this = effect.this.CastTo(MainScheme)
        this.RemoveThreatFromSchemes([this], 4, effect)

    def a_un_genie(effect: 'Effect', message: 'Message.WhenPlayerInTurn') -> bool:
        joueur = effect.GetInitiator()
        return joueur.GetControlCards(CardFinder(trait="GENIUS", card_type=Friend)) != []

    def plus_de_menace(effect: 'Effect', message: 'Message.AfterSchemeRemoveThreat') -> None:
        # « If there is no threat here and the Lizard is not in play, the
        # players win the game. »
        #
        # Les DEUX conditions comptent : vider la manigance ne suffit pas tant
        # que The Lizard tient la table — c'est Curt Connors qui doit rester.
        this = effect.this.CastTo(MainScheme)
        if this.threat > 0:
            return
        if Worlds.FindCardOnField(effect, name="The Lizard", card_type=Villain):
            return
        Worlds.SetGameOver(True, effect)

    return [
        AbilityFactory.WhenInYourPlayTurn(
            AbilityType.AlterEgoAction,
            soigner,
            conditions=[a_un_genie],
        # « (Limit once per round PER PLAYER.) » : `LimitOncePerRound` est
        # globale et interdisait l'action a tous les autres joueurs des qu'un
        # seul l'avait utilisee. Sans effet en solo, faux des deux joueurs.
        ).SetCost(Cost("BB")).LimitOncePerRoundPerPlayer(),
        AbilityFactory.AfterSchemeRemoveThreat(
            AbilityType.ForcedResponse,
            "This",
            plus_de_menace
        ),
        # « If this stage is completed, the players lose the game. »
        AbilityFactory.IfThisSchemeStageIsCompletedPlayersLoseTheGame(),
    ]
