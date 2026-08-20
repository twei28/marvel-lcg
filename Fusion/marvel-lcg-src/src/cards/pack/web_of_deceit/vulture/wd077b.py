from . import *

# Surveillance Pigeons (1B)

def GetAbilities() -> Sequence['Ability']:

    def bouclier(effect: 'Effect', message: 'Message.WhenSchemeWouldRemoveThreat') -> None:
        # « Forced Interrupt: When any amount of threat would be removed from
        # this scheme, if there are at least 3 pigeon counters here, remove
        # 3 pigeon counters from here instead. »
        this = effect.this.CastTo(MainScheme)
        message.SetBeInstead(effect)
        Faces.RemoveCountersOn([this], 3, 'pigeon', effect)

    def assez_de_pigeons(effect: 'Effect', message: 'Message.WhenSchemeWouldRemoveThreat') -> bool:
        return effect.this.CastTo(CanPlaceCounter).GetCounters('pigeon') >= 3

    # ⚠ CLAUSE NON RENDUE, ecrite plutot que silencieuse.
    #
    # « Interrupt: When you would discard a random card from your hand, you may
    # place 2 pigeon counters here instead. »
    #
    # Le moteur n'a AUCUNE fenetre sur une defausse ALEATOIRE :
    # `DiscardRandomHandCards` (player_action.py) tire les cartes puis appelle
    # `Faces.DiscardAll`, qui n'emet qu'un `WhenCardWouldDiscard` par carte,
    # identique a celui d'une defausse CHOISIE. S'accrocher a ce message ferait
    # donc esquiver AUSSI les defausses volontaires — un cout de carte, la
    # limite de main — ce qui est bien plus large que le texte.
    #
    # Le rendre demande un message moteur neuf, sur le modele de
    # `WhenPlayerWouldBeDealtEncounterCard` (sender_player.py:364) : classe
    # `CanBeInstead`, fabrique dans factory/player.py, et l'appel dans
    # `DiscardRandomHandCards`. C'est une modification du MOTEUR partage, pas
    # de cette carte : a decider a part.
    #
    # Consequence en jeu : le scenario est plus dur que son texte. Web of Deceit
    # defausse au hasard souvent (wd008, wd078, wd081, wd068), et le joueur n'a
    # pas la soupape que la carte lui promet.

    return [
        AbilityFactory.WhenSchemeWouldRemoveThreat(
            AbilityType.ForcedInterrupt,
            "This",
            bouclier,
            conditions=[assez_de_pigeons],
        ),
        # « If this stage is completed, the players lose the game. »
        AbilityFactory.IfThisSchemeStageIsCompletedPlayersLoseTheGame(),
    ]
