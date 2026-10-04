from . import *

# Alontech's Greatest Achievement — manigance annexe, WAVE NEMESIS 1/5.
# Menace de depart : 2 PAR JOUEUR (icone silhouette, base automatique du
# desc, aucun code).
# Increase the cost of the first event each player plays each turn by 1.
#
# La hausse de cout elle-meme : `AbilityFactory.IncreaseResourceCostToPlay(
# CardFinder(card_type=Event), 1, "EachPlayer")`, modele `ar010` Ire of
# Athena (pack ares) -- SEULE fabrique qui augmente un cout de jeu
# (resources.py:668). `which_player="EachPlayer"` est propre a CETTE fabrique
# (parametre local a `UpdateCostOfCardInternal`), a ne pas confondre avec le
# `PlayerType` general des AUTRES fabriques (`Condition.PLAYER_TYPE`, qui n'a
# PAS « EachPlayer » -- seulement « AnyPlayer », combine au champ `to_player`
# du message pour cibler un joueur precis).
#
# « the FIRST event ... EACH TURN » : la hausse ne s'applique qu'UNE fois par
# joueur et par tour -- un drapeau par joueur, remis a zero au debut de SON
# tour (`WhenPlayerTurnBegin(Rule, "AnyPlayer", ...)`) et pose des qu'il joue
# un evenement (`WhenPlayerPlayCard(Rule, "AnyPlayer", CardFinder(
# card_type=Event), ...)`, game/ability/factory/play.py:283). Le drapeau
# EMPECHE la hausse (via `conditions`) plutot que de l'annuler apres coup :
# pas de mecanisme de remboursement de cout dans ce depot.

def GetAbilities() -> Sequence['Ability']:
    deja_augmente: Dict['Player', bool] = {}

    def premier_evenement_du_tour(effect: 'Effect', message: 'Message.WhenCalculateEffectCost') -> bool:
        joueur = message.GetToPlayer()
        if joueur is None:
            return False
        return not deja_augmente.get(joueur, False)

    def marquer_consomme(effect: 'Effect', message: 'Message.WhenPlayerPlayCard') -> None:
        Unused(effect)
        joueur = message.to_player
        if joueur is not None:
            deja_augmente[joueur] = True

    def reinitialiser(effect: 'Effect', message: 'Message.WhenPlayerTurnBegin') -> None:
        Unused(effect)
        joueur = message.to_player
        if joueur is not None:
            deja_augmente[joueur] = False

    return [
        AbilityFactory.IncreaseResourceCostToPlay(
            CardFinder(card_type=Event), 1, "EachPlayer",
            conditions=[premier_evenement_du_tour],
        ),
        AbilityFactory.WhenPlayerPlayCard(
            AbilityType.Rule, "AnyPlayer", CardFinder(card_type=Event),
            marquer_consomme,
        ),
        AbilityFactory.WhenPlayerTurnBegin(
            AbilityType.Rule, "AnyPlayer",
            reinitialiser,
        ),
    ]
