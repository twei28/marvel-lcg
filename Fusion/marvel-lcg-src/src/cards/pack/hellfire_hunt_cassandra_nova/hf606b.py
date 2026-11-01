from . import *

# Mutant Extermination (3B), stade 3 (dernier). Menace 13[per_hero], escalade +1[per_hero], menace de depart 3[per_hero].
# « Forced Response : After your turn ends, if there is Cassandra Controls counter on your identity, you must choose to either place 3 threat here
# or discard 1 card from your hand. Hero Action : Discard 7 cards from the top of the encounter deck -> remove a Cassandra Controls counter from
# your identity. (Limit once per round per player.) When this scheme is completed, the players lose the game. »
# Cartes de reference : hf604b, gb006b (`IfThisSchemeStageIsCompletedPlayersLoseTheGame`).
# ⚠ Le texte imprime dit « When this scheme is completed » : la regle native du moteur lit « If this stage/scheme is completed » (scheme_main.py) ;
# la capacite est donc posee a la main ici (le texte imprime reste fidele au scan).


def GetAbilities() -> Sequence['Ability']:
    return [
        ReponseFinDeTour(3, "Discard 1 card from your hand", PenaliteDefausse, possible=MainNonVide),
        ActionRetirerControle(7),
        AbilityFactory.IfThisSchemeStageIsCompletedPlayersLoseTheGame(),
    ]
